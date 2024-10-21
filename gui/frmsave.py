import tkinter as tk
import tkinter.scrolledtext as tkscrolled 
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from data.data_manager import DatabaseManager
from data.DAO.applicantDAO import ApplicantDAO
from data.DAO.jobroleDAO import JobRoleDAO
from module.hover_entry_popup import HoverEntryPopup
from module.apply_theme import apply_theme
def fill_form(data):
    name_text.insert(0, data.get("Name", ""))
    phone_text.insert(0, data.get("Phone", ""))
    email_text.insert(0, data.get("Email", ""))
    gpa_text.insert(0, data.get("GPA", ""))
    education_text.insert(0, data.get("Education", ""))
    major_text.insert(0, data.get("Major", ""))
    skill_text.insert(1.0, data.get("Skills", ""))
    project_text.delete(1.0, tk.END)
    project_text.insert(tk.END, data.get("Project", ""))
def create_save_frame(master, extracted_value=None):
    theme = apply_theme()
    global name_text, phone_text, email_text, gpa_text, education_text, major_text, exp_text, skill_text, project_text
    save_frame = tk.Frame(master, bg=theme['backgroundtheme'])
    save_frame.place(relwidth=1, relheight=1)
    for row in range(10):
        save_frame.grid_rowconfigure(row, weight=1)
    for col in range(10):
        save_frame.grid_columnconfigure(col, weight=1)
    # View frame
    view_frame = tk.Frame(save_frame, bg=theme['view_text_bg'])
    view_frame.grid(row=0, column=4, rowspan=10, columnspan=6, sticky="nsew", padx=5, pady=5)
    view_frame.pack_propagate(False)
    # Text widget for resume
    text_box = tkscrolled.ScrolledText(view_frame, wrap='word', bg=theme['view_text_bg'], fg=theme['foreground'],
                       font=('Arial', 12), bd=0, insertbackground=theme['foreground'])
    text_box.pack(fill=tk.BOTH, expand=True)
    if extracted_value:
        text_box.insert(tk.END, extracted_value)
    def search_text():
        text_box.tag_remove("highlight", "1.0", tk.END)  # Delete old highlights
        search_term = search_entry.get().lower()
        if search_term:
            start_pos = "1.0"
            while True:
                start_pos = text_box.search(search_term, start_pos, stopindex=tk.END, nocase=True)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_term)}c"
            # Highlight
                text_box.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
        text_box.tag_config("highlight", background="#dffa4c", foreground="black")
    def create_button(parent, text, command):
        button = tk.Button(parent, text=text, width=10, height=2, bg=theme['button_bg'], fg=theme['foreground'], bd=0, font=('MS Sans Serif', 13),
                       activebackground=theme['button_select_bg'], activeforeground=theme["foreground"], command=command)
        return button
    def boder_button(parent):
        frame = tk.Frame(parent, bg=theme['boder_button'], bd=2)
        return frame
    # Search frame
    search_frame = tk.Frame(view_frame, bg=theme["backgroundtheme"], bd=2, relief='groove')
    search_frame.pack(fill=tk.X, pady=5, padx=5)
    search_button = create_button(search_frame, "Find", search_text)
    search_button.config(relief='groove')
    search_button.pack(side=tk.RIGHT, padx=5, pady=5)
    search_entry = tk.Entry(search_frame, width=30, bg=theme['entry_bg'], fg=theme["entry_fg"], font=('Arial', 13))
    search_entry.pack(side=tk.RIGHT, padx=5)
    search_label = tk.Label(search_frame, text="Search:", bg=theme['backgroundtheme'], fg=theme['foreground'], font=('Arial', 13))
    search_label.pack(side=tk.RIGHT, padx=5)
    # Button select
    select_button_frame = tk.Frame(save_frame, bg=theme['backgroundtheme'])
    select_button_frame.grid(row=9, column=0, rowspan=1, columnspan=4, sticky="nsew", padx=5, pady=5)
    select_button_frame.grid_propagate(False)
    for i in range(4):
        select_button_frame.columnconfigure(i, weight=1)
    select_button_frame.rowconfigure(0, weight=1)
    # function to back frmsummary
    def back_summary():
        # MessageBox to confirm
        if messagebox.askokcancel("Confirm", "Do you want to back to Summary?"):
            save_frame.destroy()
    # Button back
    back_boder = boder_button(select_button_frame)
    back_boder.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")
    back_boder.grid_propagate(False)
    back_boder.grid_rowconfigure(0, weight=1)
    back_boder.grid_columnconfigure(0, weight=1)
    back_button = create_button(back_boder, "Back", back_summary)
    back_button.grid(row=0, column=0,padx=1, pady=1, sticky="nswe")
    def save_data():
        # Get data from the resume
        data = {
            "Name": name_text.get(),
            "Phone": phone_text.get(),
            "Email": email_text.get(),
            "GPA": gpa_text.get(),
            "Education": education_text.get(),
            "Major": major_text.get(),
            "Skills": skill_text.get(1.0,tk.END).strip(),
            "Project": project_text.get(1.0, tk.END).strip(),
            "Exp": exp_combobox.get(),
            "JobRole": job_role_combobox.get()
        }
        # Check if all required fields are filled
        if not data["Name"] or not data["Phone"] or not data["Email"]:
            tk.messagebox.showerror("Error", "Please fill in all required fields.")
            return
        if not data["GPA"].replace('.', '', 1).isdigit():
            tk.messagebox.showerror("Error", "Please enter a valid GPA (number).")
            return
        # Save ApplicantDAO
        applicant_dao = ApplicantDAO.get_instance()
        jobrole_dao = JobRoleDAO.get_instance()
        if not jobrole_dao.insert_job_role(data["JobRole"]):
            tk.messagebox.showerror("Error", "Failed to save job role.")
            return
        if applicant_dao.insert_applicant(data):
            tk.messagebox.showinfo("Success", "Data saved successfully.")
        else:
            tk.messagebox.showerror("Error", "Applicant already exists and cannot be added again.")
    # Button "Save" Right side
    save_boder = boder_button(select_button_frame)
    save_boder.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
    save_boder.grid_propagate(False)
    save_boder.grid_rowconfigure(0, weight=1)
    save_boder.grid_columnconfigure(0, weight=1)
    save_button = create_button(save_boder, "Save", save_data)
    save_button.grid(row=0, column=0,padx=1, pady=1, sticky="nsew")
    option_frame = tk.LabelFrame(save_frame, text='Application information', fg=theme['foreground'], bg=theme['backgroundtheme'],
                             font=('MS Sans Serif', 13), 
                             relief='groove', 
                             highlightcolor="white")
    option_frame.grid(row=0, column=0, rowspan=9, columnspan=4, sticky="nsew", padx=5, pady=5)
    option_frame.grid_propagate(False)
    for row in range(9):
        option_frame.grid_rowconfigure(row, weight=1, minsize=25)
    for col in range(5):
        option_frame.grid_columnconfigure(col, weight=1, minsize=100)
    # for row in range(9):
    #     for col in range(5):
    #         label = tk.Label(option_frame, text=f"Row {row} Col {col}", bg='#262c3c', fg="white")
    #         label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    # LabelFrame name_frame row 0 col 0 span 1 5
    def create_label_frame(parent, text):
        frame = tk.LabelFrame(parent, text=text, fg=theme['foreground'], bg=theme['backgroundtheme'],
                            font=('MS Sans Serif', 13), relief='flat')
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame
    def create_entry(parent):
        entry = tk.Entry(parent, bg=theme["entry_dark"], fg=theme['entry_dark_fg'], font=('Arial', 13), bd=0, 
                         insertbackground=theme['foreground'],highlightbackground=theme['highlightbackground'],highlightthickness=1)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        return entry
    def create_text(parent):
        text = tk.Text(parent, wrap='word', bg=theme['entry_dark'], fg=theme['entry_dark_fg'],
                          font=('Arial', 13), bd=0, insertbackground=theme['foreground'],highlightbackground=theme['highlightbackground'],highlightthickness=1)
        text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        return text
    dao = DatabaseManager().get_dao()
    data = dao.fetch_exp_and_job_role()
    # Text name in name_frame
    name_frame = create_label_frame(option_frame, "Name:")
    name_frame.grid(row=0, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=5, pady=5)
    name_text = create_entry(name_frame)
    # Text phone in phone_frame
    phone_frame = create_label_frame(option_frame, "Phone:")
    phone_frame.grid(row=0, column=3, rowspan=1, columnspan=2, sticky="nsew", padx=5, pady=5)
    phone_text = create_entry(phone_frame)
    # Text email in email_frame
    email_frame = create_label_frame(option_frame, "Email:")
    email_frame.grid(row=1, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=5, pady=5)
    email_text = create_entry(email_frame)
    # Text widget for GPA in gpa_frame
    gpa_frame = create_label_frame(option_frame, "GPA:")
    gpa_frame.grid(row=1, column=3, rowspan=1, columnspan=2, sticky="nsew", padx=5, pady=5)
    gpa_text = create_entry(gpa_frame)
    # Text education in education_frame
    education_frame = create_label_frame(option_frame, "Education:")
    education_text = create_entry(education_frame)
    education_frame.grid(row=2, column=0, rowspan=1, columnspan=2,sticky="nsew", padx=5, pady=5)
    # Text major in major_frame
    major_frame = create_label_frame(option_frame, "Major:")
    major_frame.grid(row=2, column=2, rowspan=1, columnspan=3, sticky="nsew", padx=5, pady=5)
    major_text = create_entry(major_frame)
    # Text experience in experience_frame
    experience_frame = create_label_frame(option_frame, "Exp:")
    experience_frame.grid(row=4, column=0, rowspan=1, columnspan=5, sticky="nsew", padx=5, pady=5)
    exp_combobox = AutocompleteCombobox(experience_frame, completevalues=[])
    exp_combobox['values'] = data["exp_types"]
    exp_combobox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    # Text skill in skill_frame
    skill_frame = create_label_frame(option_frame, "Skill:")
    skill_frame.grid(row=3, column=0, rowspan=1, columnspan=5, sticky="nsew", padx=5, pady=5)
    skill_text = HoverEntryPopup(master).create_entry_save(skill_frame, "")
    # Text Project in project_frame
    project_frame = create_label_frame(option_frame, "Project:")
    project_frame.grid(row=5, column=0, rowspan=2, columnspan=5, sticky="nsew", padx=5, pady=5)
    project_text = create_text(project_frame)
    # Text Job role applied in job_role_frame
    job_role_frame = create_label_frame(option_frame, "Job role applied:")
    job_role_frame.grid(row=7, column=0, rowspan=1, columnspan=5, sticky="nsew", padx=5, pady=5)
    # Combobox for job role
    job_role_combobox = AutocompleteCombobox(job_role_frame, completevalues=[])
    job_role_combobox['values'] = data["job_roles"]
    job_role_combobox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    return save_frame
