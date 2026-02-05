print("GUI FILE STARTED")
import tkinter as tk
from tkinter import messagebox
import psutil
import shutil
import os
import tempfile
import winshell

# ---------------- SYSTEM INFO ----------------
def show_system_usage():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = shutil.disk_usage("C:/")

    info = (
        f"CPU Usage: {cpu}%\n"
        f"RAM Usage: {ram}%\n"
        f"Disk Used: {disk.used // (1024**3)} GB\n"
        f"Disk Free: {disk.free // (1024**3)} GB"
    )

    messagebox.showinfo("System Usage", info)

# ---------------- CLEAN TEMP ----------------
def clean_temp():
    temp_dir = tempfile.gettempdir()
    deleted = 0

    for item in os.listdir(temp_dir):
        path = os.path.join(temp_dir, item)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            deleted += 1
        except:
            pass

    messagebox.showinfo("Temp Cleanup", f"Deleted {deleted} temp items.")

# ---------------- BROWSER CACHE (SAFE) ----------------
def clean_browser_cache():
    paths = [
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache"),
        os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache")
    ]

    deleted = 0

    for path in paths:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                os.makedirs(path)
                deleted += 1
            except:
                pass

    messagebox.showinfo("Browser Cache", "Browser cache cleaned (Chrome / Edge).")

# ---------------- RECYCLE BIN ----------------
def empty_recycle_bin():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False)
        messagebox.showinfo("Recycle Bin", "Recycle Bin emptied.")
    except:
        messagebox.showerror("Error", "Could not empty Recycle Bin.")

# ---------------- TOP RAM USERS ----------------
def show_top_ram_apps():
    processes = []

    for p in psutil.process_iter(['name', 'memory_info']):
        try:
            ram = p.info['memory_info'].rss / (1024 * 1024)
            processes.append((p.info['name'], ram))
        except:
            pass

    processes.sort(key=lambda x: x[1], reverse=True)
    top = processes[:5]

    text = "Top RAM Usage Apps:\n\n"
    for name, ram in top:
        text += f"{name}: {ram:.1f} MB\n"

    messagebox.showinfo("Top RAM Apps", text)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Safe PC Cleaner (Python)")
root.geometry("350x360")
root.resizable(False, False)

tk.Label(root, text="SAFE PC CLEANER", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Show System Usage", width=30, command=show_system_usage).pack(pady=5)
tk.Button(root, text="Clean TEMP Files", width=30, command=clean_temp).pack(pady=5)
tk.Button(root, text="Clean Browser Cache", width=30, command=clean_browser_cache).pack(pady=5)
tk.Button(root, text="Empty Recycle Bin", width=30, command=empty_recycle_bin).pack(pady=5)
tk.Button(root, text="Show Top RAM Apps", width=30, command=show_top_ram_apps).pack(pady=5)

tk.Label(root, text="No registry • No admin • Safe", fg="gray").pack(pady=10)

root.mainloop()