#!/usr/bin/python

import tkinter as tk
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import chime

# Configurations
time_sync_precision = 0.999
time_zone=ZoneInfo("America/New_York")
font_size=32
font_color="lime"
font_color_alt="red"
background_color="black"
chime.theme('chime')


def is_last_five_seconds(seconds):
    return 55 <= seconds <= 59


def is_five_seconds_before_five_minute(minutes, seconds):
    return (55 < seconds <= 59) and (minutes + 1) % 5 == 0


def should_change_font_color(seconds):
    return is_last_five_seconds(seconds)


def should_beep(minutes, seconds):
    return is_five_seconds_before_five_minute(minutes, seconds)


def update_time():
    now = datetime.now(time_zone)
    current_time = now.strftime("%H:%M:%S")

    current_seconds = int(now.strftime("%S"))
    current_minutes = int(now.strftime("%M"))

    if should_change_font_color(current_seconds):
        clock_label.config(fg=font_color_alt)

        if should_beep(current_minutes, current_seconds):
            chime.info()
    
    else:
        clock_label.config(fg=font_color)

    clock_label.config(text=current_time)
    clock_label.after(1000, update_time) # Update every 1 second


def on_show_context_menu(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Settings", command=on_show_settings_window)
    menu.add_command(label="Exit", command=root.destroy)

    def close_context_menu(event):
        if menu.winfo_exists():
            menu.unpost()

    root.bind("<Button-1>", close_context_menu)
    menu.post(event.x_root, event.y_root)


def on_show_settings_window():
    print("Creating and showing settings window")


def on_drag_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

def get_fractional_seconds():
    return float(datetime.now(time_zone).strftime(".%f"))

def start():
    print("syncing clock...")
    fractional_seconds = get_fractional_seconds()

    while fractional_seconds <= time_sync_precision:
        fractional_seconds = get_fractional_seconds()

    update_time()
    root.mainloop()


# Set up the main application window
root = tk.Tk()
root.title("Stock Clock")
root.bind("<Button-3>", on_show_context_menu)
root.overrideredirect(True)


# Create a label to display the time
clock_label = tk.Label(root, font=("Helvetica", font_size), fg=font_color, bg=background_color)
clock_label.pack(pady=4, padx=4, expand=True)


# Run the application
root.bind("<B1-Motion>", on_drag_window)
root.eval(f"tk::PlaceWindow {str(root)} center")


start()
