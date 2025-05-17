# YouTube Downloader GUI

A simple desktop application to download YouTube videos or audio in high quality using a user-friendly graphical interface built with Tkinter and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

---

## Features

- **Download YouTube Videos**: Save videos in up to 1080p quality.
- **Download Audio Only**: Extract and save high-quality audio as MP3.
- **Progress Updates**: See real-time download progress and status messages.
- **Easy to Use**: Clean, intuitive interface with no command-line required.
- **Automatic Save Location**: Files are saved to your system's `Downloads` folder.

---

## Requirements

- **Python 3.7+**
- **yt-dlp**  
- **ffmpeg** (for audio extraction)
- **tkinter** (usually included with Python)

---

## Installation

1. **Clone or Download this Repository**

2. **Install Dependencies**

   Open a terminal and run:
   ```sh
   pip install yt-dlp
   ```

   For audio downloads, make sure [ffmpeg](https://ffmpeg.org/download.html) is installed and available in your system PATH.

   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add the `bin` folder to your PATH.
   - **Linux/macOS**:  
     ```sh
     sudo apt install ffmpeg
     # or
     brew install ffmpeg
     ```

---

## Usage

1. **Run the Application**

   ```sh
   python piper.py
   ```

2. **Using the GUI**

   - Enter the full YouTube video URL in the input box.
   - Select either **Video (1080p)** or **Audio (High Quality)**.
   - Click **Download**.
   - Progress and status messages will appear in the status box.
   - Downloaded files will be saved in your `Downloads` folder.

---

## File Naming

- **Video**:  
  `Title-VideoID-video.<ext>`
- **Audio**:  
  `Title-VideoID-audio.mp3`

---

## Functions Overview

- **progress_hook**: Updates the status box with download progress and completion messages.
- **download_thread**: Handles the download process in a background thread to keep the UI responsive.
- **download**: Starts the download thread and updates the UI.
- **check_queue**: Periodically checks for status updates and refreshes the UI.

See [piper.py](piper.py) for full implementation details.

---

## Troubleshooting

- **yt-dlp not found**:  
  Make sure you installed it with `pip install yt-dlp`.
- **ffmpeg not found**:  
  Ensure ffmpeg is installed and added to your system PATH.
- **Permission errors**:  
  Run the application with appropriate permissions or change the download directory in the code.

---

## License

This project is for educational and personal use.

---