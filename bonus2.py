from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from binascii import unhexlify
from Crypto.Cipher import PKCS1_OAEP

source_encrypted = 'HiWV9rm4zNWV7ejdIj1baz1cbTT7hCxY+s3nAjJ8dqiZyhW6s1xLAmONd1dgS9De01Ky/uXVFM2BuCFxjB0rShTezGOpVPv/Dz5NSBvxoGagA/A83AxRL99erdxclxjumzglbmAJ5A1lo93YGAbOp8o0HT6gwYB9RuRem41sAMJAYNtHa4x13aLKnEhhD/QUJQXya3242gKdT2FPWjCGTc5R4bKZ57cUg6gJQ0SXSirtarlpD81DuDH/PElXaTL7'

iv = "7bde5a0f3f39fd658efc45de143cbc94"
iv = unhexlify(iv)

cipher = AES.new(b'MZuogwKqb6un6uLQ4D4L4ORRHPXfuRCQ', AES.MODE_CBC, iv)
decrypted_source  = unpad(cipher.decrypt(b64decode(source_encrypted)), AES.block_size).decode('utf-8')

exec(decrypted_source)

import string
import random

def generate_encrypted_data(plaintext):
    data = plaintext.encode('utf-8')

    # Generate a random encryption key
    key_string = ''.join(random.choices(string.ascii_letters+ string.digits, k = 32))
    key = key_string.encode('utf-8')
    
    #Padding and ecrypting the data
    iv = unhexlify("7bde5a0f3f39fd658efc45de143cbc94")
    encrypted_data = b64encode((AES.new(key, AES.MODE_CBC, iv)).encrypt(pad(data, AES.block_size))).decode('utf-8')

    return (encrypted_data, key)

import io
import os

def replace_function(plaintext):
    # Placing the source code path 
    file_path = "/Users/MEHER BABA/Desktop/bonus2.py"
    
    # Opening and reading lines in the file
    with open(file_path, "r") as file:
        file_in = io.StringIO(file.read())
    file_in_lines = file_in.readlines()
    data_list = generate_encrypted_data(plaintext)
    
    # Assigning the ecrypted data and key to the lines in the file
    file_in_lines[6] = f"source_encrypted = '{data_list[0]}'\n"
    file_in_lines[11] = f"cipher = AES.new({data_list[1]}, AES.MODE_CBC, iv)\n"
    
    #Writing the file
    with open(file_path, "w") as file:
        for line in file_in_lines:
            file.write(line)

    print("Lines replaced successfully.")
replace_function(decrypted_source)

