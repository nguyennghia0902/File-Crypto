import tkinter as tk
from components.page import *

window_height = 400
window_width = 600


def decrypt_dynamic_password(s):
    offset = ord('A')
    t = s[0]
    for i in range(len(s))[1:]:
        cur = ord(s[i]) - offset
        last = ord(t[-1]) - offset
        c = chr((cur + last + 1) % 26 + offset)
        t += c
    return t

def generate_dynamic_password():
    nw = ''
    for i in range(8):
        n = random.randint(65,90)
        nw += chr(n)
    bv = decrypt_dynamic_password(nw)
    return nw, bv

def login(mainframe: tk.Frame):
        loginframe = tk.Frame(
            mainframe,
            name='loginframe',
            width=window_width,
            height=window_height
        )

        try:
            for frame in mainframe.children.values():
                frame.forget()
        except:
            mainframe.children['loginframe'].pack(fill="both", expand=1)

        loginframe = mainframe.children['loginframe']
        login_contentframe = tk.Frame(loginframe, padx=130, pady=10)
        
        login_label = tk.Label(
            login_contentframe,
            text='USER LOGIN',
            font=('', 24, 'bold'),
            padx=5,
            pady=20,
            width=10
        )
        nw, bv = generate_dynamic_password()
        password_label = tk.Label(
            login_contentframe,
            text='Password:\n'+ '"' + nw + '"', 
            font=('Verdana',14)
        )
        print("Mật khẩu động (chưa giải mã): ", nw)

        password_entry = tk.Entry(login_contentframe, font=('Verdana',14), show='*')

        login_button = tk.Button(
            login_contentframe,
            text="Login",
            font=('Verdana',10),
            bg='#2980b9',
            fg='#fff',
            padx=10,
            pady=10,
            width=8
        )
        mainframe.pack(fill='both', expand=1)
        loginframe.pack(fill='both', expand=1)
        login_contentframe.pack(fill='both', expand=1)

        login_label.grid(row=0, column=0, columnspan=3)

        password_label.grid(row=2, column=0, pady=10)
        password_entry.grid(row=2, column=1)
        
            
        def validate_login(): #handle click
            success = False
            password = password_entry.get().strip()
            
            if (password == bv):
                print("Mật khẩu động (đã giải mã): ", bv)
                ok = page(mainframe)
                success = True

            if success == False:
                messagebox.showerror(title='LỖI', message='Sai  Mật khẩu!\nVui lòng nhập lại!')
                login(mainframe)
            
        login_button.grid(row=3, column=0, columnspan=2, pady=30)
        login_button.bind("<Return>", (lambda e: validate_login))
        login_button['command'] = validate_login