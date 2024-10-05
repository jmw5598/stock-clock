#!/usr/bin/python

import tkinter as tk
import time
import chime

# Configurations
font_size=32
font_color="lime"
font_color_alt="red"
background_color="black"

chime.theme('chime')


def is_last_five_seconds(seconds):
    return 55 <= seconds <= 59


def is_five_seconds_before_five_minute(minutes, seconds):
    return is_last_five_seconds(seconds) and (minutes + 1) % 5 == 0


def should_change_font_color(seconds):
    return is_last_five_seconds(seconds)


def should_beep(minutes, seconds):
    return is_five_seconds_before_five_minute(minutes, seconds)


def update_time():
    current_time = time.strftime("%H:%M:%S")

    current_seconds = int(time.strftime("%S"))
    current_minutes = int(time.strftime("%M"))

    if should_change_font_color(current_seconds):
        clock_label.config(fg=font_color_alt)

        if should_beep(current_minutes, current_seconds):
            chime.info()
    
    else:
        clock_label.config(fg=font_color)

    clock_label.config(text=current_time)
    clock_label.after(1000, update_time) # Update every 1 second

# Set up the main application window
root = tk.Tk()
root.title("Stock Clock")

# Create a label to display the time
clock_label = tk.Label(root, font=("Helvetica", font_size), fg=font_color, bg=background_color)
clock_label.pack(pady=0)

# Start the time update loop
update_time()

# Run the application
root.mainloop()
