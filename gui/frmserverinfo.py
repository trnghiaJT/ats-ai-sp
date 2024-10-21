import tkinter as tk
from module.connect_server import connect_to_database
import gui.config as config
from gui.theme import DARK_THEME, LIGHT_THEME
def create_serverinfo_frame(datasetup_frame, root,api_frame_key,options):
    if config.current_theme == "Dark":
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME
# Information frame
    info_frame = tk.Frame(datasetup_frame, bg=current_theme['background'])
    info_frame.place(x=400, y=0, width=515, height=580)
    for row in range(6):
        info_frame.grid_rowconfigure(row, weight=1)
    for col in range(6):
        info_frame.grid_columnconfigure(col, weight=1)
    # for row in range(6):
    #     for col in range(6):
    #         label = tk.Label(info_frame, text=f"Row {row} Col {col}", bg='lightpink', fg="white")
    #         label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    def create_label_frame(root, text):
        frame = tk.LabelFrame(root, text=text, fg=current_theme['foreground'], bg=current_theme['background'],
                            font=('Arial', 14), relief='flat')
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame
    def create_entry(root):
        entry = tk.Entry(root, font=('Times new roman', 13),fg=current_theme['entry_fg'],bg=current_theme['entry_bg'], bd=0,highlightbackground=current_theme['highlightbackground'],highlightthickness=1,)
        entry.grid(row=0, column=0, padx=5, pady=10, sticky="new")
        return entry
    # input dbname
    dbname_frame = create_label_frame(info_frame, "Database:")
    dbname_frame.grid(row=0, column=1, rowspan=1, columnspan=4, sticky='nsew', padx=5, pady=5)
    dbname_entry = create_entry(dbname_frame)
    # input dbuser
    dbuser_frame = create_label_frame(info_frame, "Database User:")
    dbuser_frame.grid(row=1, column=1, rowspan=1, columnspan=4, sticky='nsew', padx=5, pady=5)
    dbuser_entry = create_entry(dbuser_frame)
    # input dbpassword
    dbpassword_frame = create_label_frame(info_frame, "Database Password:")
    dbpassword_frame.grid(row=2, column=1, rowspan=1, columnspan=4, sticky='nsew', padx=5, pady=5)
    dbpassword_entry = create_entry(dbpassword_frame)
    dbpassword_entry.config(show='●')
    # checkbox to show/hide password
    def show_password():
        if checkbox_pw_var.get() == 1:
            dbpassword_entry.config(show='')
        else:
            dbpassword_entry.config(show='●')
    checkbox_pw_var = tk.IntVar(value=0)
    checkbox_pw = tk.Checkbutton(info_frame, text="Show password", background=current_theme['background'], font=('MS Sans Serif', 13),
                              fg=current_theme['foreground'], variable=checkbox_pw_var,activebackground=current_theme['background'], selectcolor=current_theme['background'], command=show_password)
    checkbox_pw.place(x=285, y=261)
    checkbox_pw.bind('<Return>', lambda event: checkbox_pw.invoke())
    # input dbhost
    dbhost_frame = create_label_frame(info_frame, "Database Host:")
    dbhost_frame.grid(row=3, column=1, rowspan=1, columnspan=4, sticky='nsew', padx=5, pady=5)
    dbhost_entry = create_entry(dbhost_frame)
    # input dbport
    dbport_frame = create_label_frame(info_frame, "Database Port:")
    for row in range(1):
        dbport_frame.grid_rowconfigure(row, weight=1)
    for col in range(2):
        dbport_frame.grid_columnconfigure(col, weight=1)
    dbport_frame.grid(row=4, column=1, rowspan=1, columnspan=4, sticky='nsew', padx=5, pady=5)
    # Default port is 5432
    dbport_entry = tk.Entry(dbport_frame, font=('Times new roman', 13),fg=current_theme['entry_fg'],highlightbackground=current_theme['highlightbackground'],highlightthickness=1, bd=0)
    dbport_entry.insert(0, '5432')
    dbport_entry.config(state='disabled')
    def toggle_port_entry():
        if checkbox_var.get() == 1:
            dbport_entry.config(state='normal')
        else:
            dbport_entry.config(state='disabled')
            dbport_entry.delete(0, tk.END)
            dbport_entry.insert(0, '5432')
    dbport_entry.grid(row=0, column=0, padx=5, pady=10, sticky="new")
    # Checkbox to enable/disable the port field
    checkbox_var = tk.IntVar(value=0)
    checkbox = tk.Checkbutton(dbport_frame, text="Change port", background=current_theme['background'], font=('MS Sans Serif', 13),
                              fg=current_theme['foreground'], variable=checkbox_var,activebackground=current_theme['background'], selectcolor=current_theme['background'], command=toggle_port_entry)
    checkbox.grid(row=0, column=1, padx=5, pady=10, sticky="new")
    checkbox.bind('<Return>', lambda event: checkbox.invoke())
    # btn connect
    btn_frame = tk.LabelFrame(info_frame, text="", fg='#fdfdfd', bg=current_theme['background'],
                            font=('MS Sans Serif', 13), relief='flat')
    btn_frame.grid(row=5, column=1, rowspan=1, columnspan=4, sticky='nsew', padx=5, pady=5)
    for col in range(6):
        btn_frame.grid_columnconfigure(col, weight=1)
    for row in range(1):
        btn_frame.grid_rowconfigure(row, weight=1)
    btn_frame.grid_propagate(False)
    btn_connect_frame = tk.Frame(btn_frame, bg=current_theme['boder_button'],bd=2)
    btn_connect_frame.grid(row=0, column=5, rowspan=1, columnspan=1, sticky='new', padx=5, pady=10)
    def create_button_func(parent, text, command):
        button = tk.Button(parent, 
                           text=text, 
                           width=10, 
                           height=2, 
                           bg=current_theme['button_bg'], 
                           fg=current_theme['foreground'], 
                           bd=0, 
                           font=('Arial', 13), 
                           relief='flat',
                           command=command)
        return button
    btn_connect = create_button_func(btn_connect_frame, "Connect", lambda: connect_to_database(datasetup_frame,root,dbname_entry.get(),dbuser_entry.get(),dbpassword_entry.get(),dbhost_entry.get(),dbport_entry.get()))
    btn_connect.pack(fill='both', expand=True)
    btn_connect.bind('<Return>',lambda event:btn_connect.invoke() )
    btn_back_frame = tk.Frame(btn_frame, bg=current_theme['boder_button'],bd=2)
    btn_back_frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='new', padx=5, pady=10)
    btn_back = create_button_func(btn_back_frame, "Back", command= lambda: hide_frame(api_frame_key))
    btn_back.pack(fill='both', expand=True)
    btn_back.bind('<Return>',lambda event: btn_back.invoke())
    def hide_frame(api_frame_key):
        info_frame.place_forget()
        options.place(x=10,y=10)
        api_frame_key.place(x=385, y=76, width=515, height=580)
    return info_frame