import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
from data.DAO.applicantDAO import ApplicantDAO
from data.DAO.expDAO import expDAO
from module.apply_theme import apply_theme
canvas = None
fig = None
def setup_chart(chart_frame):
    global canvas, fig
    theme = apply_theme()
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor(theme['themechart'])
    ax.set_facecolor(theme['themechart']) 
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
    ax.tick_params(axis='x', colors=theme['foreground'])
    ax.tick_params(axis='y', colors=theme['foreground'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.grid(True, color='gray', linestyle='--', linewidth=0.5)
    toolbar = NavigationToolbar2Tk(canvas,chart_frame)
    toolbar.grid(row=1, column=0, sticky='nsew')
    toolbar.update()
def plot_data(jobrole):
    global canvas, bars, fig, ax, annot
    theme = apply_theme()
    # Get data
    dao = ApplicantDAO.get_instance()
    data = dao.fetch_applicant_by_job_role(jobrole)
    if data is None:
        return
    exp_dao = expDAO.get_instance()
    categories = exp_dao.fetch_exp_name()
    # Create DataFrame
    df = pd.DataFrame(data, columns=['name', 'phone', 'email', 'gpa', 'exp', 'job_role'])
    exp_counts = df['exp'].value_counts()
    categories = [cat[0] for cat in categories]
    values = pd.Series(exp_counts).reindex(categories, fill_value=0)
    # print("Values:", values)
    # Clear existing plot
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_facecolor(theme['themechart'])
    ax.tick_params(axis='y', colors=theme['foreground'])
    ax.tick_params(axis='x', colors=theme['foreground'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.grid(True, color='gray', linestyle='--', linewidth=0.5)
    ax.set_yticks(range(0, int(max(values)) + 2, 1))
    bars = ax.bar(categories, values.values, color='#dffa4c')
    # Config popup
    annot = ax.annotate("", xy=(0, 0), xytext=(0, 5), textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5),
                        arrowprops=dict(arrowstyle="->", color='yellow'))
    annot.set_visible(False)
    def update_annot(bar):
        x_value = bar.get_x() + bar.get_width() / 2
        y_value = bar.get_height()
        annot.xy = (x_value, y_value)
        annot.set_text(f"x={x_value:.2f}, y={y_value}")
        annot.set_visible(True)
    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            for bar in bars:
                if bar.contains(event)[0]:
                    update_annot(bar)
                    fig.canvas.draw_idle()
                    return
        if vis:
            annot.set_visible(False)
            fig.canvas.draw_idle()
    fig.canvas.mpl_connect("motion_notify_event", hover)
    canvas.draw()
    return df
# Update chart function
def update_chart(exp, exp_dao, df):
    global bars, fig, ax, annot
    theme = apply_theme()
    categories = [cat[0] for cat in exp_dao.fetch_exp_name()]
    values = pd.Series(df['exp'].value_counts()).reindex(categories, fill_value=0)
    # Clear existing bars
    if bars is not None:
        for bar in bars:
            bar.remove()
    bars = ax.bar(categories, values.values, color='#dffa4c')
    colors = [theme['barhide']] * len(categories)
    if exp in categories:
        index = categories.index(exp)
        colors[index] = '#dffa4c'
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    ax.set_yticks(range(0, int(max(values)) + 2, 1))
    canvas.draw()
def clear_chart():
    global canvas, fig, ax
    theme = apply_theme()
    ax.clear()
    ax.set_facecolor(theme['themechart'])
    ax.tick_params(axis='x', colors=theme['foreground'])
    ax.tick_params(axis='y', colors=theme['foreground'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.grid(True, color='gray', linestyle='--', linewidth=0.5)
    canvas.draw()