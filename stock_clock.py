#!/usr/bin/python

import tkinter as tk
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import chime
from tkinter import colorchooser
from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.ini")

class StockClockConfig:
    def __init__(self, time_sync_precision, time_zone, font_size, font_color, font_color_alt, background_color, notification_theme, notification_alert_type):
        self.time_sync_precision = time_sync_precision
        self.time_zone = time_zone
        self.font_size = font_size
        self.font_color = font_color
        self.font_color_alt = font_color_alt
        self.background_color = background_color
        self.notification_theme = notification_theme
        self.notification_alert_type = notification_alert_type


# Configurations
config = StockClockConfig(
    time_sync_precision = float(parser.get("default", "time_sync_precision")),
    time_zone = ZoneInfo(parser.get("default", "time_zone")),
    font_size = int(parser.get("default", "font_size")),
    font_color = parser.get("default", "font_color"),
    font_color_alt = parser.get("default", "font_color_alt"),
    background_color = parser.get("default", "background_color"),
    notification_theme = parser.get("default", "notification_theme"),
    notification_alert_type = parser.get("default", "notification_alert_type")
)

chime.theme(config.notification_theme)


def is_last_five_seconds(seconds):
    return 55 <= seconds <= 59


def is_five_seconds_before_five_minute(minutes, seconds):
    return (55 < seconds <= 59) and (minutes + 1) % 5 == 0


def should_change_font_color(seconds):
    return is_last_five_seconds(seconds)


def should_beep(minutes, seconds):
    return is_five_seconds_before_five_minute(minutes, seconds)

def beep():
    match config.notification_alert_type:
        case "success":
            chime.success()
        case "info":
            chime.info()
        case "warning":
            chime.warning()
        case "error":
            chime.error()


def update_time():
    now = datetime.now(config.time_zone)
    current_time = now.strftime("%H:%M:%S")

    current_seconds = int(now.strftime("%S"))
    current_minutes = int(now.strftime("%M"))

    if should_change_font_color(current_seconds):
        clock_label.config(fg=config.font_color_alt)

        if should_beep(current_minutes, current_seconds):
            beep()
    
    else:
        clock_label.config(fg=config.font_color)

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
    return float(datetime.now(config.time_zone).strftime(".%f"))

def restore_configurations(config):
    saved_time_sync_precision = float(parser.get("saved", "time_sync_precision"))
    saved_time_zone = ZoneInfo(parser.get("saved", "time_zone"))
    saved_font_size = int(parser.get("saved", "font_size"))
    saved_font_color = parser.get("saved", "font_color")
    saved_font_color_alt = parser.get("saved", "font_color_alt")
    saved_background_color = parser.get("saved", "background_color")
    saved_notification_theme = parser.get("saved", "notification_theme")
    
    config.font_color = saved_font_color or config["font_color"]


def start():
    print("syncing clock...")
    fractional_seconds = get_fractional_seconds()

    while fractional_seconds <= config.time_sync_precision:
        fractional_seconds = get_fractional_seconds()

    update_time()
    root.mainloop()


# Set up the main application window
root = tk.Tk()
root.title("Stock Clock")
root.bind("<Button-3>", on_show_context_menu)
root.overrideredirect(True)


# Create a label to display the time
clock_label = tk.Label(root, font=("Helvetica", config.font_size), fg=config.font_color, bg=config.background_color)
clock_label.pack(pady=4, padx=4, expand=True)


# Run the application
root.bind("<B1-Motion>", on_drag_window)
root.eval(f"tk::PlaceWindow {str(root)} center")

restore_configurations(config)
start()
