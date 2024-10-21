from module.animation import slide_up_and_hide

def on_click_outside(event, frame):
    frame_x = frame.winfo_x()
    frame_y = frame.winfo_y()
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()
    if not (frame_x <= event.x <= frame_x + frame_width and frame_y <= event.y <= frame_y + frame_height):
        slide_up_and_hide(frame)
