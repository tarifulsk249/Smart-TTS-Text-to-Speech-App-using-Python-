import customtkinter as ctk
from tkinter import filedialog
from gtts import gTTS
from langdetect import detect
import os

# Auto language detection
def auto_detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "en"

# Speak function
def speak_text(language=None):
    text = text_box.get("1.0", "end-1c").strip()
    if text == "":
        status_label.configure(text=" Please enter some text!", text_color="orange")
        return

    # Auto language detection
    if language is None:
        language = auto_detect_language(text)
        status_label.configure(text=f" Auto-detected: {language.upper()}", text_color="blue")

    # Speed control
    speed_choice = speed_option.get()
    slow_mode = True if speed_choice == "Slow" else False

    try:
        tts = gTTS(text=text, lang=language, slow=slow_mode)
        tts.save("output.mp3")
        os.system("start output.mp3")  # Windows
        status_label.configure(text=f" Played in {language.upper()} ({speed_choice})", text_color="green")
    except Exception as e:
        status_label.configure(text=f" Error: {e}", text_color="red")

# Save function
def save_audio(language=None):
    text = text_box.get("1.0", "end-1c").strip()
    if text == "":
        status_label.configure(text=" Please enter some text!", text_color="orange")
        return

    if language is None:
        language = auto_detect_language(text)

    speed_choice = speed_option.get()
    slow_mode = True if speed_choice == "Slow" else False

    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
    if not file_path:
        return

    try:
        tts = gTTS(text=text, lang=language, slow=slow_mode)
        tts.save(file_path)
        status_label.configure(text=f" Saved successfully at: {file_path}", text_color="green")
    except Exception as e:
        status_label.configure(text=f" Error: {e}", text_color="red")

# ------------------ GUI Design ------------------
ctk.set_appearance_mode("light")  # "dark" or "light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎙️ Smart TTS - Text to Speech")
app.geometry("520x580")

# Title
title_label = ctk.CTkLabel(app, text=" Text to Speech Converter", font=("Arial Rounded MT Bold", 22))
title_label.pack(pady=15)

# Text box
text_box = ctk.CTkTextbox(app, width=420, height=130, font=("Arial", 13))
text_box.pack(pady=10)

# Speed selection
ctk.CTkLabel(app, text=" Voice Speed", font=("Arial", 14)).pack(pady=5)
speed_option = ctk.CTkOptionMenu(app, values=["Slow", "Normal", "Fast"])
speed_option.set("Normal")
speed_option.pack(pady=5)

# Language buttons
ctk.CTkLabel(app, text=" Choose Language (or Auto):", font=("Arial", 14)).pack(pady=5)
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

languages = [
    ("English", "en"),
    ("Hindi", "hi"),
    ("Bengali", "bn"),
    ("Spanish", "es"),
    ("French", "fr"),
]

for i, (name, code) in enumerate(languages):
    btn = ctk.CTkButton(frame, text=name, width=120, command=lambda c=code: speak_text(c))
    btn.grid(row=i//2, column=i%2, padx=10, pady=6)

# Auto detect and Save buttons
ctk.CTkButton(app, text=" Auto Detect & Speak", width=200, fg_color="#0078D7", command=lambda: speak_text(None)).pack(pady=10)
ctk.CTkButton(app, text=" Save as MP3", width=200, fg_color="#4CAF50", command=lambda: save_audio(None)).pack(pady=5)

# Status label
status_label = ctk.CTkLabel(app, text="", font=("Arial", 12))
status_label.pack(pady=15)

# Run app

app.mainloop()
