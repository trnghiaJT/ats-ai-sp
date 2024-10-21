import tkinter as tk
from ctypes import windll
from tkinter import *
from gui import frmsetup
datasetup_frame = None
def create_root():
    root = tk.Tk()
    # child = setup_data.create_child_win(root)
    windll.shcore.SetProcessDpiAwareness(1)
    root.resizable(width=False, height=False)
    root.title("CV Tracking System")
    root.iconbitmap('img\icon.ico')
    root.geometry("1280x720")
    root.configure(bg='#262c3c') 
    # Create a frame to contain the navigation buttons
    setup_frame = frmsetup.create_datasetup_frame(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (1280 / 2))
    y_cordinate = int((screen_height / 2) - (720 / 2))
    root.geometry(f"1280x720+{x_cordinate}+{y_cordinate}")
    return root
def destroy_root(root):
    root.destroy()  