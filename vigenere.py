import tkinter as tk
from tkinter import filedialog, messagebox

def vigenere_cipher(text, key, mode):
    result = ""
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index]) - 65 if mode == 'encrypt' else 65 - ord(key[key_index])
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) + shift - 97) % 26 + 97)
            key_index = (key_index + 1) % len(key)
        else:
            result += char

    return result

def encrypt_text():
    text = text_input.get("1.0", tk.END)
    key = key_input.get()
    ciphertext = vigenere_cipher(text, key, "encrypt")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, ciphertext)

def decrypt_text():
    text = text_input.get("1.0", tk.END)
    key = key_input.get()
    plaintext = vigenere_cipher(text, key, "decrypt")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, plaintext)

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text = file.read()

            text_input.delete(1.0, tk.END)
            text_input.insert(tk.END, text)


# Create the main window
root = tk.Tk()
root.title("Vigenère Cipher")

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