import tkinter as tk 
from gui import frmsummary
from gui import frmanalytics
from gui import frmapplied
from gui import frmactive
from gui import frmsetup
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import gui.config as config
from gui.theme import dark_png_paths, light_png_paths, light_logo,dark_logo, DARK_THEME, LIGHT_THEME
# Global variables
summary_frame = None
applied_frame = None
analytics_frame = None
active_frame = None  
selected_button_index = None
main_frame = None  
frames = {}  # Store frames to switch between them
buttons = []  # Store navigation buttons
logo_path = None
def create_nav_button(parent, text, image_path=None, command=None):
    if image_path:
        img = Image.open(image_path)
        # Resize img
        img = img.resize((25, 25), Image.Resampling.LANCZOS) 
        # Convert img to PhotoImage 
        img = ImageTk.PhotoImage(img)
        button = tk.Button(parent,
                           text=text,
                           image=img,
                           compound="left",
                           width=200,
                           height=50,
                           bg=current_theme['backgroundtheme'],
                           fg=current_theme['foreground'],
                           bd=0,
                           font=('MS Sans Serif', 13),
                           activebackground=current_theme['button_select_bg'],
                           activeforeground=current_theme['foreground'],
                           command=command,
                           padx=10,
                           anchor='w')
        # Save the image reference
        button.image = img 
        return button
    else:
        return tk.Button(parent,
                         text=text,
                         width=200,
                         height=50,
                         bg=current_theme['backgroundtheme'],
                         fg=current_theme['foreground'],
                         bd=0,
                         font=('MS Sans Serif', 13, 'bold'),
                         activebackground='#2e3245',
                         activeforeground='white',
                         command=command,
                         anchor='w')
# Function to select a button
def select_button(index):
    global selected_button_index
    if selected_button_index is not None:
        buttons[selected_button_index].config(bg=current_theme['backgroundtheme'], fg=current_theme['foreground'])  
    selected_button_index = index
    buttons[index].config(bg=current_theme['button_select_bg'], fg=current_theme['foreground'])  
# Create main frame
def create_main_frame(root):
    global current_theme, logo_path
    if config.current_theme == "Dark":
        current_theme = DARK_THEME
        png_paths = dark_png_paths
        logo_path = dark_logo
    else:
        current_theme = LIGHT_THEME
        png_paths = light_png_paths
        logo_path = light_logo
    global main_frame, active_frame, buttons, frames
    # Destroy main_frame if it exists
    if main_frame:
        main_frame.destroy()
    # Create main_frame
    main_frame = tk.Frame(root, bg=current_theme['backgroundtheme'])
    main_frame.pack(side='top', fill='both', expand=True)
    # Create nav_frame
    nav_height_px = 680
    nav_relheight = nav_height_px / 720
    nav_frame = tk.Frame(main_frame, bg=current_theme['backgroundtheme'], bd=0)
    nav_frame.place(relx=0, rely=(1 - nav_relheight) / 2, relwidth=0.2, relheight=nav_relheight)
    nav_right_border = tk.Frame(nav_frame, bg=current_theme['line'], width=3)
    nav_right_border.pack(side='right', fill='y')
    # Create a frame to contain buttons
    buttons_frame = tk.Frame(nav_frame, bg=current_theme['backgroundtheme'])
    buttons_frame.pack(side="top")
    nav_buttons = [
        ("Home", lambda: on_button_click(0, root, "Home"), png_paths[0]),
        ("AI Summary", lambda: on_button_click(1, root, "AI Summary"), png_paths[1]),
        ("Analytics", lambda: on_button_click(2, root, "Analytics"), png_paths[2]),
        ("CV/Resume", lambda: on_button_click(3, root, "CV/Resume"), png_paths[3]),
        ("Exit server", lambda: on_button_click(4, root, "Exit server"), png_paths[4]),
    ]
    buttons = []  # Reset the buttons list
    for index, (text, command, image_path) in enumerate(nav_buttons):
        button = create_nav_button(buttons_frame, text, image_path=image_path, command=command)
        button.pack(fill='x')
        buttons.append(button)
    # Create active_frame
    active_frame = tk.Frame(main_frame, bg=current_theme['backgroundtheme'], bd=0)
    active_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
    def blink_text():
        current_text = label_welcome.cget("text")
        if current_text.endswith("_"):
            label_welcome.config(text="Welcome to") 
        else:
            label_welcome.config(text="Welcome to_")
        label_welcome.after(500, blink_text)
    # Label image below label_welcome
    photo = tk.PhotoImage(file=logo_path)
    label_image = tk.Label(active_frame, image=photo, bg=current_theme['backgroundtheme'], bd=0, relief='flat')
    label_image.image = photo
    label_image.pack(side='top', expand=True)
    # Label welcome
    label_welcome = tk.Label(active_frame, text="Welcome to_", bg=current_theme['backgroundtheme'], fg=current_theme['welcome'], font=('Berlin Sans FB Demi', 25, 'bold'))
    label_welcome.place(x=280, y=240)
    label_welcome.lift()
    blink_text()
    return main_frame
# Function to handle button click event
def on_button_click(index, root, frame_name):
    global main_frame, frames
    select_button(index)
    
    if frame_name == "Exit server":
        # Message box to confirm exit
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            dt = frmsetup.create_datasetup_frame(root)
            frames.clear()
            import gc
            gc.collect()
            if main_frame:
                main_frame.destroy()
    else:
        switch_frame(root, frame_name)
# Function to switch between frames
def switch_frame(root, frame_name):
    global frames, active_frame, logo_path
    # Hiding current frame
    if active_frame:
        active_frame.place_forget()
    # Check list existing frames
    if frame_name not in frames:
        if frame_name == "Home":
            frames[frame_name] = frmactive.create_active_frame(root,logo_path)
        elif frame_name == "AI Summary":
            frames[frame_name] = frmsummary.create_summary_frame(root)
        elif frame_name == "Analytics":
            frames[frame_name] = frmanalytics.create_analytics_frame(root)
        elif frame_name == "CV/Resume":
            frames[frame_name] = frmapplied.create_applied_frame(root)
    # Display the selected frame
    active_frame = frames[frame_name]
    active_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
    if frame_name == "Analytics" and hasattr(active_frame, 'refresh_treeview'):
        active_frame.refresh_treeview()
    if frame_name == "CV/Resume" and hasattr(active_frame, 'refresh_treeview_applied'):
        active_frame.refresh_treeview_applied()