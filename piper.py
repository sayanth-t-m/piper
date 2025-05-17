import tkinter as tk
from tkinter import ttk
import yt_dlp as youtube_dl
import threading
import queue
import os

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x300")

# Set a futuristic dark theme with neon highlights
root.configure(bg="#181A20")

style = ttk.Style()
style.theme_use('clam')

# Futuristic colors
bg_color = "#181A20"
frame_color = "#23263A"
accent_color = "#00FFF7"  # Neon cyan
accent2_color = "#A259FF" # Neon purple
text_color = "#E0E0E0"

style.configure("TFrame", background=frame_color)
style.configure("TLabel", background=frame_color, foreground=text_color, font=("Segoe UI", 10))
style.configure("Title.TLabel", background=bg_color, foreground=accent_color, font=("Orbitron", 18, "bold"))
style.configure("TButton", background=accent_color, foreground=bg_color, font=("Segoe UI", 10, "bold"), borderwidth=0, focusthickness=3, focuscolor=accent2_color)
style.map("TButton",
    background=[('active', accent2_color), ('pressed', accent_color)],
    foreground=[('active', text_color), ('pressed', bg_color)])
style.configure("TRadiobutton", background=frame_color, foreground=accent2_color, font=("Segoe UI", 10, "bold"))
style.map("TRadiobutton",
    background=[('selected', accent_color)],
    foreground=[('selected', bg_color)])
style.configure("TProgressbar", background=accent_color, troughcolor=frame_color, bordercolor=accent2_color, lightcolor=accent_color, darkcolor=accent2_color, thickness=12)

# Create a frame for input elements
input_frame = ttk.Frame(root, style="TFrame")
input_frame.pack(pady=16)

# Add a title label
try:
    import tkinter.font as tkfont
    if "Orbitron" not in tkfont.families():
        # Orbitron is not a default font, fallback
        title_font = ("Segoe UI", 18, "bold")
    else:
        title_font = ("Orbitron", 18, "bold")
except:
    title_font = ("Segoe UI", 18, "bold")

# Title label with accent color
title_label = ttk.Label(input_frame, text="Piper", style="Title.TLabel")
title_label.pack(pady=10)

# Add URL label and entry
url_label = ttk.Label(input_frame, text="Enter YouTube URL:", style="TLabel")
url_label.pack()
# Use tk.Entry for color customization
url_entry = tk.Entry(input_frame, width=50, font=("Consolas", 10), bg=frame_color, fg=accent_color, insertbackground=accent_color, relief=tk.FLAT, highlightthickness=1, highlightbackground=accent2_color)
url_entry.pack(pady=5)

# Add type selection label and radio buttons
type_label = ttk.Label(input_frame, text="Select type:", style="TLabel")
type_label.pack()
type_var = tk.StringVar(value="video")
video_radio = ttk.Radiobutton(input_frame, text="Video (1080p)", variable=type_var, value="video", style="TRadiobutton")
audio_radio = ttk.Radiobutton(input_frame, text="Audio (High Quality)", variable=type_var, value="audio", style="TRadiobutton")
video_radio.pack()
audio_radio.pack()

# Add the download button
download_button = ttk.Button(root, text="Download", command=lambda: download(), style="TButton")
download_button.pack(pady=14)

progress_frame = ttk.Frame(root, style="TFrame")
progress_frame.pack(pady=(0, 14))

progress = ttk.Progressbar(progress_frame, orient='horizontal',
                           mode='determinate', length=300, style="TProgressbar")
progress.pack(pady=(0, 7))
progress['maximum'] = 100
progress['value'] = 0

# Add a text widget for status messages
status_text = tk.Text(progress_frame, height=5, width=50, bg=frame_color, fg=accent_color, insertbackground=accent2_color, font=("Consolas", 10), borderwidth=0, highlightthickness=1, highlightbackground=accent2_color, state=tk.DISABLED)
status_text.pack(pady=5)

# Add a label for the save directory
download_dir = os.path.expanduser('~/Downloads')
save_label = ttk.Label(root, text=f"Files will be saved in: {download_dir}", style="TLabel")
save_label.pack(pady=5)

# Create a queue for status updates
status_queue = queue.Queue()

# Progress hook function to update status
def progress_hook(d):
    if d.get('status') == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
        pct = downloaded / total * 100
        status_queue.put(('text', f"Downloading… {pct:.1f}%\n"))
        status_queue.put(('bar', pct))
    elif d.get('status') == 'finished':
        status_queue.put(('text', "Download finished; post-processing…\n"))
        status_queue.put(('bar', 100))

# Download thread function
def download_thread():
    url = url_entry.get()
    if not url:
        status_queue.put(('text', "Please enter a URL.\n"))
        status_queue.put(('enable_button', None))
        return
    type_selected = type_var.get()
    if type_selected == "video":
        ydl_opts = {
            'format': 'bestvideo[height=1080]+bestaudio/bestvideo+bestaudio',
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(download_dir, '%(title)s-%(id)s-video.%(ext)s'),
        }
    else:
        ydl_opts = {
            'format': 'bestaudio',
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(download_dir, '%(title)s-%(id)s-audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        status_queue.put(('text', f"An error occurred: {e}\n"))
    finally:
        status_queue.put(('enable_button', None))

# Function to start the download
def download():
    download_button.config(state=tk.DISABLED)
    progress['value'] = 0
    status_text.config(state=tk.NORMAL)
    status_text.delete(1.0, tk.END)
    status_text.insert(tk.END, "Starting download...\n")
    status_text.config(state=tk.DISABLED)
    thread = threading.Thread(target=download_thread)
    thread.start()

# Function to check the queue and update the GUI
def check_queue():
    while not status_queue.empty():
        msg = status_queue.get()
        if isinstance(msg, tuple):
            msg_type, data = msg
            if msg_type == 'text':
                status_text.config(state=tk.NORMAL)
                status_text.insert(tk.END, data)
                status_text.see(tk.END)
                status_text.config(state=tk.DISABLED)
            elif msg_type == 'bar':
                progress['value'] = data
            elif msg_type == 'enable_button':
                download_button.config(state=tk.NORMAL)
                progress['value'] = 0
        else:
            # For backward compatibility if a string is put
            status_text.config(state=tk.NORMAL)
            status_text.insert(tk.END, str(msg))
            status_text.see(tk.END)
            status_text.config(state=tk.DISABLED)
    root.after(100, check_queue)

# Start the queue checking
root.after(100, check_queue)

# Run the main loop
root.mainloop()