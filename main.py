import tkinter


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 22
SHORT_BREAK_MIN = 8
LONG_BREAK_MIN = 30
reps = 4
timer = ''
timer2 = -1
started = False
paused = False
session_time = -1


# --------------------------- START/PAUSE THE WHOLE COUNTDOWN --------
# should not be possible to press the start button multiple times and increase the reps.

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
    global reps, timer2, started
    reps = 1
    global timer
    window.after_cancel(timer)
    title.config(text="Timer", fg=GREEN)
    canvas.itemconfig(countdown_text, text=f"00:00")
    check_mark.config(text="")
    timer2 = 0
    total_time_label.config(text=f"Total time: 00:00")
    started = 0
    started = False
    start_button.config(text='Start')

# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    global reps, session_time
    session_time = -1
    if reps % 8 == 0:
        title.config(text="Break", fg=RED)
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
        countdown(WORK_MIN * 60)
        reps += 1
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(counter):
    global timer2, session_time
    if counter >= 0:
        minutes = counter // 60
        seconds = counter % 60
        global timer, paused
        if not paused:
            canvas.itemconfig(countdown_text, text=f"{minutes:02}:{seconds:02}")
            timer = window.after(1000, countdown, counter-1)
            # total_time = int(timer[6:])
            # total_minutes = total_time // 60
            # total_seconds = total_time % 60
            timer2 += 1
            session_time += 1
            timer2_hours = timer2 // 3600
            timer2_minutes = (timer2 % 3600) // 60
            timer2_seconds = timer2 % 60
            total_time_label.config(text=f'Total time: {timer2_hours:02}:{timer2_minutes:02}:{timer2_seconds:02}')
            # total_time_label.config(text=f'Total time: {total_minutes:02}:{total_seconds:02}')
        else:
            timer = window.after(1000, countdown, counter)
    else:
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

canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = tkinter.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
countdown_text = canvas.create_text(100, 134, text="00:00", fill='white', font=(FONT_NAME, 26, "bold"))
canvas.grid(row=2, column=2)

start_button = tkinter.Button(text="Start", command=pomodoro_start, width=6)
start_button.grid(row=3, column=1)

check_mark = tkinter.Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 24))
check_mark.grid(row=4, column=2)

reset_button = tkinter.Button(text="Reset", command=timer_reset, width=6)
reset_button.grid(row=3, column=3)


window.mainloop()
