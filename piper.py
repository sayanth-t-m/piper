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

# Set a theme for better aesthetics
style = ttk.Style()
style.theme_use('clam')

# Create a frame for input elements
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Add a title label
title_label = ttk.Label(input_frame, text="YouTube Downloader", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Add URL label and entry
url_label = ttk.Label(input_frame, text="Enter YouTube URL:")
url_label.pack()
url_entry = ttk.Entry(input_frame, width=50)
url_entry.pack(pady=5)

# Add type selection label and radio buttons
type_label = ttk.Label(input_frame, text="Select type:")
type_label.pack()
type_var = tk.StringVar(value="video")
video_radio = ttk.Radiobutton(input_frame, text="Video (1080p)", variable=type_var, value="video")
audio_radio = ttk.Radiobutton(input_frame, text="Audio (High Quality)", variable=type_var, value="audio")
video_radio.pack()
audio_radio.pack()

# Add the download button
download_button = ttk.Button(root, text="Download", command=lambda: download())
download_button.pack(pady=10)

# Add a text widget for status messages
status_text = tk.Text(root, height=5, width=50)
status_text.pack(pady=5)

# Add a label for the save directory
download_dir = os.path.expanduser('~/Downloads')
save_label = ttk.Label(root, text=f"Files will be saved in: {download_dir}")
save_label.pack(pady=5)

# Create a queue for status updates
status_queue = queue.Queue()

# Progress hook function to update status
def progress_hook(d):
    if d['status'] == 'finished':
        status_queue.put("Download complete!\n")
    elif d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        status_queue.put(f"Downloading: {percent:.2f}%\n")

# Download thread function
def download_thread():
    url = url_entry.get()
    if not url:
        status_queue.put("Please enter a URL.\n")
        status_queue.put("enable_button")
        return
    type_selected = type_var.get()
    if type_selected == "video":
        ydl_opts = {
            'format': 'bestvideo[height=1080]+bestaudio/bestvideo+bestaudio',
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(download_dir, '%(title)s-%(id)s-video.%(ext)s'),  # <-- add -video
        }
    else:
        ydl_opts = {
            'format': 'bestaudio',
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(download_dir, '%(title)s-%(id)s-audio.%(ext)s'),  # <-- add -audio
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
        status_queue.put(f"An error occurred: {e}\n")
    finally:
        status_queue.put("enable_button")

# Function to start the download
def download():
    download_button.config(state=tk.DISABLED)
    status_text.delete(1.0, tk.END)
    status_text.insert(tk.END, "Starting download...\n")
    thread = threading.Thread(target=download_thread)
    thread.start()

# Function to check the queue and update the GUI
def check_queue():
    while not status_queue.empty():
        message = status_queue.get()
        if message == "enable_button":
            download_button.config(state=tk.NORMAL)
        else:
            status_text.insert(tk.END, message)
            status_text.see(tk.END)
    root.after(100, check_queue)

# Start the queue checking
root.after(100, check_queue)

# Run the main loop
root.mainloop()