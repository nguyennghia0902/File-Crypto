import os, json, re, string, random
import tkinter as tk
from tkinter import messagebox, filedialog
#pip install pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
import hashlib


def hash_password(password, salt_len):
    salt = os.urandom(salt_len)
    hashed_password = hashlib.sha256(password.encode()).digest() + salt
    return hashed_password.hex()
def get_digest(password_hex, salt_len):
    password_digest = bytes.fromhex(password_hex)
    return password_digest[:len(password_digest) - salt_len]
def validate_password(input, from_dir, salt_len):
    hashed_password = hashlib.sha256(input.encode()).digest()
    from_dir = get_digest(from_dir, salt_len)
    if hashed_password == from_dir:
        return True
    return False

def forget_old_widgets(frame: tk.Frame):
    if frame.children:
        for name, widget in list(frame.children.items()):
            if name != 'loginframe':
                widget.destroy()

def encrypt_file(file_in, password):        
    fileIn = open(file_in, 'rb')
    file_name = file_in.split('/')[-1]
    name = file_name
    addr = file_in.split('/')[:-1]
    file_out = '/'.join(addr)
    if '.' in file_name:
        name = file_name.split('.')[0]
    file_name = file_name.replace(name, name + '_encrypted')
    file_out += '/' + file_name
    fileOut = open(file_out, 'wb+')
    bs = AES.block_size 
    salt_len = random.randint(0, 500000)
    pass_hashed = hash_password(password, salt_len)
    Ksession = get_digest(pass_hashed, salt_len)#os.urandom(bs)
    cipher = AES.new(Ksession, AES.MODE_CBC)
    finished = False

    fileOut.write(cipher.iv)
    fileOut.write(bytes(str(salt_len), 'utf-8'))
    fileOut.write(bytes(random.choice(string.ascii_lowercase), 'utf-8'))
    # fileOut.write(bytes('a', 'utf-8'))
    fileOut.write(bytes(pass_hashed, 'utf-8'))

    while not finished:
        chunk = fileIn.read(1024 * bs) 
        if len(chunk) == 0 or len(chunk) % bs != 0:   
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += str.encode(padding_length * chr(padding_length))
            finished = True
        fileOut.write(cipher.encrypt(chunk))                 
    
    fileIn.close()
    fileOut.close()
    return True

def decrypt_file(file_in, passinput):                     #5.4
    fileIn = open(file_in, 'rb')
    matches = re.findall(r'/\w+',file_in)
    file_name = matches[-1]
    file_name = file_name[1:]
    if file_name.find('_encrypted') != -1:
        file_name.replace('_encrypted','')
    file_out = file_in.replace(file_name, file_name + '_decrypted')
    fileOut = open(file_out, 'wb+')
    bs = AES.block_size #16 bytes
    
    iv = fileIn.read(bs)
    # salt_test = fileIn.read(1).decode() + fileIn.read(1).decode() + fileIn.read(1).decode()
    # random_char = fileIn.read(1).decode()
    next_char = fileIn.read(1)
    salt_len = str('')
    while(next_char.decode() not in string.ascii_lowercase):
        salt_len = salt_len + next_char.decode()
        next_char = fileIn.read(1)

    print('random_char = ' + next_char.decode())
    print('salt_test = ' + salt_len)
    # salt_len = 200
    check = hash_password(passinput, int(salt_len))
    cont = fileIn.read(len(check))
    pass_hashed = cont.decode()

    if validate_password(passinput, pass_hashed, int(salt_len)):
      key = get_digest(pass_hashed, int(salt_len))
      cipher = AES.new(key, AES.MODE_CBC, iv)
      next_chunk = ''
      finished = False
      while not finished:
          chunk, next_chunk = next_chunk, cipher.decrypt(fileIn.read(1024 * bs))
          if len(next_chunk) == 0:
            padding_length = chunk[-1]
            chunk = chunk[: - padding_length]  # type: ignore
            finished = True 
          fileOut.write(bytes(x for x in chunk))   # type: ignore
      return True
    messagebox.showerror(title='LỖI', message='Sai  Mật khẩu!\nVui lòng nhập lại!')
    return False
    