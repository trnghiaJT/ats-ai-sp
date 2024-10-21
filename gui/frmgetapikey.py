import tkinter as tk
from module.animation import sliding
from gui.frmserverinfo import create_serverinfo_frame
import webbrowser
import tkinter.font as tkFont 
from tkinter import messagebox
from tkinter.ttk import OptionMenu
import tkinter.ttk as ttk
import gui.config as config
from gui.theme import * 
api_key = None
def create_getapikey_frame(datasetup_frame, root):
    global api_key
    if config.current_theme == "Dark":
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME
    api_key_frame = tk.Frame(datasetup_frame, bg=current_theme['background'])
    for row in range(6):
        api_key_frame.grid_rowconfigure(row, weight=1)
    for col in range(6):
        api_key_frame.grid_columnconfigure(col, weight=1)
    api_key_frame.grid_propagate(False)
    valueslist = ['Dark', 'Light']
    selected_value = tk.StringVar(root)
    style = ttk.Style()
    style.configure("TMenubutton", relief=tk.FLAT, bd=0,font=('MS Sans Serif', 12), highlightthickness=1,
        arrowcolor="#909090", foreground=current_theme['foreground'], background=current_theme['background'])
    selected_value.set('config.current_theme')
    default = config.current_theme
    option_select = OptionMenu(root,selected_value ,default, *valueslist, style='TMenubutton')
    option_select.place(x=10, y=10)
    def blink_text():
        current_text = label_welcome.cget("text")
        base_text = "API Key and Server Configuration"
        if current_text.endswith("..."):
            label_welcome.config(text=base_text)
        else:
            label_welcome.config(text=current_text + ".")
        label_welcome.after(500, blink_text)
    label_welcome = tk.Label(api_key_frame, 
                             text="API Key and Server Configuration",
                             anchor='w', 
                             bg=current_theme['background'], 
                             fg=current_theme['foreground'], 
                             font=('Berlin Sans FB Demi', 15, 'bold'),
                             width=35,
                             wraplength=300,
                             justify='left')
    label_welcome.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky="nsw")
    label_welcome.lift()
    blink_text()
    api_frame = tk.LabelFrame(api_key_frame,
                              text='Gemini API Key', 
                              bg=current_theme['background'], 
                              fg=current_theme['foreground'], 
                              font=('Arial', 14,'bold'), 
                              relief='flat')
    api_frame.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="nsew")
    api_frame.grid_propagate(False)
    api_frame.grid_rowconfigure(0, weight=1)
    api_frame.grid_columnconfigure(0, weight=1)
    api_entry = tk.Entry(api_frame,  
                         fg="#222222", 
                         font=('Times New Roman', 14), 
                         insertbackground='black',
                         highlightbackground=current_theme['highlightbackground'],
                         highlightthickness=1,
                         relief='flat',
                         bd=0)
    api_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    urltutorial = "https://www.youtube.com/watch?v=03Hcs6PnWU4&ab_channel=CoolPlugins"
    font = tkFont.Font(family='Arial', size=13, slant='italic',underline=1)
    def open_url():
        webbrowser.open_new(urltutorial)
    url_label = tk.Label(api_key_frame, 
                         text="Click here to watch the tutorial", 
                         bg=current_theme['background'], 
                         fg=current_theme['foreground'], 
                         font=font, 
                         cursor='hand2')
    url_label.bind("<Button-1>", lambda e: open_url())
    url_label.grid(row=3, column=1, columnspan=4, padx=5, pady=5, sticky="ne")
    def check_api_connect():
        global api_key
        from module.gen_sum import test_connect_api
        api_key = api_entry.get()
        # print(api_key)
        if test_connect_api(api_key):
            sliding(api_key_frame, create_serverinfo_frame(datasetup_frame, root,api_key_frame,option_select))
            option_select.place_forget()
        else:
            messagebox.showerror("Error", "Invalid API Key")
    btn_sliding_frame = tk.Frame(api_key_frame, bg=current_theme['boder_button'], bd=2)
    btn_sliding_frame.grid(row=5, column=2, rowspan=1, columnspan=2, sticky='new', padx=5, pady=10)
    btn_sliding = tk.Button(btn_sliding_frame, 
                            text="Next", 
                            font=('Arial', 13), 
                            bg=current_theme['button_bg'], 
                            fg=current_theme['foreground'],
                            relief='flat',
                            command=lambda: check_api_connect())
    btn_sliding.pack(fill='both', expand=True)
    btn_sliding.bind('<Return>',lambda event: check_api_connect())
    def switch_theme(*args):
        config.current_theme = selected_value.get()
        if config.current_theme == 'Light':
            current_theme = LIGHT_THEME
            tree_combo_light()
        else:
            current_theme = DARK_THEME
            tree_combo_dark()
        api_key_frame.config(bg=current_theme['background'])
        style.configure("TMenubutton", relief=tk.FLAT, bd=0,font=('MS Sans Serif', 12), highlightthickness=1,
        arrowcolor="#909090", foreground=current_theme['foreground'], background=current_theme['background'])
        datasetup_frame.config(bg=current_theme['backgroundtheme'])
        label_welcome.config(bg=current_theme['background'],fg=current_theme['foreground'])
        api_frame.config(bg=current_theme['background'],fg=current_theme['foreground'])
        api_entry.config(bg=current_theme['entry_bg'],fg=current_theme['entry_fg'], highlightbackground=current_theme['highlightbackground'])
        url_label.config(bg=current_theme['background'],fg=current_theme['foreground'])
        btn_sliding_frame.config(bg=current_theme['boder_button'])
        btn_sliding.config(bg=current_theme['button_bg'],fg = current_theme['foreground'])
    selected_value.trace('w', switch_theme)
    switch_theme(default)
    return api_key_frame