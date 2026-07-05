import tkinter as tk
import serial
import serial.tools.list_ports
import threading
import queue
import time

q = queue.Queue()

def get_macropad_port():
    for port in serial.tools.list_ports.comports():
        if port.vid in [0x2E8A, 0x239A] or "CircuitPython" in port.description:
            return port.device
    return None

def serial_listener():
    while True:
        com_port = get_macropad_port()
        
        if not com_port:
            time.sleep(2)
            continue
            
        try:
            with serial.Serial(com_port, 115200, timeout=1) as ser:
                while True:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    if "active_layers=" in line:
                        # Passing a tuple: (Title, Keymap)
                        if "[0]" in line or "[4, 0]" in line or "[0, 4]" in line:
                            q.put(("Layer 0: System Utility", 
                                   "[ Snip ]  |  [ Copy ]  |  [ Paste ]  |  [ TaskMgr ]"))
                            
                        elif "[1]" in line or "[4, 1]" in line or "[1, 4]" in line:
                            q.put(("Layer 1: Media Controls", 
                                   "[ Play/Pause ]  |  [ Vol - ]  |  [ Vol + ]  |  [ Mute ]"))
                            
                        elif "[2]" in line or "[4, 2]" in line or "[2, 4]" in line:
                            q.put(("Layer 2: Browser Ninja", 
                                   "[ Reopen Tab ]  |  [ Tab < ]  |  [ Tab > ]  |  [ Close Tab ]"))
                            
                        elif "[3]" in line or "[4, 3]" in line or "[3, 4]" in line:
                            q.put(("Layer 3: Global Hotkeys", 
                                   "[ F13 ]  |  [ F14 ]  |  [ F15 ]  |  [ F16 ]"))
                            
        except (serial.SerialException, OSError):
            time.sleep(2)

listener = threading.Thread(target=serial_listener, daemon=True)
listener.start()

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.90)    # Slightly less transparent so text is highly readable
root.configure(bg='#1a1a1a')

window_width = 600
window_height = 90
x = (root.winfo_screenwidth() // 2) - (window_width // 2)
y = root.winfo_screenheight() - 180
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

title_label = tk.Label(root, text="", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#1a1a1a")
title_label.pack(pady=(12, 0))

keymap_label = tk.Label(root, text="", font=("Consolas", 11), fg="#b3b3b3", bg="#1a1a1a")
keymap_label.pack(pady=(4, 12))

hide_job = None

def hide_window():
    root.withdraw()

def check_queue():
    global hide_job
    try:
        title_text, keymap_text = q.get_nowait()
        title_label.config(text=title_text)
        keymap_label.config(text=keymap_text)
        
        root.deiconify() 
        
        if hide_job is not None:
            root.after_cancel(hide_job)
            
        hide_job = root.after(2000, hide_window)
    except queue.Empty:
        pass
    
    root.after(50, check_queue)

root.withdraw()
root.after(50, check_queue)
root.mainloop()