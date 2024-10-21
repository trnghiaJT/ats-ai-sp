import tkinter as tk
import os
from pypdf import PdfReader
from tkinter import filedialog, messagebox
from module.gen_sum import evaluate_resume
from gui import frmsave
from module.wraping_info import wraping_resume
from module.apply_theme import apply_theme
# Declare position of frame
pox = (1024-826)/2
global extracted_value
def create_summary_frame(master):
    theme = apply_theme()
    summary_frame = tk.Frame(master, bg=theme['backgroundtheme'])
    label_summary = tk.Label(summary_frame, 
                              text="AI SUMMARY APPLICATION TRACKING SYSTEM", 
                              bg=theme['backgroundtheme'], 
                              fg=theme['foreground'], 
                              font=('MS Sans Serif', 20, 'bold'), 
                              wraplength=550,
                              anchor='w',
                              justify='left')
    label_summary.place(x=pox, y=20, width=550)  
    border_frame = tk.Frame(summary_frame, bg=theme['background'], bd=2)
    border_frame.place(x=pox, y=100)
    jd_text = tk.Text(border_frame, 
                      wrap='word',
                      highlightbackground=theme['highlightbackground'],highlightthickness=1, 
                      bg=theme['background'],fg=theme['foreground'], 
                      width=91,insertbackground=theme['foreground'], 
                      height=5, font=('Arial', 13), bd=0)
    jd_text.pack(fill=tk.BOTH, expand=True)  
    default_text = "Type job description here..."
    jd_text.insert(tk.END, default_text)
    jd_text.tag_configure("italic", font=('Arial', 13, 'italic'))  
    jd_text.tag_add("italic", "1.0", "1.end")  
    jd_text.tag_configure("italic", font=('Arial', 13, 'italic'))  
    jd_text.tag_add("italic", "1.0", "1.end")  
    # Function to clear default text
    def clear_default_text(event):
        if jd_text.get("1.0", tk.END).strip() == default_text:
            jd_text.delete("1.0", tk.END)
    # Function to remove italic tag
    def remove_italic(event):
        if jd_text.get("1.0", tk.END).strip() != "":
            jd_text.tag_remove("italic", "1.0", "1.end")
    def update_response_text(response):
        response_text.config(state='normal')
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, response)
        response_text.config(state='disabled') 
    # Bind events to jd_text
    jd_text.bind("<FocusIn>", clear_default_text)
    jd_text.bind("<Key>", remove_italic)
    # Wraping info
    def parse_response(response_text):
        # Convert response_text to a list of lines
        lines = response_text.splitlines()
        # Create an empty dictionary to store parsed data
        parsed_data = {}
        # Loop through each line
        for line in lines:
            if ": " in line:
                # Split the line into key and value
                key, value = line.split(": ", 1)
                parsed_data[key] = value
        return parsed_data
    # Create get file_frame same size with jd_text
    get_file_frame = tk.Frame(summary_frame, bg=theme['line'])
    get_file_frame.place(x=pox, y=220, width=826, height=50)
    get_file_frame.grid_columnconfigure(0, minsize=150, weight=1)  
    get_file_frame.grid_columnconfigure(1, minsize=400, weight=3)  
    get_file_frame.grid_columnconfigure(2, minsize=150, weight=1) 
    get_file_frame.grid_rowconfigure(0, weight=1)  
    get_file_frame.grid_rowconfigure(1, weight=0)  
    get_file_frame.grid_rowconfigure(2, weight=1) 
    def choose_file():
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
         # get the file name and display it on the label
            global file_path
            file_path = filename
            short_filename = os.path.basename(filename)
        # shorten the filename if it's too long
            max_length = 50 
            if len(short_filename) > max_length:
                short_filename = short_filename[:47] + "..."
            file_label_var.set(short_filename)
        else:
            file_label_var.set("No file chosen")
    # Function to submit file
    def submit_file():
        global extracted_value 
        try:
        # Check if file_path isn't defined
            if 'file_path' not in globals() or file_path is None:
                messagebox.showwarning("Warning", "Please select a valid file!")
                return
        # Check if jd_text is still default content
            jd_content = jd_text.get("1.0", tk.END).strip()
            if jd_content == default_text:
                messagebox.showwarning("Warning", "Please import your job description!")
                return
        # Check if response_text is empty
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                extracted_text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    extracted_text += page.extract_text()
            # print("PDF content extracted.")
        # Get job description text to save
            jd = jd_content
            # print(f"Extracted PDF Text:\n{extracted_text}")
            # print(f"Job Description Text:\n{jd}")
            response = evaluate_resume(extracted_text, jd)
            response_info = wraping_resume(extracted_text)
            # print(response_info)
            extracted_value = extracted_text
            global parse_text
            parse_text = parse_response(response_info)
            update_response_text(response)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing file: {e}")
            # print(f"Error processing file: {e}")
    # Button "Choose file"
    choose_file_button = tk.Button(get_file_frame, text="Choose file", 
                                   command=choose_file, bg=theme['button_bg'], fg=theme['foreground'],
                                   relief='groove',font=('Ms Sans Serif', 12),bd=2)
    choose_file_button.grid(row=1, column=0, padx=10, pady=5,sticky='ns')
    # Label to show the chosen file
    file_label_var = tk.StringVar()
    file_label_var.set("No file chosen")  # Set default "No file chosen"
    file_label = tk.Label(get_file_frame, textvariable=file_label_var,
                          fg=theme['foreground'], bg=theme['line'], 
                          anchor='w',font=('Arial', 12))
    file_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')
    # Button "Submit"
    submit_button = tk.Button(get_file_frame, text="Submit", command=submit_file,width=20, bg=theme['button_bg'], fg=theme['foreground'],relief='flat',font=('Ms Sans Serif', 12))
    submit_button.grid(row=1, column=2, padx=10, pady=5,sticky='ns')
    # Create main_content_sumary_frame
    main_content_summary_frame = tk.Frame(summary_frame, bg=theme['background'],bd=3)
    main_content_summary_frame.place(x=pox, y=290, width=826, height=350)
    response_text = tk.Text(main_content_summary_frame, 
                            wrap='word', 
                            bg=theme['background'], 
                            fg=theme['foreground'],
                            highlightbackground=theme['highlightbackground'],
                            highlightthickness=1,
                         font=('Arial', 12), bd=0,state='disabled',insertbackground=theme['foreground'])
    response_text.pack(fill=tk.BOTH, expand=True)
    # Create a frame to contain buttons
    button_refesh_frame = tk.Frame(summary_frame, bg=theme['boder_button'],bd=2)
    button_refesh_frame.place(x=pox+550+(826-550-150), y=40, width=150, height=40)
    # Refresh fields
    def refresh_fields():
        # Clear job description text and set it to default
        jd_text.delete("1.0", tk.END)
        jd_text.insert(tk.END, default_text)
        jd_text.tag_add("italic", "1.0", "1.end")
        file_label_var.set("No file chosen")
        global file_path
        file_path = None
        # Clear response text
        response_text.config(state='normal')
        response_text.delete("1.0", tk.END)
        response_text.config(state='disabled')
        summary_frame.focus_set()
    # Create button func
    def create_button_func(parent, text, command):
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
                           highlightbackground=theme['highlightbackground'],
                            highlightthickness=1,
                           command=command)
        return button
    # Create a button to refresh
    button_refresh = create_button_func(button_refesh_frame, "Refresh", refresh_fields)
    button_refresh.pack(fill='x')
    # Create a frame to contain buttons
    button_save_frame = tk.Frame(summary_frame, bg=theme['boder_button'],bd=2)
    button_save_frame.place(x=pox+550+(826-550-150), y=660, width=150, height=40)
    # Create def open_save_frame call from frmsave.py frame size full root
    def open_save_frame():
        # Check if file_path isn't defined
        if 'file_path' not in globals() or file_path is None:
            messagebox.showwarning("Warning", "Please select a valid file!")
            return
        # Check if jd_text is still default content
        jd_content = jd_text.get("1.0", tk.END).strip()
        if jd_content == default_text:
            messagebox.showwarning("Warning", "Please import your job description!")
            return
        # Check if response_text is empty
        response = response_text.get("1.0", tk.END).strip()
        if response == "":
            messagebox.showwarning("Warning", "Please submit the file first!")
            return
        save_frame = frmsave.create_save_frame(master,extracted_value)
        frmsave.fill_form(parse_text)
        save_frame.tkraise()
    # Create a button to save
    button_save = create_button_func(button_save_frame, "Save", open_save_frame)
    button_save.pack(fill='x')
    jd_text.bind("<FocusIn>", clear_default_text)
    jd_text.bind("<Key>", remove_italic)
    return summary_frame