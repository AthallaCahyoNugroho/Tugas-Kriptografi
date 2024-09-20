import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

def create_playfair_matrix(key):
    key = key.upper().replace("J", "I")  # Replace J with I
    used_chars = set()
    matrix = []

    for char in key:
        if char not in used_chars and char.isalpha():
            used_chars.add(char)
            matrix.append(char)

    for char in range(65, 91):  # ASCII A-Z
        letter = chr(char)
        if letter not in used_chars and letter != "J":
            used_chars.add(letter)
            matrix.append(letter)

    return np.array(matrix).reshape(5, 5)

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return (row, col)
    return None

def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = ''.join(filter(str.isalpha, text))

    digraphs = []
    i = 0

    while i < len(text):
        if i + 1 < len(text):
            if text[i] == text[i + 1]:
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i] + text[i + 1])
                i += 2
        else:
            digraphs.append(text[i] + 'X')
            i += 1

    return digraphs

def encrypt_playfair(text, key):
    matrix = create_playfair_matrix(key)
    digraphs = prepare_text(text)
    result = ""

    for digraph in digraphs:
        pos1 = find_position(matrix, digraph[0])
        pos2 = find_position(matrix, digraph[1])

        if pos1 and pos2:
            row1, col1 = pos1
            row2, col2 = pos2

            if row1 == row2:  # Same row
                result += matrix[row1, (col1 + 1) % 5]
                result += matrix[row2, (col2 + 1) % 5]
            elif col1 == col2:  # Same column
                result += matrix[(row1 + 1) % 5, col1]
                result += matrix[(row2 + 1) % 5, col2]
            else:  # Rectangle swap
                result += matrix[row1, col2]
                result += matrix[row2, col1]

    return result

def decrypt_playfair(text, key):
    matrix = create_playfair_matrix(key)
    digraphs = prepare_text(text)  # Prepare digraphs for the ciphertext
    result = ""

    for digraph in digraphs:
        pos1 = find_position(matrix, digraph[0])
        pos2 = find_position(matrix, digraph[1])

        if pos1 is None or pos2 is None:
            messagebox.showerror("Decryption Error", f"Character '{digraph[0] if pos1 is None else digraph[1]}' not found in matrix.")
            return ""

        row1, col1 = pos1
        row2, col2 = pos2

        if row1 == row2:  # Same row
            result += matrix[row1, (col1 - 1) % 5]
            result += matrix[row2, (col2 - 1) % 5]
        elif col1 == col2:  # Same column
            result += matrix[(row1 - 1) % 5, col1]
            result += matrix[(row2 - 1) % 5, col2]
        else:  # Rectangle swap
            result += matrix[row1, col2]
            result += matrix[row2, col1]

    # Remove trailing X if it was added as padding
    if result.endswith('X') and len(result) > 1:
        result = result[:-1]
        
    return result

def encrypt_text():
    text = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    if key and text:
        ciphertext = encrypt_playfair(text, key)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, ciphertext)
    else:
        messagebox.showwarning("Input Error", "Please enter both text and a key.")

def decrypt_text():
    text = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    if key and text:
        plaintext = decrypt_playfair(text, key)
        if plaintext:  # Only update if decryption was successful
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, plaintext)
    else:
        messagebox.showwarning("Input Error", "Please enter both text and a key.")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text = file.read()
            text_input.delete(1.0, tk.END)
            text_input.insert(tk.END, text)

# Create the main window
root = tk.Tk()
root.title("Playfair Cipher")

# Create input and output text boxes
text_input = tk.Text(root, wrap=tk.WORD, width=50, height=10)
text_input.pack(pady=10)
result_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
result_text.pack(pady=10)

# Create key input and buttons
key_label = tk.Label(root, text="Enter Key:")
key_label.pack(pady=5)
key_input = tk.Entry(root, width=50)
key_input.pack(pady=5)
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_text)
encrypt_button.pack(pady=5)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_text)
decrypt_button.pack(pady=5)
load_button = tk.Button(root, text="Load File", command=load_file)
load_button.pack(pady=5)

root.mainloop()
