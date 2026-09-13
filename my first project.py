import tkinter as tk
import webbrowser
import subprocess
import sys
import json
import os
from datetime import datetime
from plyer import notification


timer_job = None
window = tk.Tk()
window.title("task_manager")
window.geometry("900x820")
task_page = tk.Frame(window)
timer_page = tk.Frame(window)
task_page.pack(fill="both", expand=True)
timer_seconds = 0
timer_running = False
# ---------------- THEME SYSTEM ----------------

current_theme = "normal"

themes = {
    "normal": {
        "bg": "#f0f0f0",
        "task_bg": "#ffffff",
        "text": "#222222",
        "secondary_text": "#555555",
        "button_bg": "#111111",
        "button_fg": "#ffffff",
        "button_active": "#333333",
        "border": "#dddddd",
        "entry_bg": "#ffffff",
        "entry_fg": "#222222"
    },

    "dark": {
        "bg": "#1e1e1e",
        "task_bg": "#2b2b2b",
        "text": "#ffffff",
        "secondary_text": "#bdbdbd",
        "button_bg": "#111111",
        "button_fg": "#ffffff",
        "button_active": "#333333",
        "border": "#444444",
        "entry_bg": "#2b2b2b",
        "entry_fg": "#ffffff"
    },

    "light": {
        "bg": "#ffffff",
        "task_bg": "#f5f5f5",
        "text": "#222222",
        "secondary_text": "#666666",
        "button_bg": "#222222",
        "button_fg": "#ffffff",
        "button_active": "#444444",
        "border": "#dddddd",
        "entry_bg": "#ffffff",
        "entry_fg": "#222222"
    },

    "ocean": {
        "bg": "#dff6ff",
        "task_bg": "#ffffff",
        "text": "#123456",
        "secondary_text": "#39708f",
        "button_bg": "#168aad",
        "button_fg": "#ffffff",
        "button_active": "#126782",
        "border": "#9ed9ec",
        "entry_bg": "#ffffff",
        "entry_fg": "#123456"
    },

    "forest": {
        "bg": "#e8f5e9",
        "task_bg": "#ffffff",
        "text": "#1b4332",
        "secondary_text": "#52796f",
        "button_bg": "#2d6a4f",
        "button_fg": "#ffffff",
        "button_active": "#24563f",
        "border": "#b7d7c1",
        "entry_bg": "#ffffff",
        "entry_fg": "#1b4332"
    },

    "sunset": {
        "bg": "#fff1e6",
        "task_bg": "#ffffff",
        "text": "#6d3b2a",
        "secondary_text": "#9a6250",
        "button_bg": "#d96c3d",
        "button_fg": "#ffffff",
        "button_active": "#b9572d",
        "border": "#f0c2ad",
        "entry_bg": "#ffffff",
        "entry_fg": "#6d3b2a"
    }
}
#timer
timer_title = tk.Label(
    timer_page,
    text="TIMER",
    font=("Arial", 36, "bold"),
    fg="#222222",
    bg="#f0f0f0"
)

timer_title.pack(pady=(10, 5))

timer_label = tk.Label(
    timer_page,
    text="00:00:00",
    font=("Arial", 58, "bold"),
    fg="#111111",
    bg="#f0f0f0"
)

timer_label.pack(pady=30)
time_input_frame = tk.Frame(timer_page)
time_input_frame.pack(pady=20)

def update_timer_display():
    hours = timer_seconds // 3600
    minutes = (timer_seconds % 3600) // 60
    seconds = timer_seconds % 60

    timer_label.config(
        text=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    )
hour_box = tk.Spinbox(
    time_input_frame,
    from_=0,
    to=99,
    width=3,
    font=("Arial", 23),
    justify="center",
    format="%02.0f",
    state="readonly",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground="#d0d0d0"
)

hour_box.pack(side="left", padx=5, ipady=5)

timer_colon_1 = tk.Label(
    time_input_frame,
    text=":",
    font=("Arial", 23, "bold"),
    bg="#f0f0f0",
    fg="#555555"
)

timer_colon_1.pack(side="left")

minute_box = tk.Spinbox(
    time_input_frame,
    from_=0,
    to=59,
    width=3,
    font=("Arial", 23),
    justify="center",
    format="%02.0f",
    state="readonly",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground="#d0d0d0"
)

minute_box.pack(side="left", padx=5, ipady=5)

timer_colon_2 = tk.Label(
    time_input_frame,
    text=":",
    font=("Arial", 23, "bold"),
    bg="#f0f0f0",
    fg="#555555"
)

timer_colon_2.pack(side="left")

second_box = tk.Spinbox(
    time_input_frame,
    from_=0,
    to=59,
    width=3,
    font=("Arial", 23),
    justify="center",
    format="%02.0f",
    state="readonly",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground="#d0d0d0"
)

second_box.pack(side="left", padx=5, ipady=5)

# ---------------- THEME HELPERS ----------------

def get_theme():
    return themes[current_theme]


def style_button(button_widget):
    theme = get_theme()

    button_widget.config(
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"],
        relief="flat",
        bd=0
    )


def style_spinbox(spinbox_widget):
    theme = get_theme()

    if current_theme in ("normal", "light"):
        spinbox_widget.config(
            bg="#ffffff",
            fg=theme["entry_fg"],
            readonlybackground="#ffffff",

            # قسمت فلش‌ها
            buttonbackground="#ffffff",

            activebackground="#eeeeee",

            # خط دور Spinbox
            highlightbackground="#000000",
            highlightcolor="#000000",
            highlightthickness=2,

            insertbackground=theme["entry_fg"],

            buttonuprelief="flat",
            buttondownrelief="flat"
        )

    else:
        spinbox_widget.config(
            bg=theme["entry_bg"],
            fg=theme["entry_fg"],
            readonlybackground=theme["entry_bg"],

            # قسمت فلش‌ها
            buttonbackground=theme["button_bg"],

            activebackground=theme["button_active"],

            # خط دور Spinbox
            highlightbackground=theme["border"],
            highlightcolor=theme["button_active"],
            highlightthickness=3,

            insertbackground=theme["entry_fg"],

            buttonuprelief="flat",
            buttondownrelief="flat"
        )


def set_timer():
    global timer_seconds
    global timer_running
    global timer_job

    hours = int(hour_box.get())
    minutes = int(minute_box.get())
    seconds = int(second_box.get())

    if hours == 0 and minutes == 0 and seconds == 0:
        return

    timer_running = False

    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    timer_seconds = (
        hours * 3600
        + minutes * 60
        + seconds
    )

    update_timer_display()
def countdown():
    global timer_seconds
    global timer_running
    global timer_job

    if not timer_running:
        timer_job = None
        return

    if timer_seconds > 0:
        timer_seconds -= 1
        update_timer_display()

        timer_job = window.after(1000, countdown)

    else:
        timer_running = False
        timer_job = None

        notification.notify(
            title="Task Manager",
            message="Timer finished! 🔔",
            timeout=10
        )
def start_timer():
    global timer_running

    if timer_running:
        return

    if timer_seconds <= 0:
        return

    timer_running = True
    countdown()
def pause_timer():
    global timer_running
    global timer_job

    timer_running = False

    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None
def reset_timer():
    global timer_seconds
    global timer_running
    global timer_job

    timer_running = False

    if timer_job is not None:
        window.after_cancel(timer_job)
        timer_job = None

    timer_seconds = 0
    update_timer_display()

# ---------------- TIMER BUTTONS ----------------

timer_buttons_frame = tk.Frame(
    timer_page,
    bg="#f0f0f0"
)

timer_buttons_frame.pack(pady=20)

start_button = tk.Button(
    timer_buttons_frame,
    text="START",
    font=("Arial", 13, "bold"),
    width=10,
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=8,
    pady=8,
    command=start_timer
)

start_button.pack(side="left", padx=5)

pause_button = tk.Button(
    timer_buttons_frame,
    text="PAUSE",
    font=("Arial", 13, "bold"),
    width=10,
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=8,
    pady=8,
    command=pause_timer
)

pause_button.pack(side="left", padx=5)

reset_button = tk.Button(
    timer_buttons_frame,
    text="RESET",
    font=("Arial", 13, "bold"),
    width=10,
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=8,
    pady=8,
    command=reset_timer
)

reset_button.pack(side="left", padx=5)

set_time_button = tk.Button(
    timer_buttons_frame,
    text="SET TIME",
    font=("Arial", 13, "bold"),
    width=10,
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=8,
    pady=8,
    command=set_timer
)

set_time_button.pack(side="left", padx=5)

#somethings
tasks = []
selected_time = None
time_window = None
FILE_NAME = "tasks.json"
notified_tasks = set()



#2 page
def show_task_page():
    close_theme_menu()

    timer_page.pack_forget()
    task_page.pack(fill="both", expand=True)


def show_timer_page():
    close_theme_menu()

    task_page.pack_forget()
    timer_page.pack(fill="both", expand=True)

bottom_bar = tk.Frame(
    window,
    bg="#f0f0f0"
)
bottom_bar.pack(side="bottom", fill="x")
task_button = tk.Button(
    bottom_bar,
    text="TASK",
    font=("Arial", 13, "bold"),
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    pady=8,
    command=show_task_page
)
timer_button = tk.Button(
    bottom_bar,
    text="TIMER",
    font=("Arial", 13, "bold"),
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    pady=8,
    command=show_timer_page
)

task_button.pack(side="left", expand=True, fill="x")
timer_button.pack(side="left", expand=True, fill="x")
# ---------------- THEME MENU ----------------

theme_menu = tk.Frame(
    window,
    bg="#1e1e1e",
    bd=0,
    highlightthickness=2,
    highlightbackground="#555555"
)


# ---------------- NORMAL ----------------
def set_normal_theme():
    close_theme_menu()
    message_premium_frame.config(
    bg="#f0f0f0"
)

    premium_frame.config(
    bg="#f0f0f0"
)

    message_Lable.config(
    bg="#f0f0f0",
    fg="black"
)

    button_2.config(
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white"
)


    window.config(bg="#f0f0f0")
    task_page.config(bg="#f0f0f0")
    timer_page.config(bg="#f0f0f0")
    bottom_bar.config(bg="#f0f0f0")

    label.config(
        bg="#f0f0f0",
        fg="black"
    )

    timer_title.config(
        bg="#f0f0f0",
        fg="black"
    )

    timer_label.config(
        bg="#f0f0f0",
        fg="black"
    )

normal_button = tk.Button(
    theme_menu,
    text="🏠  Normal",
    font=("Arial", 13),
    width=14,
    anchor="w",
    bg="#2b2b2b",
    fg="white",
    activebackground="#3d3d3d",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=lambda: change_theme("normal")
)

normal_button.pack(fill="x", padx=8, pady=3)



# ---------------- DARK ----------------
def set_dark_theme():
    close_theme_menu()

    # رنگ‌های اصلی
    dark_bg = "#1e1e1e"
    dark_text = "#ffffff"
    dark_secondary = "#bdbdbd"
    dark_button = "#111111"
    dark_active = "#333333"

    # Window و Pageها
    window.config(bg=dark_bg)
    task_page.config(bg=dark_bg)
    timer_page.config(bg=dark_bg)
    bottom_bar.config(bg=dark_bg)

    # ---------- TASK PAGE ----------
    label.config(
        bg=dark_bg,
        fg=dark_text
    )

    input_frame.config(
        bg=dark_bg
    )

    tasks_frame.config(
        bg=dark_bg
    )

    message_premium_frame.config(
        bg=dark_bg
    )

    premium_frame.config(
        bg=dark_bg
    )

    message_Lable.config(
        bg=dark_bg,
        fg=dark_secondary
    )

    # Entry
    entry.config(
        bg="#2b2b2b",
        fg=dark_text,
        insertbackground=dark_text,
        highlightbackground="#555555",
        highlightcolor="#777777"
    )

    # Add Time
    time_button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    # Add
    button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    # Premium
    button_2.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    # ---------- TIMER PAGE ----------
    timer_title.config(
        bg=dark_bg,
        fg=dark_text
    )

    timer_label.config(
        bg=dark_bg,
        fg=dark_text
    )

    time_input_frame.config(
        bg=dark_bg
    )

    timer_buttons_frame.config(
        bg=dark_bg
    )

    # ---------- TIMER BUTTONS ----------
    start_button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    pause_button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    reset_button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    set_time_button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    # ---------- BOTTOM BAR ----------
    task_button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    timer_button.config(
        bg=dark_button,
        fg=dark_text,
        activebackground=dark_active,
        activeforeground=dark_text
    )

    # ---------- THEME BUTTON ----------
    theme_button.config(
        bg="#111111",
        fg="white",
        activebackground="#333333",
        activeforeground="white"
    )

dark_button = tk.Button(
    theme_menu,
    text="☾ Dark",
    font=("Arial", 12),
    width=12,
    anchor="w",
    bg="#2b2b2b",
    fg="white",
    activebackground="#3d3d3d",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=lambda: change_theme("dark")
)

dark_button.pack(fill="x", padx=8, pady=3)


# ---------------- LIGHT ----------------

light_button = tk.Button(
    theme_menu,
    text="☀  Light",
    font=("Arial", 13),
    width=14,
    anchor="w",
    bg="#2b2b2b",
    fg="white",
    activebackground="#3d3d3d",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=lambda: change_theme("light")
)

light_button.pack(fill="x", padx=8, pady=3)

# ---------------- OCEAN ----------------

ocean_button = tk.Button(
    theme_menu,
    text="≋  Ocean",
    font=("Arial", 13),
    width=14,
    anchor="w",
    bg="#2b2b2b",
    fg="white",
    activebackground="#3d3d3d",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=lambda: change_theme("ocean")
)

ocean_button.pack(fill="x", padx=8, pady=3)

# ---------------- FOREST ----------------

forest_button = tk.Button(
    theme_menu,
    text="♣  Forest",
    font=("Arial", 13),
    width=14,
    anchor="w",
    bg="#2b2b2b",
    fg="white",
    activebackground="#3d3d3d",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=lambda: change_theme("forest")
)

forest_button.pack(fill="x", padx=8, pady=3)
# ---------------- SUNSET ----------------

sunset_button = tk.Button(
    theme_menu,
    text="◐  Sunset",
    font=("Arial", 13),
    width=14,
    anchor="w",
    bg="#2b2b2b",
    fg="white",
    activebackground="#3d3d3d",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=lambda: change_theme("sunset")
)

sunset_button.pack(fill="x", padx=8, pady=3)

# ---------------- THEME BUTTON ----------------

theme_menu_open = False


def close_theme_menu():
    global theme_menu_open

    theme_menu.place_forget()
    theme_menu_open = False


def show_theme_menu():
    global theme_menu_open

    if theme_menu_open:
        close_theme_menu()
        return

    theme_menu.place(
        relx=0.97,
        rely=0.07,
        anchor="ne"
    )

    theme_menu_open = True


theme_button = tk.Button(
    window,
    text="T",
    font=("Arial", 14, "bold"),
    width=3,
    height=1,
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    highlightthickness=0,
    command=show_theme_menu
)

theme_button.place(
    relx=0.97,
    rely=0.02,
    anchor="ne"
)
#notif
def schedule_task_notification(index, task_name, task_time):
    if task_time == "No time":
        return

    hour, minute_ampm = task_time.split(":", 1)
    minute, am_pm = minute_ampm.strip().split(" ")

    hour = int(hour)
    minute = int(minute)

    if am_pm == "PM" and hour != 12:
        hour += 12

    if am_pm == "AM" and hour == 12:
        hour = 0

    time_24 = f"{hour:02d}:{minute:02d}"

    python_path = sys.executable.replace(
        "python.exe",
        "pythonw.exe"
    )

    notifier_path = r"D:\task manager\notifier.py"

    task_name_windows = f"TaskManager_Notification_{index}"

    command = f'"{python_path}" "{notifier_path}" "{task_name}"'

    subprocess.run(
        [
            "schtasks",
            "/create",
            "/sc", "daily",
            "/tn", task_name_windows,
            "/tr", command,
            "/st", time_24,
            "/f"
        ],
        capture_output=True,
        text=True
    )


def delete_scheduled_notification(index):
    task_name_windows = f"TaskManager_Notification_{index}"

    subprocess.run(
        [
            "schtasks",
            "/delete",
            "/tn", task_name_windows,
            "/f"
        ],
        capture_output=True,
        text=True
    )
#site
def open_site():
    webbrowser.open("https://www.digikala.com")
#dlete def
def delete_task(index):
    old_count = len(tasks)

    # حذف scheduled task مربوط به task حذف‌شده
    delete_scheduled_notification(index)

    # حذف از لیست
    tasks.pop(index)

    # taskهای بعدی یک شماره عقب می‌آیند
    for old_index in range(index + 1, old_count):
        old_task_name, old_task_time = tasks[old_index - 1]

        # حذف scheduled task با شماره قبلی
        delete_scheduled_notification(old_index)

        # ساخت دوباره با شماره جدید
        schedule_task_notification(
            old_index - 1,
            old_task_name,
            old_task_time
        )

    save_tasks()
    show_tasks()

#show tasks
def show_tasks():

    theme = themes[current_theme]

    for widget in tasks_frame.winfo_children():
        widget.destroy()

    for i, (task, time) in enumerate(tasks, start=1):

        row = tk.Frame(
            tasks_frame,
            bg=theme["task_bg"],
            highlightthickness=1,
            highlightbackground=theme["border"]
        )

        row.pack(
            pady=6,
            padx=10,
            fill="x"
        )

        task_label = tk.Label(
            row,
            text=f"{i}. {task}",
            font=("Arial", 20, "bold"),
            bg=theme["task_bg"],
            fg=theme["text"],
            anchor="w"
        )

        task_label.pack(
            side="left",
            padx=12,
            pady=10,
            expand=True,
            fill="x"
        )

        right_frame = tk.Frame(
            row,
            bg=theme["task_bg"]
        )

        right_frame.pack(
            side="right",
            padx=8
        )

        time_label = tk.Label(
            row,
            text=f"⏰ {time}",
            font=("Arial", 14),
            bg=theme["task_bg"],
            fg=theme["secondary_text"]
        )

        time_label.pack(
            side="right",
            padx=8
        )

        delete_button = tk.Button(
            right_frame,
            text="❌",
            font=("Arial", 11, "bold"),
            width=3,
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            activebackground=theme["button_active"],
            activeforeground=theme["button_fg"],
            relief="flat",
            bd=0,
            padx=5,
            pady=5,
            command=lambda index=i-1: delete_task(index)
        )

        edit_button = tk.Button(
            right_frame,
            text="✏️",
            font=("Arial", 11, "bold"),
            width=3,
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            activebackground=theme["button_active"],
            activeforeground=theme["button_fg"],
            relief="flat",
            bd=0,
            padx=5,
            pady=5,
            command=lambda index=i-1: edit_task(index)
        )

        edit_button.pack(side="left", padx=4)
        delete_button.pack(side="left", padx=4)
# ---------------- TIME PICKER ----------------

def choose_time():
    global selected_time
    global time_window

    theme = get_theme()

    if time_window is not None and time_window.winfo_exists():
        time_window.focus()
        return

    time_window = tk.Toplevel(window)
    time_window.configure(bg=theme["bg"])
    time_window.title("Choose Time")
    time_window.geometry("400x300")
    time_window.resizable(False, False)

    def close_time_window():
        global time_window

        time_window.destroy()
        time_window = None

    time_window.protocol(
        "WM_DELETE_WINDOW",
        close_time_window
    )

    tk.Label(
        time_window,
        text="Choose a time",
        font=("Arial", 24, "bold"),
        bg=theme["bg"],
        fg=theme["text"]
    ).pack(pady=(20, 15))

    time_frame = tk.Frame(
        time_window,
        bg=theme["bg"]
    )

    time_frame.pack(pady=10)

    # ---------- HOUR ----------

    hour_box = tk.Spinbox(
        time_frame,
        from_=1,
        to=12,
        width=3,
        font=("Arial", 22),
        justify="center",
        state="readonly",
        relief="flat",
        bd=0,
        highlightthickness=1
    )

    hour_box.pack(
        side="left",
        padx=5,
        ipady=5
    )

    style_spinbox(hour_box)

    tk.Label(
        time_frame,
        text=":",
        font=("Arial", 22, "bold"),
        bg=theme["bg"],
        fg=theme["secondary_text"]
    ).pack(side="left")

    # ---------- MINUTE ----------

    minute_box = tk.Spinbox(
        time_frame,
        from_=0,
        to=59,
        width=3,
        font=("Arial", 22),
        justify="center",
        format="%02.0f",
        state="readonly",
        relief="flat",
        bd=0,
        highlightthickness=1
    )

    minute_box.pack(
        side="left",
        padx=5,
        ipady=5
    )

    style_spinbox(minute_box)

    tk.Label(
        time_frame,
        text=":",
        font=("Arial", 22, "bold"),
        bg=theme["bg"],
        fg=theme["secondary_text"]
    ).pack(side="left")

    # ---------- AM / PM ----------

    am_pm_box = tk.Spinbox(
        time_frame,
        values=("AM", "PM"),
        width=4,
        font=("Arial", 20),
        justify="center",
        state="readonly",
        relief="flat",
        bd=0,
        highlightthickness=1
    )

    am_pm_box.pack(
        side="left",
        padx=5,
        ipady=5
    )

    style_spinbox(am_pm_box)

    # ---------- SAVE TIME ----------

    def save_time():
        global selected_time

        hour = hour_box.get()
        minute = minute_box.get()
        am_pm = am_pm_box.get()

        selected_time = f"{hour}:{minute} {am_pm}"

        time_button.config(
            text=f"TIME: {selected_time}"
        )

        close_time_window()

    tk.Button(
        time_window,
        text="SET TIME",
        font=("Arial", 13, "bold"),
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"],
        relief="flat",
        bd=0,
        padx=18,
        pady=8,
        command=save_time
    ).pack(pady=25)
# ---------------- EDIT TASK ----------------

def edit_task(index):
    edit_window = tk.Toplevel(window)
    theme = get_theme()

    edit_window.configure(bg=theme["bg"])
    edit_window.title("Edit Task")
    edit_window.geometry("500x350")
    edit_window.resizable(False, False)

    task_entry = tk.Entry(
        edit_window,
        width=25,
        font=("Arial", 20),
        relief="flat",
        bd=0,
        highlightthickness=2,
        highlightbackground=theme["border"],
        highlightcolor=theme["button_active"],
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"]
    )

    task_entry.insert(0, tasks[index][0])

    task_entry.pack(
        pady=(25, 15),
        ipady=7
    )

    time_label = tk.Label(
        edit_window,
        text=f"Current time: {tasks[index][1]}",
        font=("Arial", 14),
        bg=theme["bg"],
        fg=theme["secondary_text"]
    )

    time_label.pack(pady=5)

    new_time = [tasks[index][1]]

    # ---------- CHANGE TIME ----------

    def choose_edit_time():

        edit_time_window = tk.Toplevel(edit_window)
        theme = get_theme()

        edit_time_window.configure(bg=theme["bg"])
        edit_time_window.title("Choose Time")
        edit_time_window.geometry("400x300")
        edit_time_window.resizable(False, False)

        tk.Label(
            edit_time_window,
            text="Choose a time",
            font=("Arial", 24, "bold"),
            bg=theme["bg"],
            fg=theme["text"]
        ).pack(pady=(20, 15))

        time_frame = tk.Frame(
            edit_time_window,
            bg=theme["bg"]
        )

        time_frame.pack(pady=10)

        hour_box = tk.Spinbox(
            time_frame,
            from_=1,
            to=12,
            width=3,
            font=("Arial", 22),
            justify="center",
            state="readonly",
            relief="flat",
            bd=0,
            highlightthickness=1
        )

        hour_box.pack(
            side="left",
            padx=5,
            ipady=5
        )

        style_spinbox(hour_box)

        tk.Label(
            time_frame,
            text=":",
            font=("Arial", 22, "bold"),
            bg=theme["bg"],
            fg=theme["secondary_text"]
        ).pack(side="left")

        minute_box = tk.Spinbox(
            time_frame,
            from_=0,
            to=59,
            width=3,
            font=("Arial", 22),
            justify="center",
            format="%02.0f",
            state="readonly",
            relief="flat",
            bd=0,
            highlightthickness=1
        )

        minute_box.pack(
            side="left",
            padx=5,
            ipady=5
        )

        style_spinbox(minute_box)

        tk.Label(
            time_frame,
            text=":",
            font=("Arial", 22, "bold"),
            bg=theme["bg"],
            fg=theme["secondary_text"]
        ).pack(side="left")

        am_pm_box = tk.Spinbox(
            time_frame,
            values=("AM", "PM"),
            width=4,
            font=("Arial", 20),
            justify="center",
            state="readonly",
            relief="flat",
            bd=0,
            highlightthickness=1
        )

        am_pm_box.pack(
            side="left",
            padx=5,
            ipady=5
        )

        style_spinbox(am_pm_box)

        def save_edit_time():

            hour = hour_box.get()
            minute = minute_box.get()
            am_pm = am_pm_box.get()

            new_time[0] = f"{hour}:{minute} {am_pm}"

            time_label.config(
                text=f"Current time: {new_time[0]}"
            )

            edit_time_window.destroy()

        tk.Button(
            edit_time_window,
            text="SET TIME",
            font=("Arial", 13, "bold"),
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            activebackground=theme["button_active"],
            activeforeground=theme["button_fg"],
            relief="flat",
            bd=0,
            padx=18,
            pady=8,
            command=save_edit_time
        ).pack(pady=25)

    change_time_button = tk.Button(
        edit_window,
        text="CHANGE TIME",
        font=("Arial", 13, "bold"),
        width=15,
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"],
        relief="flat",
        bd=0,
        padx=10,
        pady=8,
        command=choose_edit_time
    )

    change_time_button.pack(pady=12)

    # ---------- SAVE ----------

    def save_edit():

        new_task = task_entry.get()

        if new_task == "":
            return

        new_task_time = new_time[0]

        delete_scheduled_notification(index)

        tasks[index] = (
            new_task,
            new_task_time
        )

        schedule_task_notification(
            index,
            new_task,
            new_task_time
        )

        save_tasks()
        show_tasks()

        edit_window.destroy()

    save_button = tk.Button(
        edit_window,
        text="SAVE",
        font=("Arial", 13, "bold"),
        width=15,
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"],
        relief="flat",
        bd=0,
        padx=10,
        pady=8,
        command=save_edit
    )

    save_button.pack(pady=15)

#notith
def check_tasks():
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")

    for i, (task, task_time) in enumerate(tasks):
        task_id = f"{i}-{task}-{task_time}"

        if task_time == current_time and task_id not in notified_tasks:
            notification.notify(
                title="Task Manager",
                message=f"its time to do «{task}»! 🔔",
                timeout=10
            )

            notified_tasks.add(task_id)

    window.after(1000, check_tasks)
#jshon
def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

def apply_theme():
    theme = themes[current_theme]
    
    # ---------- THEME MENU ----------

    theme_menu.config(
    bg=theme["bg"],
    highlightbackground=theme["border"]
)

    for theme_button_widget in (
    normal_button,
    dark_button,
    light_button,
    ocean_button,
    forest_button,
    sunset_button
):
        theme_button_widget.config(
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"]
    )

    # Window
    window.config(bg=theme["bg"])

    # Pages
    task_page.config(bg=theme["bg"])
    timer_page.config(bg=theme["bg"])

    # Frames
    bottom_bar.config(bg=theme["bg"])
    input_frame.config(bg=theme["bg"])
    tasks_frame.config(bg=theme["bg"])
    message_premium_frame.config(bg=theme["bg"])
    premium_frame.config(bg=theme["bg"])
    time_input_frame.config(bg=theme["bg"])
    timer_buttons_frame.config(bg=theme["bg"])

    # ---------- TASK PAGE ----------

    label.config(
        bg=theme["bg"],
        fg=theme["text"]
    )

    entry.config(
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        highlightbackground=theme["border"],
        highlightcolor=theme["button_active"]
    )

    time_button.config(
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"]
    )

    button.config(
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"]
    )

    message_Lable.config(
        bg=theme["bg"],
        fg=theme["secondary_text"]
    )

    button_2.config(
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"]
    )

    # ---------- TIMER ----------

    timer_title.config(
    bg=theme["bg"],
    fg=theme["text"]
)

    timer_label.config(
    bg=theme["bg"],
    fg=theme["text"]
)

    time_input_frame.config(
    bg=theme["bg"]
)

    timer_buttons_frame.config(
    bg=theme["bg"]
)

    timer_colon_1.config(
    bg=theme["bg"],
    fg=theme["secondary_text"]
)

    timer_colon_2.config(
    bg=theme["bg"],
    fg=theme["secondary_text"]
)

    style_spinbox(hour_box)
    style_spinbox(minute_box)
    style_spinbox(second_box)
    style_button(start_button)
    style_button(pause_button)
    style_button(reset_button)
    style_button(set_time_button)
    # ---------- BOTTOM BAR ----------

    for nav_button in (
        task_button,
        timer_button
    ):
        nav_button.config(
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            activebackground=theme["button_active"],
            activeforeground=theme["button_fg"]
        )

    # ---------- THEME BUTTON ----------

    theme_button.config(
        bg=theme["button_bg"],
        fg=theme["button_fg"],
        activebackground=theme["button_active"],
        activeforeground=theme["button_fg"]
    )

    # دوباره ساختن Taskها با تم جدید
    show_tasks()

def change_theme(theme_name):
    global current_theme

    current_theme = theme_name
    apply_theme()
    close_theme_menu()

def load_tasks():
    global tasks

    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        tasks = json.load(file)

    tasks = [tuple(task) for task in tasks]


# ---------------- ADD TASK ----------------

def add_task():
    global selected_time

    task_save = entry.get()

    if task_save == "":
        return

    if len(tasks) >= 4:
        message_Lable.config(
            text="You can only add 4 tasks.",
            font=("Arial", 20)
        )

        button_2.pack(pady=0)
        button_2.pack(pady=0) 

        # بعد از 4 ثانیه پیام پاک شود
        window.after(
            4000,
            lambda: message_Lable.config(text="")
        )

        # بعد از 4 ثانیه Premium مخفی شود
        window.after(
            4000,
            button_2.pack_forget
        )

        return

    if selected_time is None:
        time_for_task = "No time"
    else:
        time_for_task = selected_time
    tasks.append((task_save, time_for_task))

    save_tasks()

    new_index = len(tasks) - 1

    schedule_task_notification(
        new_index,
        task_save,
        time_for_task
    )

    show_tasks()
    
    
    # پاک کردن Entry
    entry.delete(0, tk.END)

    # ریست زمان برای تسک بعدی
    selected_time = None
    time_button.config(text="TIME")


# ---------------- TITLE ----------------

label = tk.Label(
    task_page,
    text="My Task Manager",
    font=("Arial", 36, "bold"),
    fg="#222222",
    bg="#f0f0f0"
)

label.pack(pady=(10, 5))


# ---------------- ENTRY + TIME BUTTON ----------------

input_frame = tk.Frame(task_page)
input_frame.pack(pady=10)

entry = tk.Entry(
    input_frame,
    width=24,
    font=("Arial", 22),
    relief="flat",
    bd=0,
    highlightthickness=2,
    highlightbackground="#d0d0d0",
    highlightcolor="#777777"
)

entry.pack(side="left", padx=5, ipady=8)

time_button = tk.Button(
    input_frame,
    text="ADD TIME",
    font=("Arial", 14, "bold"),
    width=12,
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=choose_time
)

time_button.pack(side="left", padx=5)


# ---------------- ADD BUTTON ----------------

button = tk.Button(
    task_page,
    text="ADD",
    command=add_task,
    font=("Arial", 14, "bold"),
    width=12,
    bg="#222222",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8
)

button.pack(pady=15)


# ---------------- TASKS ----------------

tasks_frame = tk.Frame(task_page)
tasks_frame.pack(pady=30)
load_tasks()
show_tasks()

# ---------------- MESSAGE ----------------

message_premium_frame = tk.Frame(task_page)
message_premium_frame.pack(pady=5)

message_Lable = tk.Label(
    message_premium_frame,
    text="",
    font=("Arial", 20)
)
message_Lable.pack()
# ---------------- PREMIUM ----------------

premium_frame = tk.Frame(task_page)
premium_frame.pack(pady=0)

button_2 = tk.Button(
    premium_frame,
    text="get premium",
    font=("Arial", 20),
    bg="#111111",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    command=open_site
)

button_2.pack_forget()


load_tasks()
show_tasks()
check_tasks()

apply_theme()

window.mainloop()