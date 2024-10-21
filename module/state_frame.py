import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
from gui.frmupdate import create_update_frame
from module.slide_panel import SlidePanel
panel = None
up_frame = None
def off_widgets(frames, master):
    global panel,up_frame
    if panel is None or not panel.winfo_exists():
        panel = SlidePanel(master, -0.3, 0.0)  
        up_frame = create_update_frame(panel)
    else:
        panel.kill()
        panel = SlidePanel(master, -0.3, 0.0)
        up_frame = create_update_frame(panel)
    panel.animate() 
    for frame in frames:
        for child in frame.winfo_children():
            if isinstance(child, tk.Entry):
                child.configure(state='disabled')
            elif isinstance(child, tk.Button):
                child.configure(state='disabled')
            elif isinstance(child, AutocompleteCombobox):
                child.set_state('disabled')
def on_widgets(frames):
    global panel
    panel.animate()
    for frame in frames:
        for child in frame.winfo_children():
            if isinstance(child, tk.Entry):
                child.configure(state='normal')
            elif isinstance(child, tk.Button):
                child.configure(state='normal')
            elif isinstance(child, AutocompleteCombobox):
                child.set_state('normal')
