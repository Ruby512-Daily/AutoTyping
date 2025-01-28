import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import keyboard

# Global variables
is_typing = False

def start_auto_typing():
    global is_typing
    is_typing = True
    text = input_text.get("1.0", tk.END).strip()
    interval = float(interval_entry.get())
    prep_time = float(preparation_entry.get())

    if not text:
        output_label.config(text="Please enter some text to auto-type.")
        return

    output_label.config(text=f"Preparing to start in {prep_time} seconds...")

    def type_out():
        global is_typing
        # Wait for the preparation time
        time.sleep(prep_time)

        for char in text:
            if not is_typing:  # Stop if the typing is canceled
                output_label.config(text="Auto-typing stopped!")
                return
            pyautogui.typewrite(char)  # Sends keystrokes to the focused window
            time.sleep(interval)
        output_label.config(text="Auto-typing completed!")
        is_typing = False

    # Run auto-typing in a separate thread to prevent UI freezing
    threading.Thread(target=type_out, daemon=True).start()

def stop_auto_typing():
    global is_typing
    is_typing = False
    output_label.config(text="Auto-typing stopped by user.")

# Set up hotkeys
def setup_hotkeys():
    def listen_for_hotkeys():
        keyboard.add_hotkey('ctrl+shift+3', start_auto_typing)
        keyboard.add_hotkey('ctrl+shift+4', stop_auto_typing)
        keyboard.wait()  # Keeps the hotkey listener running

    threading.Thread(target=listen_for_hotkeys, daemon=True).start()

# Create the main application window
root = tk.Tk()
root.title("Auto-Typing Program with Hotkeys and Preparation Time")
root.attributes('-topmost', False)  # Ensure the program is not always on top

# Input text label and text area
input_label = ttk.Label(root, text="Input Text:")
input_label.pack(pady=5)

input_text = tk.Text(root, wrap=tk.WORD, height=10, width=50)
input_text.pack(pady=5)

# Time interval input
interval_frame = ttk.Frame(root)
interval_frame.pack(pady=5)

interval_label = ttk.Label(interval_frame, text="Time Interval (seconds):")
interval_label.pack(side=tk.LEFT, padx=5)

interval_entry = ttk.Entry(interval_frame)
interval_entry.insert(0, "0.1")  # Default interval of 0.1 seconds
interval_entry.pack(side=tk.LEFT, padx=5)

# Preparation time input
preparation_frame = ttk.Frame(root)
preparation_frame.pack(pady=5)

preparation_label = ttk.Label(preparation_frame, text="Preparation Time (seconds):")
preparation_label.pack(side=tk.LEFT, padx=5)

preparation_entry = ttk.Entry(preparation_frame)
preparation_entry.insert(0, "3")  # Default preparation time
preparation_entry.pack(side=tk.LEFT, padx=5)

# Start and Stop buttons
start_button = ttk.Button(root, text="Start Auto-Typing", command=start_auto_typing)
start_button.pack(pady=5)

stop_button = ttk.Button(root, text="Stop Auto-Typing", command=stop_auto_typing)
stop_button.pack(pady=5)

# Output text label
output_label = ttk.Label(root, text="")
output_label.pack(pady=10)

# Set up hotkeys on application start
setup_hotkeys()

# Run the Tkinter event loop
root.mainloop()