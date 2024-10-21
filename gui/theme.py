DARK_THEME = {
    'background': '#353a4a',
    'backgroundtheme': '#262c3c',
    'foreground': '#fdfdfd',
    'highlightbackground':"white",
    'boder_button':'#2e3245',
    'button_bg':'#262c3c',
    'entry_bg': '#ffffff',
    'entry_fg': '#222222',
    'welcome':'#ffffff',
    'line':'#353a4a',
    'button_select_bg':'#2e3245',
    'themechart':'#2e3245',
    'barhide':'#353a4a',
    'entry_dark':'#2e3245',
    'entry_dark_fg':'#fdfdfd',
    'view_text_bg' : '#303147',
}
LIGHT_THEME = {
    'background': '#ffffff',
    'backgroundtheme': '#ebeef3',
    'highlightbackground':"#bac1cd",
    'boder_button':'#bac1cd',
    'button_bg':'#ffffff',
    'foreground': '#000000',
    'entry_bg': '#ffffff',
    'entry_fg': '#000000',
    'welcome':'#29313e',
    'line':'#bac1cd',
    'button_select_bg':'#ffffff',
    'themechart':'#ffffff',
    'barhide':'#ebeef3',
    'entry_dark':'#ffffff',
    'entry_dark_fg':'#222222',
    'view_text_bg' : '#ffffff',
}
light_png_paths = [
    "img\light\house-solid.png",
    "img\light\sparkles.png",
    "img\light\chart-simple-solid.png",
    "img\light\database-solid.png",
    "img\light\out.png",
]
dark_png_paths = [
    "img\dark\house-solid.png",
    "img\dark\sparkles.png",
    "img\dark\chart-simple-solid.png",
    "img\dark\database-solid.png",
    "img\dark\out.png",
]
light_logo = "img\light\cvlogo.png"
dark_logo = "img\dark\cvlogo.png"
import tkinter as tk
from tkinter import ttk
def tree_combo_dark():
    # Treeview style
    styletree = ttk.Style()
    styletree.theme_use("clam")
    styletree.layout(
        'Edge.Treeview',
        [('Edge.Treeview.treearea', {'sticky': 'nsew'})],
    )
    styletree.configure("Edge.Treeview",
                        background="#2e3245",
                        foreground="#fdfdfd",
                        bordercolor="#2e3245",
                        fieldbackground="#2e3245",
                        rowheight=30,
                        highlightthickness=0, 
                        bd=0)
    styletree.configure("Edge.Treeview.Heading",
                        background="#2e3245",
                        foreground="#fdfdfd",
                        relief='flat')
    styletree.map('Edge.Treeview',
                  background=[('selected', '#dffa4c')],
                  foreground=[('selected', 'black')],
                 )
    # Combobox style
    styletree.configure('TCombobox',
                        fieldbackground='#2e3245',
                        background='#2e3245',
                        foreground='#fdfdfd',
                        bordercolor='#2e3245',
                        insertbackground='#fdfdfd')
    # Apply root-wide option defaults (these affect all Tkinter widgets globally)
    tk._default_root.option_add("*TCombobox*fieldbackground", '#2e3245')
    tk._default_root.option_add("*TCombobox*font", "Calibri 13")
    tk._default_root.option_add("*TCombobox*Listbox*Background", '#303147')  
    tk._default_root.option_add("*TCombobox*Listbox*Foreground", '#fdfdfd')  
    tk._default_root.option_add("*TCombobox*selectBackground", '#dffa4c')  
    tk._default_root.option_add("*TCombobox*selectForeground", '#303147')  
    tk._default_root.option_add("*TCombobox*Listbox*highlightColor", '#303147')
    tk._default_root.option_add("*Button.cursor", "hand2")
def tree_combo_light():
        # Treeview style
    styletree = ttk.Style()
    styletree.theme_use("clam")
    styletree.layout(
        'Edge.Treeview',
        [('Edge.Treeview.treearea', {'sticky': 'nsew'})],
    )
    styletree.configure("Edge.Treeview",
                        background="#ffffff",
                        foreground="#000000",
                        bordercolor="#bac1cd",
                        fieldbackground="#bac1cd",
                        rowheight=30,
                        highlightthickness=0, 
                        bd=0)
    styletree.configure("Edge.Treeview.Heading",
                        background="#ffffff",
                        foreground="#000000",
                        relief='flat')
    styletree.map('Edge.Treeview',
                  background=[('selected', '#dffa4c')],
                  foreground=[('selected', 'black')],
                 )
    # Combobox style
    styletree.configure('TCombobox',
                        fieldbackground='#ffffff',
                        background='#ffffff',
                        foreground='#000000',
                        bordercolor='#ffffff',
                        insertbackground='#fdfdfd')
    # Apply root-wide option defaults (these affect all Tkinter widgets globally)
    tk._default_root.option_add("*TCombobox*fieldbackground", '#ffffff')
    tk._default_root.option_add("*TCombobox*font", "Calibri 13")
    tk._default_root.option_add("*TCombobox*Listbox*Background", '#ffffff')  
    tk._default_root.option_add("*TCombobox*Listbox*Foreground", '#000000')  
    tk._default_root.option_add("*TCombobox*selectBackground", '#dffa4c')  
    tk._default_root.option_add("*TCombobox*selectForeground", '#303147')  
    tk._default_root.option_add("*TCombobox*Listbox*highlightColor", '#303147')
    tk._default_root.option_add("*Button.cursor", "hand2")