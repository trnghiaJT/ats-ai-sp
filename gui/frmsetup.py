import tkinter as tk
from gui.frmgetapikey import create_getapikey_frame
import gui.config as config
from gui.theme import DARK_THEME, LIGHT_THEME
def create_datasetup_frame(root):
    if config.current_theme == "Dark":
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME
    datasetup_frame = tk.Frame(root, bg=current_theme['backgroundtheme'])
    datasetup_frame.pack(side='top', fill='both', expand=True) 
    api_key_frame = create_getapikey_frame(datasetup_frame, root)
    api_key_frame.place(x=385, y=76, width=515, height=580)
    return datasetup_frame
