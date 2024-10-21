import tkinter as tk
from tkinter.ttk import Treeview
from data.data_manager import DatabaseManager
from ttkwidgets.autocomplete import AutocompleteCombobox 
from data.DAO.applicantDAO import ApplicantDAO
from module.create_chart import *
from module.hover_entry_popup import HoverEntryPopup
from module.treeview_select import on_treeview_select
from module.apply_theme import apply_theme
def create_analytics_frame(master):
    theme = apply_theme()
    analytics_frame = tk.Frame(master, bg=theme['backgroundtheme'])
    for row in range(10):
        analytics_frame.grid_rowconfigure(row, weight=1)
    for col in range(10):
        analytics_frame.grid_columnconfigure(col, weight=1)
    for row in range(10):
        for col in range(10):
            label = tk.Label(analytics_frame, text=f"Row {row} Col {col}", bg=theme["backgroundtheme"], fg=theme['backgroundtheme'])
            label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    analytics_frame.grid_propagate(False)
    # Select job role frame
    dao = DatabaseManager().get_dao()
    data = dao.fetch_exp_and_job_role()
    job_role_frame = tk.Frame(analytics_frame, bg=theme['backgroundtheme'])
    job_role_frame.grid(row=0, column=2, rowspan=1, columnspan=6, sticky='nsew', padx=5, pady=5)
    job_role_frame.grid_propagate(False)
    for i in range(4):
        job_role_frame.columnconfigure(i, weight=1)
    job_role_frame.rowconfigure(0, weight=1)
    border_frame = tk.Frame(job_role_frame, bg=theme['background'], bd=2)
    border_frame.grid(row=0, column=0, rowspan=1, columnspan=3, sticky='nsew', padx=5, pady=15)
    border_frame.grid_propagate(False)
    border_frame.columnconfigure(0, weight=1)
    border_frame.rowconfigure(0, weight=1)
    job_role_combobox = AutocompleteCombobox(border_frame, completevalues=[])
    job_role_combobox['values'] = data["job_roles"]
    job_role_combobox.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    button_frame = tk.Frame(job_role_frame, bg=theme['boder_button'], bd=2)
    button_frame.grid(row=0, column=3, rowspan=1, columnspan=1, sticky='nsw', padx=5, pady=15)
    button_search = tk.Button(button_frame, text="Search",
                              command=lambda:select_button() , font=( 'Ms Sans Serif' , 13), 
                              bg=theme['button_bg'], fg=theme['foreground'],relief='flat')
    button_search.pack(fill='x')
    # Chart frame 
    chart_frame = tk.Frame(analytics_frame, bg=theme['boder_button'])
    chart_frame.grid(row=1, column=0, rowspan=5, columnspan=6, sticky='nsew', padx=5, pady=5)
    chart_frame.grid_propagate(False)
    chart_frame.columnconfigure(0, weight=1)
    chart_frame.rowconfigure(0, weight=1)
    setup_chart(chart_frame)
    # Select option_analytics frame
    info_analytics_frame =tk.Frame(analytics_frame, bg=theme['boder_button'])
    info_analytics_frame.grid(row=1, column=6, rowspan=9, columnspan=4, sticky='nsew', padx=1, pady=1)
    info_analytics_frame.grid_propagate(False)
    for row in range(9):
        info_analytics_frame.grid_rowconfigure(row, weight=1, minsize=25)
    for col in range(4):
        info_analytics_frame.grid_columnconfigure(col, weight=1, minsize=100)
    # for row in range(9):
    #     for col in range(4):
    #         label = tk.Label(info_analytics_frame, text=f"Row {row} Col {col}", bg='#262c3c', fg="white")
    #         label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    hover = HoverEntryPopup(analytics_frame)
    label = tk.Label(info_analytics_frame, text="Applicant Information", 
                     bg=theme['backgroundtheme'], fg=theme['foreground'],font = ('MS Sans Serif', 15))
    label.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")
    # Create text just for read
    def create_text(parent):
        text = tk.Text(parent, wrap='word', bg=theme['entry_dark'], fg=theme['entry_dark_fg'],
                          font=('Arial', 13), bd=0, insertbackground=theme['foreground'],state='disabled',
                          highlightbackground=theme['highlightbackground'],highlightthickness=1, relief='flat')
        text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        return text
    def create_labelframe(parent, text):
        frame = tk.LabelFrame(parent, text=text, fg=theme["foreground"], bg=theme['backgroundtheme'],
                              font=('MS Sans Serif', 13), relief='flat')
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame
    # Name
    name_frame = create_labelframe(info_analytics_frame, "Name:")
    name_entry = hover.create_entry(name_frame,"")
    name_frame.grid(row=1, column=0, columnspan=4 ,  padx=5, pady=5, sticky="nsew")
    # Email
    email_frame = create_labelframe(info_analytics_frame, "Email:")
    email_entry = hover.create_entry(email_frame,"")
    email_frame.grid(row=2, column=0,columnspan=4, padx=5, pady=5, sticky="nsew")
    # Phone 
    phone_frame = create_labelframe(info_analytics_frame, "Phone:")
    phone_entry = hover.create_entry(phone_frame,"")
    phone_frame.grid(row=3, column=0,columnspan=2, padx=5, pady=5, sticky="nsew")
    # EXP
    exp_frame = create_labelframe(info_analytics_frame, "Exp:")
    exp_entry = hover.create_entry(exp_frame,"")
    exp_frame.grid(row=3, column=2,columnspan=2, padx=5, pady=5, sticky="nsew")
    # Education
    education_frame = create_labelframe(info_analytics_frame, "Education:")
    education_entry = hover.create_entry(education_frame,"")
    education_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    # GPA
    gpa_frame = create_labelframe(info_analytics_frame, "GPA:")
    gpa_entry = hover.create_entry(gpa_frame,"")
    gpa_frame.grid(row=4, column=2,columnspan=2, padx=5, pady=5, sticky="nsew")
    # Major
    major_frame = create_labelframe(info_analytics_frame, "Major:")
    major_entry = hover.create_entry(major_frame,"")
    major_frame.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
    # Skiil
    skill_frame = create_labelframe(info_analytics_frame, "Skill:")
    skill_entry = hover.create_entry(skill_frame,"")
    skill_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
    # Project
    project_frame = create_labelframe(info_analytics_frame, "Project:")
    project_text = create_text(project_frame)
    project_frame.grid(row=7, column=0, columnspan=4,rowspan=2, padx=5, pady=5, sticky="nsew")
    # Tree frame data
    tree_frame = tk.Frame(analytics_frame, bg=theme['boder_button'])
    tree_frame.grid(row=6, column=0, rowspan=4, columnspan=6, sticky='nsew', padx=5, pady=5)
    tree_frame.grid_propagate(False)
    treeview = Treeview(tree_frame, style="Edge.Treeview")
    columns = ("Name", "Phone", "Email", "GPA", "EXP","Job role")
    treeview["columns"] = columns
    treeview["show"] = "headings" 
    # Config width of columns
    treeview.heading("Name", text="Name")
    treeview.column("Name", anchor='center', width=150)
    treeview.heading("Phone", text="Phone")
    treeview.column("Phone", anchor='center', width=80)
    treeview.heading("Email", text="Email")
    treeview.column("Email", anchor='center', width=150)
    treeview.heading("GPA", text="GPA")
    treeview.column("GPA", anchor='center', width=50)
    treeview.heading("EXP", text="EXP")
    treeview.column("EXP", anchor='center', width=70)
    treeview.heading("Job role", text="Job role")
    treeview.column("Job role", anchor='center', width=100)
    treeview.grid(row=0, column=0, sticky='nsew',padx=1, pady=1)
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    treeview.bind("<<TreeviewSelect>>", lambda event: on_treeview_select(event,
                                                                        treeview,
                                                                        job_role_combobox, 
                                                                        name_entry, 
                                                                        phone_entry, 
                                                                        email_entry, 
                                                                        gpa_entry, 
                                                                        education_entry, 
                                                                        major_entry,
                                                                        exp_entry,
                                                                        skill_entry, 
                                                                        project_text))
    def refresh_treeview():
        dao = DatabaseManager().get_dao()
        applicants = dao.fetch_applicants()
        treeview.delete(*treeview.get_children())
        for applicant in applicants:
            treeview.insert("", "end", values=applicant)
    analytics_frame.refresh_treeview = refresh_treeview
    refresh_treeview()  
    # Select button func
    def select_button():
        selected_job_role = job_role_combobox.get()
        if not selected_job_role or selected_job_role not in job_role_combobox['values']:
            tk.messagebox.showerror("Error", f"'{selected_job_role}' is not a valid job role.")
            return
        applicant_dao = ApplicantDAO.get_instance()
        applicants = applicant_dao.fetch_applicant_by_job_role(selected_job_role)
        if not applicants:
            tk.messagebox.showinfo("No Data", f"No applicants found for the job role: {selected_job_role}")
            return
        # Refresh treeview
        treeview.delete(*treeview.get_children())
        for applicant in applicants:
            treeview.insert("", "end", values=applicant)
        plot_data(selected_job_role)
    # Button "Refresh"
    border_button_frame = tk.Frame(analytics_frame, bg=theme['boder_button'], bd=2)
    border_button_frame.grid(row=0, column=9, rowspan=1, columnspan=1, sticky='nsew', padx=5, pady=15)
    border_button_frame.grid_propagate(False)
    border_button_frame.columnconfigure(0, weight=1)
    border_button_frame.rowconfigure(0, weight=1)
    button_refresh = tk.Button(border_button_frame, text="Refresh", font=( 'Ms Sans Serif' , 13), 
                               bg=theme["backgroundtheme"], fg=theme['foreground'],relief='flat',command=lambda:refresh())
    button_refresh.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
    def clear_entry(entry):
        entry.config(state='normal')
        entry.delete(1.0, tk.END)
        entry.config(state='disabled')
    def refresh():
        global data
        job_role_combobox.set('')
        analytics_frame.refresh_treeview()
        dao = DatabaseManager().get_dao()
        data = dao.fetch_exp_and_job_role()
        job_role_combobox['values'] = data["job_roles"]
        entries = [
            name_entry,
            phone_entry,
            email_entry,
            gpa_entry,
            education_entry,
            major_entry,
            skill_entry,
            project_text
        ]
        for entry in entries:
            clear_entry(entry)
        clear_chart()
        setup_chart(chart_frame)   
    return analytics_frame