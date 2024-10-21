import tkinter as tk
from module.apply_theme import apply_theme
def create_active_frame(master,path):
    theme = apply_theme()
    active_frame = tk.Frame(master, bg=theme['backgroundtheme'])
    active_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
    def blink_text():
        current_text = label_welcome.cget("text")
        if current_text.endswith("_"):
            label_welcome.config(text="Welcome to")
        else:
            label_welcome.config(text="Welcome to_")
        # Loop the blink_text function after 500ms
        label_welcome.after(500, blink_text)
    # Label image below label_welcome
    photo = tk.PhotoImage(file=path)
    label_image = tk.Label(active_frame, image=photo, bg=theme['backgroundtheme'], bd=0,relief='flat')
    label_image.image = photo
    label_image.pack(side='top', expand=True)
    # Label welcome
    label_welcome = tk.Label(active_frame, text="Welcome to_", bg=theme['backgroundtheme'], fg=theme['welcome'], font=('Berlin Sans FB Demi', 25, 'bold'))
    label_welcome.place(x=280, y=240)
    label_welcome.lift()
    blink_text()
    return active_frame