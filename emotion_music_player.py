import sys, importlib.resources
class _PkgCompat:
    @staticmethod
    def resource_filename(package, resource):
        return str(importlib.resources.files(package).joinpath(resource))
sys.modules["pkg_resources"] = _PkgCompat()

import cv2
from fer import FER
import pygame
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk

MUSIC_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")

pygame.mixer.init()

songs = []
current_folder = ""
paused = False

def play_music(folder):
    global songs, current_folder
    current_folder = folder
    songs = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    if not songs:
        now_playing_label.config(text="No songs in this folder!")
        return
    song = random.choice(songs)
    pygame.mixer.music.load(os.path.join(folder, song))
    pygame.mixer.music.play()
    now_playing_label.config(text=f"Now Playing: {song}")
    status_label.config(text="Status: Playing", fg="#4caf50")

def stop_music():
    pygame.mixer.music.stop()
    now_playing_label.config(text="Stopped")
    status_label.config(text="Status: Stopped", fg="#f44336")

def toggle_pause():
    global paused
    if pygame.mixer.music.get_busy():
        if paused:
            pygame.mixer.music.unpause()
            paused = False
            pause_btn.config(text="Pause")
            status_label.config(text="Status: Playing", fg="#4caf50")
        else:
            pygame.mixer.music.pause()
            paused = True
            pause_btn.config(text="Resume")
            status_label.config(text="Status: Paused", fg="#ff9800")

def next_song():
    if songs:
        song = random.choice(songs)
        pygame.mixer.music.load(os.path.join(current_folder, song))
        pygame.mixer.music.play()
        now_playing_label.config(text=f"Now Playing: {song}")
        status_label.config(text="Status: Playing", fg="#4caf50")

def set_volume(val):
    pygame.mixer.music.set_volume(float(val) / 100)

def auto_next_song():
    if not pygame.mixer.music.get_busy() and songs and not paused:
        next_song()
    root.after(1000, auto_next_song)

def detect_emotion():
    detector = FER()
    cam = cv2.VideoCapture(0)
    emotion_result = None

    messagebox.showinfo("Instructions", "Press 'q' to capture your emotion from webcam")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow('Emotion Capture - Press q', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            emotions = detector.detect_emotions(frame)
            if emotions:
                emotion_result = max(emotions[0]["emotions"], key=emotions[0]["emotions"].get)
            break

    cam.release()
    cv2.destroyAllWindows()
    return emotion_result

def get_music_folder(emotion):
    mapping = {
        "happy": "happy",
        "sad": "sad",
        "angry": "angry",
        "neutral": "neutral",
        "surprise": "happy",
        "fear": "neutral",
        "disgust": "neutral"
    }
    return os.path.join(MUSIC_BASE_PATH, mapping.get(emotion, "neutral"))

def start_app():
    emotion = detect_emotion()
    if not emotion:
        messagebox.showerror("Error", "No face detected! Try again.")
        return
    folder = get_music_folder(emotion)
    emotion_label.config(text=f"Detected Emotion: {emotion}")
    play_music(folder)
    root.after(1000, auto_next_song)
    messagebox.showinfo("Emotion Detected", f"Detected Emotion: {emotion}\nPlaying matching music!")

def stop_app():
    stop_music()
    root.destroy()

root = tk.Tk()
root.title("Emotion-Based Music Player")
root.geometry("400x400")
root.configure(bg="#1e1e2f")

tk.Label(root, text="Emotion-Based Music Player", font=("Helvetica", 16, "bold"), bg="#1e1e2f", fg="#f5f5f5").pack(pady=15)

emotion_label = tk.Label(root, text="Detected Emotion: None", font=("Helvetica", 10), bg="#1e1e2f", fg="#ffd700")
emotion_label.pack()

now_playing_label = tk.Label(root, text="No song playing", font=("Helvetica", 9, "italic"), bg="#1e1e2f", fg="#cccccc")
now_playing_label.pack(pady=5)

status_label = tk.Label(root, text="Status: Idle", font=("Helvetica", 9), bg="#1e1e2f", fg="#888888")
status_label.pack()

start_btn = tk.Button(root, text="Start", command=start_app, width=18, bg="#4caf50", fg="white", activebackground="#45a049", activeforeground="white")
start_btn.pack(pady=5)

pause_btn = tk.Button(root, text="Pause", command=toggle_pause, width=18, bg="#ff9800", fg="white", activebackground="#e68900", activeforeground="white")
pause_btn.pack(pady=2)

next_btn = tk.Button(root, text="Next Song", command=next_song, width=18, bg="#2196f3", fg="white", activebackground="#0b7dda", activeforeground="white")
next_btn.pack(pady=2)

vol_frame = tk.Frame(root, bg="#1e1e2f")
vol_frame.pack(pady=10)
tk.Label(vol_frame, text="Volume", bg="#1e1e2f", fg="#cccccc", font=("Helvetica", 9)).pack(side=tk.LEFT, padx=5)
vol_slider = ttk.Scale(vol_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume)
vol_slider.set(50)
vol_slider.pack(side=tk.LEFT)

pygame.mixer.music.set_volume(0.5)

stop_btn = tk.Button(root, text="Stop & Exit", command=stop_app, width=18, bg="#f44336", fg="white", activebackground="#da190b", activeforeground="white")
stop_btn.pack(pady=5)

root.mainloop()
