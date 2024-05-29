import tkinter

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 20
SHORT_BREAK_MIN = 10
LONG_BREAK_MIN = 30
reps = 1
timer_label = ''
timer_total_time = 0
timer_work_time = 0
started = False
paused = False
working = False

# bugs
# bug when pausing on a changeover
# "still working" button that (1) reverts to working rep without loosing timing,
# and (2) adds the used break time to the working time,
# and (3) adds the extra working time to the later break time? Or a portion of it?

# --------------------------- START/PAUSE THE WHOLE COUNTDOWN --------


def pomodoro_start():
    global started, paused
    if not started:
        started = True
        start_timer()
        start_button.config(text='Pause')
    else:
        if not paused:
            paused = True
            start_button.config(text='Unpause')
        else:
            paused = False
            start_button.config(text='Pause')


# ---------------------------- TIMER RESET ------------------------------- #


def timer_reset():
    global reps, timer_total_time, timer_work_time, started
    reps = 1
    global timer_label
    window.after_cancel(timer_label)
    title.config(text="Timer", fg=GREEN)
    canvas.itemconfig(countdown_text, text=f"00:00")
    check_mark.config(text="")
    timer_total_time = 0
    timer_work_time = 0
    total_time_label.config(text=f"Total time: 00:00")
    work_time_label.config(text=f'Work time: 00:00')
    started = 0
    started = False
    start_button.config(text='Start')

# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    global reps, working
    working = False
    if reps % 8 == 0:
        title.config(text="Long Break", fg=RED)
        countdown(LONG_BREAK_MIN * 60)
        reps = 1
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)
    elif reps % 2 == 0:
        title.config(text="Break", fg=PINK)
        countdown(SHORT_BREAK_MIN * 60)
        reps += 1
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)
    else:
        title.config(text="Work", fg=GREEN)
        working = True
        countdown(WORK_MIN * 60)
        reps += 1
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(counter):
    global timer_total_time, timer_work_time
    if counter > 0:
        minutes = counter // 60
        seconds = counter % 60
        global timer_label, paused
        if not paused:
            canvas.itemconfig(countdown_text, text=f"{minutes:02}:{seconds:02}")
            timer_label = window.after(1000, countdown, counter - 1)

            total_hours = timer_total_time // 3600
            total_minutes = (timer_total_time % 3600) // 60
            total_seconds = timer_total_time % 60
            total_time_label.config(text=f'Total time: {total_hours:02}:{total_minutes:02}:{total_seconds:02}')
            timer_total_time += 1
            if working:
                work_hours = timer_work_time // 3600
                work_minutes = (timer_work_time % 3600) // 60
                work_seconds = timer_work_time % 60
                work_time_label.config(text=f'Time worked: {work_hours:02}:{work_minutes:02}:{work_seconds:02}')
                timer_work_time += 1
        else:
            timer_label = window.after(500, countdown, counter)
    else:
        work_hours = timer_work_time // 3600
        work_minutes = (timer_work_time % 3600) // 60
        work_seconds = timer_work_time % 60
        work_time_label.config(text=f'Time worked: {work_hours:02}:{work_minutes:02}:{work_seconds:02}')
        start_timer()
        if reps % 2 == 0:
            check_mark.config(text="✔" * ((reps-1)//2))


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Pomodoro technique")
window.config(padx=100, pady=50, bg=YELLOW)
# window.geometry('200x200')
# window.resizable(height = None, width = None)


title = tkinter.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
title.grid(row=0, column=2)

total_time_label = tkinter.Label(text='', bg=YELLOW)
total_time_label.grid(row=1, column=2)

work_time_label = tkinter.Label(text='', bg=YELLOW)
work_time_label.grid(row=2, column=2)

canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = tkinter.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
countdown_text = canvas.create_text(100, 134, text="00:00", fill='white', font=(FONT_NAME, 26, "bold"))
canvas.grid(row=3, column=2)

start_button = tkinter.Button(text="Start", command=pomodoro_start, width=6)
start_button.grid(row=4, column=1)

reset_button = tkinter.Button(text="Reset", command=timer_reset, width=6)
reset_button.grid(row=4, column=3)

check_mark = tkinter.Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 24))
check_mark.grid(row=5, column=2)


window.mainloop()
