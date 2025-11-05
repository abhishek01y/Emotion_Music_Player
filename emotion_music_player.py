import cv2
from fer import FER
import pygame
import os
import random
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame for music playback
pygame.mixer.init()

# Global variables for music
songs = []
current_folder = ""

def play_music(folder):
    global songs
    global current_folder
    current_folder = folder
    songs = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    if not songs:
        print(f"No songs in {folder}")
        return
    song = random.choice(songs)
    pygame.mixer.music.load(os.path.join(folder, song))
    pygame.mixer.music.play()
    print(f"Now playing: {song}")

def stop_music():
    pygame.mixer.music.stop()

def next_song():
    if songs:
        song = random.choice(songs)
        pygame.mixer.music.load(os.path.join(current_folder, song))
        pygame.mixer.music.play()
        print(f"Now playing: {song}")

def auto_next_song():
    if not pygame.mixer.music.get_busy() and songs:
        next_song()
    root.after(1000, auto_next_song)  # check every second

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
        "angry": "vibe",   # replace 'angry' with 'vibe'
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
    play_music(folder)
    root.after(1000, auto_next_song)  # start automatic song change
    messagebox.showinfo("Emotion Detected", f"Detected Emotion: {emotion}\nPlaying matching music!")

def stop_app():
    stop_music()
    root.destroy()

# GUI
root = tk.Tk()
root.title("Emotion-Based Music Player")
root.geometry("350x250")
root.configure(bg="#1e1e2f")

tk.Label(root, text="Emotion-Based Music Player", font=("Helvetica", 16, "bold"), bg="#1e1e2f", fg="#f5f5f5").pack(pady=20)

# Start button
start_btn = tk.Button(root, text="Start", command=start_app, width=18, bg="#4caf50", fg="white", activebackground="#45a049", activeforeground="white")
start_btn.pack(pady=5)

# Stop button
stop_btn = tk.Button(root, text="Stop & Exit", command=stop_app, width=18, bg="#f44336", fg="white", activebackground="#da190b", activeforeground="white")
stop_btn.pack(pady=5)

# Next Song button
next_btn = tk.Button(root, text="Next Song", command=next_song, width=18, bg="#2196f3", fg="white", activebackground="#0b7dda", activeforeground="white")
next_btn.pack(pady=5)

root.mainloop()
