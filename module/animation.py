# follow x axis
def sliding(current_frame, next_frame):
    current_frame.place_forget()
    next_frame.place(x=400, y=76) 
    for x in range(700, 385, -2):  
        next_frame.place(x=x, y=76)
        next_frame.update()
# slide scroll up   
def slide_up_and_hide(next_frame):
    from module.state_frame import on_widgets
    from gui.frmapplied import exp_frame, job_role_frame, gpa_frame_from, gpa_frame_to, boder_frame_delete, boder_frame_update, filter_frame
    for y in range(0, -700, -20):  
        next_frame.place(x=0, y=y)
        next_frame.update()
    next_frame.place(x=0, y=-next_frame.winfo_height())
    next_frame.update()
    next_frame.destroy()
    on_widgets([exp_frame, job_role_frame, gpa_frame_from, gpa_frame_to, boder_frame_delete, boder_frame_update, filter_frame])