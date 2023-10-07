import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import os, json
from datetime import datetime
from components.login import *


def main():
    root = tk.Tk()
    
    ### FRAME ###
    window_height = 400
    window_width = 600

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws-window_width)/2
    y = (hs-window_height)/2

    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
    root.resizable(False, False)
    
    root.title('Assignment 01.03')
    ###

    mainframe = tk.Frame(root, name='mainframe', width=window_width, height=window_height)

    ### MAIN ###



    log = login(mainframe)

    root.mainloop()

if __name__ == '__main__':
    main()