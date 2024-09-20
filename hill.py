import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

def matrix_inverse(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))  # Determinant
    det_inv = pow(det, -1, modulus)  # Modular inverse of determinant
    
    # Adjugate matrix
    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    
    return (det_inv * adjugate) % modulus

def create_hill_key_matrix(key):
    # Convert key to numeric matrix (assuming it's a 2x2 matrix)
    key = key.replace(' ', '').upper()
    key_matrix = np.array([[ord(key[0]) - 65, ord(key[1]) - 65],
                            [ord(key[2]) - 65, ord(key[3]) - 65]])
    return key_matrix

def encrypt_hill(text, key):
    modulus = 26
    key_matrix = create_hill_key_matrix(key)
    
    # Pad text if necessary
    while len(text) % 2 != 0:
        text += 'X'

    text_numeric = [ord(char) - 65 for char in text.upper()]
    encrypted_text = ""

    for i in range(0, len(text_numeric), 2):
        block = np.array(text_numeric[i:i + 2])
        encrypted_block = np.dot(key_matrix, block) % modulus
        encrypted_text += chr(encrypted_block[0] + 65) + chr(encrypted_block[1] + 65)

    return encrypted_text

def decrypt_hill(text, key):
    modulus = 26
    key_matrix = create_hill_key_matrix(key)
    inv_key_matrix = matrix_inverse(key_matrix, modulus)

    text_numeric = [ord(char) - 65 for char in text.upper()]
    decrypted_text = ""

    for i in range(0, len(text_numeric), 2):
        block = np.array(text_numeric[i:i + 2])
        decrypted_block = np.dot(inv_key_matrix, block) % modulus
        decrypted_text += chr(int(decrypted_block[0]) + 65) + chr(int(decrypted_block[1]) + 65)

    return decrypted_text

def encrypt_text():
    text = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    if key and text:
        ciphertext = encrypt_hill(text, key)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, ciphertext)
    else:
        messagebox.showwarning("Input Error", "Please enter both text and a key.")

def decrypt_text():
    text = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    if key and text:
        plaintext = decrypt_hill(text, key)
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
root.title("Hill Cipher")

# Create input and output text boxes
text_input = tk.Text(root, wrap=tk.WORD, width=50, height=10)
text_input.pack(pady=10)
result_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
result_text.pack(pady=10)

# Create key input and buttons
key_label = tk.Label(root, text="Enter Key (4 letters):")
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
