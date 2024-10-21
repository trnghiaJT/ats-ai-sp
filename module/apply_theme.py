import gui.config as config
from gui.theme import DARK_THEME, LIGHT_THEME

def apply_theme():
    if config.current_theme == "Dark":
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME
    return current_theme