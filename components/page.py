import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry

import os, json
from datetime import datetime

from components.utils import *

window_height = 400
window_width = 600


def page(mainframe: tk.Frame):

    mainframe.children['loginframe'].forget()
    user_page_frame = tk.Frame(
        mainframe,
        name='userpage',
        width=window_width,
        height=window_height
    )

    user_page_frame.pack(fill='both', expand=1)

    user_page_header_frame = tk.Frame(
        user_page_frame,
        name='header_frame',
        padx = 70,
        highlightthickness=3,
        highlightbackground='black'
    )
    
    
    user_page_header_frame.pack(fill='both')
    
    # Menu panel
    user_page_content_frame_left = tk.Frame(
        user_page_frame,
        name='menu_content_frame',
        width=50
    )
    func_label = tk.Label(
        user_page_content_frame_left,
        text='MENU',
        font=('Verdana',18,'bold')
    )
    
    encrypt_send_button = tk.Button(
        user_page_content_frame_left,
        text='Chọn và mã hoá tập tin',
        width=25
    )
    decrypt_receive_button = tk.Button(
        user_page_content_frame_left,
        text='Giải mã tập tin',
        width=25
    )
    

    user_page_content_frame_left.pack(fill='both',side = 'left', padx=20, pady=10)

    func_label.grid(row=0, column=0, columnspan=3)
    encrypt_send_button.grid(row=3, column=0, pady=5)
    decrypt_receive_button.grid(row=4, column=0, pady=5)
    

    # Content panel
    user_page_content_frame_right = tk.Frame(
        user_page_frame,
        name='content_frame',
        highlightthickness=2,
        bg='white',
        highlightbackground='black',
        width=360,
        height=290
    )
    user_page_content_frame_right.pack(pady=10, side='left', ipady=40)
    user_page_content_frame_right.grid_propagate(False)
    user_page_content_frame_right.pack_propagate(False)
    
    def encrypt_send_file():

        user_dir = 'data/' 

        forget_old_widgets(user_page_content_frame_right)

        file_frame = tk.Frame(
            user_page_content_frame_right,
            name='file_pick_frame',
            bg='white',
            width=170,
            height=290
        )

        file_frame.pack(side='left', fill='both')
        file_frame.grid_propagate(False)

        file_choose_label = tk.Label(
            file_frame,
            text='Chọn file cần mã hoá: ',
            font=('Verdana',8),
        )
        file_name_display = tk.Label(
            file_frame,
            wraplength=150,
            bg='white'
        )
        file_name = tk.StringVar(file_frame)
        def get_file():
            get_file_name = filedialog.askopenfilename(
                title='Chọn file',
                initialdir=user_dir
            )
            file_name.set(get_file_name)
            file_name_display['textvariable']=file_name

        file_choose_button = tk.Button(
            file_frame,
            text='Chọn file',
            command=get_file,
            anchor='w'
        )

        file_choose_label.grid(row=0, column=0, pady=5, sticky='w')
        file_choose_button.grid(row=1, column=0, pady=5, sticky='w')
        file_name_display.grid(row=2, column=0, columnspan=1, pady=5, sticky='w')

        user_frame = tk.Frame(
            user_page_content_frame_right,
            name='user_pick_frame',
            bg='white',
            width=190,
            height=290
        )

        user_frame.pack(side='left')
        user_frame.grid_propagate(False)

        user_pick_label = tk.Label(
            user_frame,
            text='Nhập email cần gửi:',
            font=('Verdana',8)
        )
        user_pick_entry = tk.Entry(
            user_frame,
            width=25,
            font=('Verdana',8)
        )
        """
        def submit():
            email = user_pick_entry.get().strip()
            if not get_user(email):
                messagebox.showerror(
                    title='Lỗi',
                    message='Không tồn tại người dùng này!'
                
                )
            else:
                if encrypt_file(file_name.get(), email):
                    messagebox.showinfo(title='CHÚC MỪNG', message='Mã hoá và gửi thành công')
                else: messagebox.showerror(title='LỖI', message='Mã hoá không thành công')
        submit_button = tk.Button(
            user_frame,
            text='Xác nhận',
            width=10,
            command=submit
        )
        """
        user_pick_label.grid(row=0, column=0, pady=5)
        user_pick_entry.grid(row=1, column=0, pady=5, sticky='w')
        #submit_button.grid(row=2,column=0, pady=5)

    def decrypt_receive():
        user_dir = 'data/'

        forget_old_widgets(user_page_content_frame_right)
        if user_page_content_frame_right.children:
            for i in user_page_content_frame_right.children.values():
                print(i)

        file_choose_label = tk.Label(
            user_page_content_frame_right,
            text='Chọn file cần giải mã: ',
            font=('Verdana',8),
        )
        file_name_display = tk.Label(
            user_page_content_frame_right,
            wraplength=150,
            bg='white'
        )

        file_name = tk.StringVar(user_page_content_frame_right)

        def get_file():
            get_file_name = filedialog.askopenfilename(
                title='Chọn file',
                initialdir=user_dir
            )
            file_name.set(get_file_name)
            file_name_display['textvariable']=file_name

        file_choose_button = tk.Button(
            user_page_content_frame_right,
            text='Chọn file',
            command=get_file,
            anchor='w'
        )
        """
        def submit():
            if decrypt_file(file_name.get(), user.email):
                messagebox.showinfo(title='CHÚC MỪNG', message='Giải mã thành công')
            else: messagebox.showerror(title='LỖI', message='Giải mã không thành công')
        
        submit_button = tk.Button(
            user_page_content_frame_right,
            text='Xác nhận',
            width=10,
            command=submit
        )
        """
        file_choose_label.grid(row=0, column=0, pady=5, sticky='w')
        file_choose_button.grid(row=1, column=0, pady=5, sticky='w')
        file_name_display.grid(row=2, column=0, columnspan=1, pady=5, sticky='w')
        #submit_button.grid(row=3,column=0, pady=5)
    encrypt_send_button['command']=encrypt_send_file
    decrypt_receive_button['command']=decrypt_receive