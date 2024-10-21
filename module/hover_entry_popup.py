import tkinter as tk
from module.apply_theme import apply_theme

class HoverEntryPopup:
    def __init__(self, root):
        self.root = root
        self.popup = None  
    def create_entry(self, parent, text):
        theme = apply_theme()
        # Create Text widget
        entry = tk.Text(parent,wrap='none', 
                        bg=theme['entry_dark'], fg=theme['entry_dark_fg'],  
                        font=('Arial', 13), 
                        highlightbackground=theme['highlightbackground'],
                        highlightthickness=1,
                        bd=0, insertbackground=theme['foreground'],state='disabled',spacing3=10)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        entry.insert('1.0', text)
        # Hover event (enter) and (leave)
        entry.bind("<Enter>", lambda event: self.show_popup(event, entry))
        entry.bind("<Leave>", self.hide_popup)
        # Event when user change content
        entry.bind("<KeyRelease>", lambda event: self.update_popup(entry))
        return entry
    def create_entry_save(self, parent, text):
        # Create Text widget
        theme = apply_theme()
        entry = tk.Text(parent,wrap='none', 
                        bg=theme['entry_dark'], fg=theme['entry_dark_fg'], font=('Arial', 13), bd=0, 
                        insertbackground=theme['entry_fg'],spacing3=10)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        entry.insert('1.0', text)
        # Hover event (enter) and (leave)
        entry.bind("<Enter>", lambda event: self.show_popup(event, entry))
        entry.bind("<Leave>", self.hide_popup)
        # Event when user change content
        entry.bind("<KeyRelease>", lambda event: self.update_popup(entry))
        return entry
    def show_popup(self, event, entry):
        # Show popup when mouse enter entry
        theme = apply_theme()
        if not self.popup:
            self.popup = tk.Toplevel(self.root)
            self.popup.overrideredirect(True)
            self.popup.geometry(f"+{event.x_root + 20}+{event.y_root + 20}")
            # Create label to show content of entry
            label = tk.Label(self.popup, text=entry.get('1.0', 'end-1c'), bg=theme['background'], fg=theme['foreground'], font=('Arial', 13), padx=10, pady=5,wraplength=300)
            label.pack()
    def update_popup(self, entry):
        theme = apply_theme()
        # Update content of popup when user change content of entry
        if self.popup:
            for widget in self.popup.winfo_children():
                widget.destroy()
            label = tk.Label(self.popup, text=entry.get('1.0', 'end-1c'), bg=theme['background'], fg=theme['foreground'], font=('Arial', 13), padx=10, pady=5)
            label.pack()
    def hide_popup(self, event):
        # Hide popup when mouse leave entry
        if self.popup:
            self.popup.destroy()
            self.popup = None