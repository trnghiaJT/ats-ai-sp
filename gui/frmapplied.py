import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox 
from data.DAO.applicantDAO import ApplicantDAO
from data.data_manager import DatabaseManager
from tkinter.ttk import Treeview, Scrollbar
from module.state_frame import *
from module.treeview_select import *
from gui.frmupdate import data
from module.apply_theme import apply_theme
Applicantdao = None
exp_frame = None
job_role_frame =None 
gpa_frame_from= None
gpa_frame_to = None 
boder_frame_delete = None 
boder_frame_update = None 
filter_frame = None
update_selected = False
def create_applied_frame(master):
    theme = apply_theme()
    global exp_frame, job_role_frame, gpa_frame_from, gpa_frame_to, boder_frame_delete, boder_frame_update, filter_frame
    dao = DatabaseManager().get_dao()
    data = dao.fetch_exp_and_job_role()
    applied_frame = tk.Frame(master, bg=theme['backgroundtheme'])
    for row in range(10):
        applied_frame.grid_rowconfigure(row, weight=1)
    for col in range(10):
        applied_frame.grid_columnconfigure(col, weight=1)
    applied_frame.grid_propagate(False)
    # for row in range(10):
    #     for col in range(10):
    #         label = tk.Label(applied_frame, text=f"Row {row} Col {col}", bg='lightpink', fg="white")
    #         label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    def create_label_frame(root, text):
        frame = tk.LabelFrame(root, text=text, fg=theme['foreground'], bg=theme['background'],
                            font=('MS Sans Serif', 13), relief='flat')
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame
    # Create a frame for the job role
    job_role_frame = create_label_frame(applied_frame, "Job Role")
    job_role_frame.grid(row=0, column=0,columnspan=3,  padx=5, pady=5, sticky="nsew")
    job_role_combobox = AutocompleteCombobox(job_role_frame, completevalues=[])
    job_role_combobox['values'] = data["job_roles"]
    job_role_combobox.grid(row=0, column=0, sticky="ew")
    # Create a frame for the experience
    exp_frame = create_label_frame(applied_frame, "Experience")
    exp_frame.grid(row=0, column=3, columnspan=3, padx=5, pady=5, sticky="nsew")
    exp_combobox = AutocompleteCombobox(exp_frame, completevalues=[])
    exp_combobox['values'] = data["exp_types"]
    exp_combobox.grid(row=0, column=0, sticky="ew")
    # Create a frame for the gpa
    def validate_numeric_input(char):
        if char.isdigit() or char == '.':  
            return True
        elif char == "":  
            return True
        else:
            return False
    gpa_frame = tk.Frame(applied_frame, bg=theme['background'])
    gpa_frame.grid(row=0, column=6, columnspan=3, padx=5, pady=5, sticky="nsew")
    gpa_frame.grid_propagate(False)
    gpa_frame.grid_rowconfigure(0, weight=1)
    for col in range(2):
        gpa_frame.grid_columnconfigure(col, weight=1)
    validate_cmd = gpa_frame.register(validate_numeric_input)
    gpa_frame_from = create_label_frame(gpa_frame, "From:")
    gpa_frame_from.grid(row=0, column=0, columnspan=1, padx=2, pady=2, sticky="nsew")
    gpa_frame_from.grid_propagate(False)
    gpa_frame_to = create_label_frame(gpa_frame, "To:")
    gpa_frame_to.grid(row=0, column=1, columnspan=1, padx=2, pady=2, sticky="nsew")
    gpa_frame_to.grid_propagate(False)
    gpa_entry_from = tk.Entry(gpa_frame_from, bg=theme['entry_dark'], 
                              fg=theme['entry_dark_fg'], font=('Arial', 13), 
                              insertbackground=theme['foreground'],highlightbackground=theme['highlightbackground'],
                              highlightthickness=1,relief='flat', validate="key", validatecommand=(validate_cmd, '%S'))
    gpa_entry_from.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    gpa_entry_to = tk.Entry(gpa_frame_to, bg=theme['entry_dark'], 
                            fg=theme['entry_dark_fg'], font=('Arial', 13), 
                            insertbackground=theme['foreground'],highlightbackground=theme['highlightbackground'],
                            highlightthickness=1,relief='flat', validate="key", validatecommand=(validate_cmd, '%S'))
    gpa_entry_to.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    # Create a frame for the filter button
    def create_boder_button(parent):
        boder_frame = tk.Frame(parent, bg=theme['boder_button'])
        return boder_frame
    filter_frame = create_boder_button(applied_frame)
    filter_frame.grid(row=0, column=9, columnspan=1, padx=5, pady=5, sticky="nsew")
    filter_frame.grid_propagate(False)
    filter_frame.grid_rowconfigure(0, weight=1)
    filter_frame.grid_columnconfigure(0, weight=1)
    filter_button = tk.Button(filter_frame, text="Filter", bg=theme['button_bg'], fg=theme['foreground'], font=('MS Sans Serif', 13), bd=0, activebackground=theme['button_select_bg'], activeforeground=theme['foreground'],command=lambda: filter_applied(Aplicantdao)) 
    filter_button.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
    # Button "Refresh"
    refesh_frame = create_boder_button(applied_frame)
    refesh_frame.grid(row=1, column=9, columnspan=1, padx=5, pady=5, sticky="nsew")
    refesh_frame.grid_propagate(False)
    refesh_frame.grid_rowconfigure(0, weight=1)
    refesh_frame.grid_columnconfigure(0, weight=1)
    refresh_button = tk.Button(refesh_frame, text="Refresh", bg=theme['button_bg'], fg=theme['foreground'], font=('MS Sans Serif', 13), bd=0, activebackground=theme['button_select_bg'], activeforeground=theme['foreground'],command=lambda: reset_data())
    refresh_button.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
    # Function reset data value, refresh treeview, clear all entry, combobox
    def reset_data():
        global data
        job_role_combobox.set('')
        exp_combobox.set('')
        gpa_entry_from.delete(0, tk.END)
        gpa_entry_to.delete(0, tk.END)
        applied_frame.refresh_treeview_applied()
        dao = DatabaseManager().get_dao()
        data = dao.fetch_exp_and_job_role()
        job_role_combobox['values'] = data["job_roles"]
        exp_combobox['values'] = data["exp_types"]
    # Treeview 
    tree_frame = tk.Frame(applied_frame, bg=theme['background'])
    tree_frame.grid(row=1, column=1, columnspan=8,rowspan=8, padx=5, pady=5, sticky="nsew")
    tree_frame.grid_propagate(False)
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    treeview = Treeview(tree_frame,style="Edge.Treeview")
    columns = ("Name", "Phone", "Email", "GPA","Education","Major", "Skill", "Project","Experience", "Job role","ID")
    treeview["columns"] = columns
    treeview["show"] = "headings"
    treeview.heading("Name", text="Name")
    treeview.column("Name", anchor='center', width=150, stretch=False)
    treeview.heading("Phone", text="Phone")
    treeview.column("Phone", anchor='center', width=80, stretch=False)
    treeview.heading("Email", text="Email")
    treeview.column("Email", anchor='center', width=150, stretch=False)
    treeview.heading("GPA", text="GPA")
    treeview.column("GPA", anchor='center', width=50, stretch=False)
    treeview.heading("Education", text="Education")
    treeview.column("Education", anchor='center', width=100, stretch=False)
    treeview.heading("Major", text="Major")
    treeview.column("Major", anchor='center', width=100, stretch=False)
    treeview.heading("Experience", text="EXP")
    treeview.column("Experience", anchor='center', width=70, stretch=False)
    treeview.heading("Skill", text="Skill")
    treeview.column("Skill", anchor='center', width=150, stretch=False)
    treeview.heading("Project", text="Project")
    treeview.column("Project", anchor='center', width=150, stretch=False)
    treeview.heading("Job role", text="Job role")
    treeview.column("Job role", anchor='center', width=100, stretch=False)
    treeview.heading("ID", text="ID")
    treeview.column("ID", anchor='center', width=50, stretch=False)
    treeview.grid(row=0, column=0, padx=1, pady=1, sticky="nsew") 
    hs = Scrollbar(tree_frame, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=hs.set)
    treeview.bind("<<TreeviewSelect>>", lambda e: on_treeview_applied_select(e,treeview) if update_selected else None)
    hs.grid(row=1, column=0, sticky="ew")
    def refresh_treeview_applied():
        global Aplicantdao
        Aplicantdao = ApplicantDAO.get_instance()
        applicants = Aplicantdao.fetch_all_applicants()
        treeview.delete(*treeview.get_children())
        for applicant in applicants:
            treeview.insert("", "end", values=applicant)
    applied_frame.refresh_treeview_applied = refresh_treeview_applied
    refresh_treeview_applied()  
    def filter_applied(dao):
        job_role = job_role_combobox.get()
        exp = exp_combobox.get()
        gpa_from = gpa_entry_from.get() 
        gpa_to = gpa_entry_to.get() 
        if job_role =="" and exp=="" and gpa_from=="" and gpa_to=="":
            return
        gpa_from = float(gpa_from) if gpa_from != "" else 0
        gpa_to = float(gpa_to) if gpa_to != "" else 4
        print(f"Job Role: {job_role}, Exp: {exp}, GPA From: {gpa_from}, GPA To: {gpa_to}")
        applicants = dao.fetch_by_filter(job_role, exp, gpa_from, gpa_to)
        print(applicants)
        treeview.delete(*treeview.get_children())
        for applicant in applicants:
            treeview.insert("", "end", values=applicant)
    def create_button(parent, text,command):
        button = tk.Button(parent, 
                           text=text, 
                           width=10, 
                           height=2, 
                           bg=theme['button_bg'], 
                           fg=theme['foreground'], 
                           bd=0, 
                           font=('MS Sans Serif', 13), 
                           activebackground=theme['button_select_bg'], 
                           activeforeground=theme['foreground'],
                           command=command)
        return button
    button_footer_frame = tk.Frame(applied_frame, bg=theme['backgroundtheme'],bd=2)
    button_footer_frame.grid(row=9, column=1, columnspan=8, padx=5, pady=5, sticky="nsew")
    button_footer_frame.grid_propagate(False)
    button_footer_frame.grid_rowconfigure(0, weight=1)
    for col in range(8):
        button_footer_frame.grid_columnconfigure(col, weight=1)
    # for col in range(8):
    #     label = tk.Label(button_footer_frame, text=f"Col {col}", bg='lightpink', fg="white")
    #     label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
    # Delete button
    def delete_applicant():
        selected_item = treeview.selection()
        if not selected_item:
            return
        applicant_id = treeview.item(selected_item)['values'][-1]
        dao = ApplicantDAO.get_instance()
        success = dao.delete_applicant(applicant_id)
        if success:
            tk.messagebox.showinfo("Success", "Delete successful!")
            refresh_treeview_applied()
        else:
            tk.messagebox.showerror("Error", "Delete failed!")
    boder_frame_delete = create_boder_button(button_footer_frame)
    boder_frame_delete.grid(row=0,column=2,columnspan=2, padx=5, pady=5, sticky="nsew")
    boder_frame_delete.grid_propagate(False)
    boder_frame_delete.grid_rowconfigure(0, weight=1)
    boder_frame_delete.grid_columnconfigure(0, weight=1)
    button_delete = create_button(boder_frame_delete, "Delete",lambda: delete_applicant())
    button_delete.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
    # Update button
    def on_update_button_click():
        global update_selected
        update_selected = True  
        off_widgets([exp_frame, boder_frame_update, job_role_frame, gpa_frame_from, gpa_frame_to, boder_frame_delete, filter_frame], master)
    boder_frame_update = create_boder_button(button_footer_frame)
    boder_frame_update.grid(row=0,column=4,columnspan=2, padx=5, pady=5, sticky="nsew")
    boder_frame_update.grid_propagate(False)
    boder_frame_update.grid_rowconfigure(0, weight=1)
    boder_frame_update.grid_columnconfigure(0, weight=1)
    button_update = create_button(boder_frame_update, "Update", lambda: on_update_button_click())
    button_update.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
    return applied_frame