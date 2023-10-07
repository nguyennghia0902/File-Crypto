import os, json, re
import tkinter as tk
from tkinter import messagebox, filedialog
#pip install pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
import hashlib


salt_len = 16
def hash_password(password):
    salt = os.urandom(salt_len)
    hashed_password = hashlib.sha256(password.encode()).digest() + salt
    return hashed_password.hex()
def get_digest(password_hex):
    password_digest = bytes.fromhex(password_hex)
    return password_digest[:len(password_digest) - salt_len]
def validate_password(input, from_dir):
    hashed_password = hashlib.sha256(input.encode()).digest()
    from_dir = get_digest(from_dir)
    if hashed_password == from_dir:
        return True
    return False

def forget_old_widgets(frame: tk.Frame):
    if frame.children:
        for name, widget in list(frame.children.items()):
            if name != 'loginframe':
                widget.destroy()

def read_size_bs_bytes(size, data):
    bs = AES.block_size
    chunk_size = size * bs
    offset = 0
    while offset < len(data):
        chunk = data[offset:offset + chunk_size]
        offset += chunk_size
        yield chunk

def encrypt_file(file_in, password): 
    file = open(file_in, 'rb')
    data = file.read()
    file.close()

    name = str(file_in)
    name += ".enc"
    os.rename(file_in, name)

    file = open(name, 'wb')
    bs = AES.block_size 
    pass_hashed = hash_password(password)
    Ksession = get_digest(pass_hashed)  #os.urandom(bs)
    cipher = AES.new(Ksession, AES.MODE_CBC)
    finished = False
    
    file.write(cipher.iv)

    file.write(bytes(pass_hashed, 'utf-8'))

    while not finished:
        for chunk in read_size_bs_bytes(1024, data):
            if len(chunk) == 0 or len(chunk) % bs != 0:   
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += str.encode(padding_length * chr(padding_length))
                finished = True
            file.write(cipher.encrypt(chunk))   
        pass         
    file.close()
    return True
    
def decrypt_file(file_in, passinput):  
    file = open(file_in, 'rb')
    file_name = file_in.split('/')[-1]
    name = file_name
    addr = file_in.split('/')[:-1]
    file_out = '/'.join(addr)
    if '.' in file_name:
        full = file_name.split('.')
        name = full[0]
        exte = full[-1]
    if exte == "enc":    
        filename = str(file_in)
        filename = filename[:-4]
        print(filename)
        bs = AES.block_size 
        iv = file.read(bs)
        check = hash_password(passinput)
        passhase = file.read(len(check))
        data = file.read()
        file.close()
        os.rename(file_in, filename)
    else:
        messagebox.showerror(title='LỖI', message='Không phải file mã hóa!\nVui lòng chọn lại!')
        return False
    file = open(filename, 'wb+')
    pass_hashed = passhase[:len(check)].decode()
    if validate_password(passinput, pass_hashed):
      key = get_digest(pass_hashed)
      cipher = AES.new(key, AES.MODE_CBC, iv)
      next_chunk = ''
      finished = False
      offset = 0
      chunk_size = 1024 * bs
      while not finished:
          chunk, next_chunk = next_chunk, cipher.decrypt(data[offset:offset + chunk_size])
          offset += chunk_size
          if len(next_chunk) == 0:
            padding_length = chunk[-1]
            chunk = chunk[: - padding_length]  # type: ignore
            finished = True 
          file.write(bytes(x for x in chunk))   # type: ignore
      return True
    messagebox.showerror(title='LỖI', message='Sai  Mật khẩu!\nVui lòng nhập lại!')
    file.close()
    return False                 
    
    