import tkinter as tk
from tkinter import filedialog
import os.path
import random
import string

abc = string.ascii_lowercase
stringlength = 26
key_to_decode = ''.join(random.sample(abc,stringlength))

print("The key to decode: ", key_to_decode)

root = tk.Tk()
root.withdraw()

def encoder():

    current_user = os.path.expanduser('~')
    path_to_a_file = filedialog.askopenfilename()
    where_to_save = current_user + "\\Desktop"

    new_file_name = input("Please Enter The New File Name: ")
    new_file_type = input("Ente the File Type: ")
    path_to_new_file = os.path.join(where_to_save, new_file_name + new_file_type)
    print(path_to_new_file)

    file_to_encode = open(path_to_a_file, "r")
    clear_string = file_to_encode.read().lower()

    table = str.maketrans(
            "abcdefghijklmnopqrstuvwxyz", key_to_decode
        )

    result = clear_string.translate(table)
    file_to_encode.close()
    print(result)
    encode_file = open(path_to_new_file, "w")
    encode_file.write(result)
    encode_file.close()
    encode_file = open(path_to_new_file, "r")
    encode_string = encode_file.read()
    print(encode_string)


encoder()
