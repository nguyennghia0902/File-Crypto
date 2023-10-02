import tkinter as tk
from components.page import *

window_height = 400
window_width = 600

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
        password_label = tk.Label(
            login_contentframe,
            text='Password:', 
            font=('Verdana',14)
        )

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
            check = "123"
            if (password == check):
                ok = page(mainframe)
                success = True

            if success == False:
                messagebox.showerror(title='LỖI', message='Sai  Mật khẩu!\nVui lòng nhập lại!')
                login(mainframe)
            
        login_button.grid(row=3, column=0, columnspan=2, pady=30)
        login_button.bind("<Return>", (lambda e: validate_login))
        login_button['command'] = validate_login