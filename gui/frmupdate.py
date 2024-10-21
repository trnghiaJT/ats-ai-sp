import tkinter as tk
from module.hover_entry_popup import HoverEntryPopup
from ttkwidgets.autocomplete import AutocompleteCombobox
from data.data_manager import DatabaseManager
from data.DAO.applicantDAO import ApplicantDAO
from data.DAO.jobroleDAO import JobRoleDAO
from module.apply_theme import apply_theme 
up_frame = None
name_entry_up = None
email_entry_up = None
phone_entry_up = None
exp_cb_up = None
education_entry_up = None
gpa_entry_up = None
job_role_cb_up = None
major_entry_up = None
skill_entry_up = None
project_text_up = None
data = None
def create_update_frame(panel):
    theme = apply_theme()
    global data, name_entry_up, email_entry_up, phone_entry_up, exp_cb_up, education_entry_up, gpa_entry_up,job_role_cb_up, major_entry_up,skill_entry_up,project_text_up
    up_frame = tk.Frame(panel, bg=theme['backgroundtheme'])
    up_frame.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
    for row in range(9):
        up_frame.grid_rowconfigure(row, weight=1, minsize=25)
    for col in range(3):
        up_frame.grid_columnconfigure(col, weight=1, minsize=100)
    # for row in range(9):
    #     for col in range(3):
    #         label = tk.Label(up_frame, text=f"Row {row} Col {col}", bg='#262c3c', fg="white")
    #         label.grid(row=row, column=col, padx=0, pady=5, sticky="nsew")
    up_frame.grid_propagate(False)
    # Create text just for read
    def create_text(parent):
        text = tk.Text(parent, 
                       wrap='word', 
                       bg=theme['entry_dark'], 
                       fg=theme['entry_dark_fg'],
                       font=('Arial', 13), 
                       bd=0, 
                       insertbackground=theme['entry_dark_fg'],
                       state='normal',
                       relief='flat',
                       highlightbackground=theme['highlightbackground'],
                       highlightthickness=1)
        text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        return text
    def create_entry(parent):
        entry = tk.Entry(parent, bg=theme['entry_dark'], 
                         fg=theme['entry_dark_fg'],
                         font=('Arial', 13), 
                         bd=0, 
                         insertbackground=theme['entry_dark_fg'],
                         state='normal',
                         highlightbackground=theme['highlightbackground'],
                         highlightthickness=1,
                         relief='flat')
        entry.grid(row=0, column=0, padx=5, pady=10, sticky="new")
        return entry
    def create_labelframe(parent, text):
        frame = tk.LabelFrame(parent, 
                              text=text, 
                              fg=theme['foreground'], 
                              bg=theme['backgroundtheme'],
                              font=('MS Sans Serif', 13),
                              relief='flat' 
                              )
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame
    hover = HoverEntryPopup(up_frame)
    dao = DatabaseManager().get_dao()
    data = dao.fetch_exp_and_job_role()
    # Name
    # Name
    name_frame = create_labelframe(up_frame, "Name:")
    name_entry_up = create_entry(name_frame)
    name_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    # Phone
    phone_frame = create_labelframe(up_frame, "Phone:")
    phone_entry_up = create_entry(phone_frame)
    phone_frame.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky="nsew")
    # Email
    email_frame = create_labelframe(up_frame, "Email:")
    email_entry_up = create_entry(email_frame)
    email_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew") 
    # GPA
    gpa_frame = create_labelframe(up_frame, "GPA:")
    gpa_entry_up = create_entry(gpa_frame)
    gpa_frame.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky="nsew")
    # Education
    education_frame = create_labelframe(up_frame, "Education:")
    education_entry_up = create_entry(education_frame)
    education_frame.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
    # Major
    major_frame = create_labelframe(up_frame, "Major:")
    major_entry_up = create_entry(major_frame)
    major_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    # Skill
    skill_frame = create_labelframe(up_frame, "Skill:")
    skill_entry_up = create_entry(skill_frame)
    skill_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    # Project
    project_frame = create_labelframe(up_frame, "Project:")
    project_text_up = create_text(project_frame)
    project_frame.grid(row=5, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky="nsew")
    # EXP
    exp_frame = create_labelframe(up_frame, "Exp:")
    exp_cb_up = AutocompleteCombobox(exp_frame, completevalues=[])
    exp_cb_up['values'] = data["exp_types"]
    exp_cb_up.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    exp_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    # Job Role
    job_role = create_labelframe(up_frame, "Job Role:")
    job_role_cb_up = AutocompleteCombobox(job_role)
    job_role.grid(row=6, column=2, columnspan=1, padx=5, pady=5, sticky="nsew")
    job_role_cb_up['values'] = data["job_roles"]
    job_role_cb_up.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    # Id
    id_frame = create_labelframe(up_frame, "ID:")
    id_entry = create_entry(id_frame)
    id_frame.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    # Button
    def boder_button(parent):
        boder_frame = tk.Frame(parent, bg=theme['boder_button'])
        return boder_frame
   
    def update_applicant_data(applicant_id):
        global data
        updated_data = {
            "Name": name_entry_up.get(),
            "Phone": phone_entry_up.get(),
            "Email": email_entry_up.get(),
            "GPA": gpa_entry_up.get(),
            "Education": education_entry_up.get(),
            "Major": major_entry_up.get(),
            "Skill": skill_entry_up.get(),
            "Project": project_text_up.get("1.0", tk.END).strip(),
            "Exp": exp_cb_up.get(),
            "JobRole": job_role_cb_up.get()
        }
        dao = ApplicantDAO.get_instance()
        success = dao.update_applicant(applicant_id, updated_data)
        job_role_dao = JobRoleDAO.get_instance()
        if not job_role_dao.insert_job_role(updated_data["JobRole"]):
            tk.messagebox.showerror("Error", "Failed to save job role.")
            return
        if success:
            tk.messagebox.showinfo("Success", "Update successful!")
            dao = DatabaseManager().get_dao()
            data = dao.fetch_exp_and_job_role()
        else:
            tk.messagebox.showerror("Error", "Update failed!")  
    # Button "Update"
    button_update_frame = boder_button(up_frame)
    button_update_frame.grid(row=8, column=2, columnspan=1, padx=5, pady=5, sticky="nsew")
    button_update_frame.grid_propagate(False)
    button_update_frame.grid_rowconfigure(0, weight=1)
    button_update_frame.grid_columnconfigure(0, weight=1)
    button_update = tk.Button(button_update_frame, 
                              text="Update", 
                              bg=theme['button_bg'], 
                              fg=theme['foreground'], 
                              font=('MS Sans Serif', 13), 
                              bd=0, 
                              activebackground=theme['button_select_bg'], 
                              activeforeground=theme['foreground'],
                              command=lambda: update_applicant_data(id_entry.get()))
    button_update.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
    # Button "Back"
    button_back_frame = boder_button(up_frame)
    button_back_frame.grid(row=8, column=0, columnspan=1, padx=5, pady=5, sticky="nsew")
    button_back_frame.grid_propagate(False)
    button_back_frame.grid_rowconfigure(0, weight=1)
    button_back_frame.grid_columnconfigure(0, weight=1)
    from module.state_frame import on_widgets
    from gui.frmapplied import exp_frame, job_role_frame, gpa_frame_from, gpa_frame_to, boder_frame_delete, boder_frame_update, filter_frame
    button_back = tk.Button(button_back_frame, 
                            text="Back", 
                            bg=theme['button_bg'], 
                            fg=theme['foreground'], 
                            font=('MS Sans Serif', 13), 
                            bd=0, 
                            activebackground=theme['button_select_bg'], 
                            activeforeground=theme['foreground'],
                            command=lambda: on_widgets([exp_frame, 
                                                        job_role_frame, 
                                                        gpa_frame_from, 
                                                        gpa_frame_to, 
                                                        boder_frame_delete, 
                                                        boder_frame_update, 
                                                        filter_frame]))
    button_back.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
    return up_frame
    