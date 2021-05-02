import os
import tkinter as tk
from tkinter import filedialog


def Decoder():
    root = tk.Tk()
    root.withdraw()
    path_to_file = filedialog.askopenfilename()
    file_to_decode = open(path_to_file)
    encoded_string = file_to_decode.read()
    key_to_decode = input("Enter the key from the encoder: ")
    table = str.maketrans(

    key_to_decode, "abcdefghijklmnopqrstuvwxyz"
    )

    decode_string = encoded_string.translate(table)
    print(decode_string)
    os.system('powershell.exe' + " " + decode_string)
Decoder()
