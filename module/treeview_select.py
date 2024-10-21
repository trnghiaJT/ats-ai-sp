from data.DAO.applicantDAO import ApplicantDAO
from data.DAO.expDAO import expDAO
from module.create_chart import *
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
def on_treeview_select(event,
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
                       project_text):
        selected_item = treeview.selection() 
        if not treeview.get_children():
            return
        if not selected_item:
            return
        item_values = treeview.item(selected_item)["values"]
        if len(item_values) <= 4:
            return
        item_values = treeview.item(selected_item)["values"] 
        exp = item_values[4]   
        exp_dao = expDAO.get_instance()
        df = plot_data(job_role_combobox.get())
        update_chart(exp,exp_dao,df)
        if selected_item:
            selected_name = item_values[0]
            selected_phone = '0'+str(item_values[1])
            selected_job_role = item_values[5]
            # print(f"Selected: Name = {selected_name}, Phone = {selected_phone}, Role = {selected_job_role}")
            applicant_dao = ApplicantDAO.get_instance()
            applicant_data = applicant_dao.fetch_applicant_by_info(selected_name, selected_phone, selected_job_role)
            if applicant_data:
                # print("Get data successful:", applicant_data)
                # Fill data to text widgets
                name_entry.config(state='normal')
                name_entry.delete("1.0", tk.END)
                name_entry.insert("1.0", applicant_data[0])
                name_entry.config(state='disabled')
                # print(f"Name: {applicant_data[0]}")
                phone_entry.config(state='normal')
                phone_entry.delete("1.0", tk.END)
                phone_entry.insert("1.0", str(applicant_data[1]))
                phone_entry.config(state='disabled')
                # print(f"Phone: {applicant_data[1]}")
                email_entry.config(state='normal')
                email_entry.delete("1.0", tk.END)
                email_entry.insert("1.0", applicant_data[2])
                email_entry.config(state='disabled')
                # print(f"Email: {applicant_data[2]}")
                gpa_entry.config(state='normal')
                gpa_entry.delete("1.0", tk.END)
                gpa_entry.insert("1.0", applicant_data[3])
                gpa_entry.config(state='disabled')
                # print(f"GPA: {applicant_data[3]}")
                education_entry.config(state='normal')
                education_entry.delete("1.0", tk.END)
                education_entry.insert("1.0", applicant_data[4])
                education_entry.config(state='disabled')
                # print(f"Education: {applicant_data[4]}")
                major_entry.config(state='normal')
                major_entry.delete("1.0", tk.END)
                major_entry.insert("1.0", applicant_data[5])
                major_entry.config(state='disabled')
                # print(f"Major: {applicant_data[5]}")
                exp_entry.config(state='normal')
                exp_entry.delete("1.0", tk.END)
                exp_entry.insert("1.0", applicant_data[6])
                exp_entry.config(state='disabled')
                # print(f"Exp: {applicant_data[6]}")
                skill_entry.config(state='normal')
                skill_entry.delete("1.0", tk.END)
                skill_entry.insert("1.0", applicant_data[7])
                skill_entry.config(state='disabled')
                # print(f"Skills: {applicant_data[7]}")
                project_text.config(state='normal')
                project_text.delete("1.0", tk.END)
                project_text.insert("1.0", applicant_data[8])
                project_text.config(state='disabled')
                # print(f"Project: {applicant_data[8]}")
            else:
                return
        else:
            return

def on_treeview_applied_select(event, treeview):
    selected_item = treeview.selection()
    if not selected_item:
        return
    values = treeview.item(selected_item[0], 'values')
    from module.state_frame import up_frame
    from gui.frmupdate import data
    for labelframe in up_frame.winfo_children():
        if isinstance(labelframe, tk.LabelFrame):
            for widget in labelframe.winfo_children():
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                elif isinstance(widget, AutocompleteCombobox):
                    widget.set('')
    name_entry = up_frame.winfo_children()[0].winfo_children()[0]  
    phone_entry = up_frame.winfo_children()[1].winfo_children()[0]  
    email_entry = up_frame.winfo_children()[2].winfo_children()[0]
    gpa_entry = up_frame.winfo_children()[3].winfo_children()[0]
    education_entry = up_frame.winfo_children()[4].winfo_children()[0]
    major_entry = up_frame.winfo_children()[5].winfo_children()[0]
    skill_entry = up_frame.winfo_children()[6].winfo_children()[0]
    project_text = up_frame.winfo_children()[7].winfo_children()[0]
    exp_cb = up_frame.winfo_children()[8].winfo_children()[0]  
    job_role_cb = up_frame.winfo_children()[9].winfo_children()[0]  
    id_entry = up_frame.winfo_children()[10].winfo_children()[0]  
    name_entry.insert(0, values[0])
    phone_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    gpa_entry.insert(0, values[3])
    education_entry.insert(0, values[4])
    major_entry.insert(0, values[5])
    skill_entry.insert(0, values[6])
    project_text.insert(tk.END, values[7])
    id_entry.insert(0, values[10])
    exp_cb['values'] = data["exp_types"]
    exp_cb.set(values[8])
    job_role_cb['values'] = data["job_roles"]
    job_role_cb.set(values[9])