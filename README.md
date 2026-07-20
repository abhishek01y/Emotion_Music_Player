# Emotion Music Player 🎵

Detect your mood from your face — play matching music instantly. Built with FER + Flask.

A web application that uses facial expression recognition to detect your emotion (happy, sad, angry, neutral) and plays music from the matching playlist — either from local MP3 files or via YouTube search.

## Features

**Emotion Detection**
Real-time face detection via webcam or photo upload — identifies 7 emotions using deep learning (FER model)

**Smart Music Selection**
Maps detected emotion to a curated music folder or YouTube search query

| Emotion  | Music Folder | Vibe       |
|----------|-------------|------------|
| 😊 Happy  | `happy/`    | Upbeat, energetic |
| 😢 Sad    | `sad/`      | Melancholy, slow |
| 😠 Angry  | `angry/`    | High-energy, intense |
| 😐 Neutral| `neutral/`  | Chill, relaxing |

**Spotify-Style Player**
- Play / Pause / Next / Previous controls
- Progress bar with seek
- Auto-play next song when current ends
- Volume control
- Gradient theme matching your mood

**Two Apps in One**

| App | File | Description |
|-----|------|-------------|
| 🌐 Web App | `app.py` | Flask web app — upload photo or use webcam → plays in browser |
| 🖥️ Desktop App | `emotion_music_player.py` | Tkinter GUI — uses webcam → plays via pygame |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 + Flask 3 |
| Emotion Detection | FER (Facial Expression Recognition) + OpenCV |
| Desktop GUI | Tkinter + Pygame |
| Music Playback | HTML5 Audio (web) / Pygame (desktop) |
| YouTube Search | yt-dlp (optional fallback) |
| Frontend | HTML/CSS + Jinja2 Templates |

## Project Structure

```
EmotionMusicPlayer/
│
├── app.py                      # Flask web server
├── emotion_music_player.py     # Desktop Tkinter app
├── emotion_detector.py         # Standalone emotion detector
├── requirements.txt
├── README.md
│
├── music/
│   ├── happy/      (5 songs)
│   ├── sad/        (4 songs)
│   ├── angry/      (4 songs)
│   └── neutral/    (4 songs)
│
├── templates/
│   ├── index.html              # Webcam + upload UI
│   └── result.html             # Spotify-style player
│
└── static/                     # Uploaded images (auto-cleaned)
```

## Quick Start

### 1. Install Dependencies

```bash
pip install opencv-python fer pygame flask
```

### 2. Run Web App

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

### 3. Run Desktop App (alternative)

```bash
python emotion_music_player.py
```

## How It Works

### Emotion Detection Pipeline

```
Webcam / Photo → OpenCV capture → FER model → Emotion label
```

FER uses a deep neural network trained on FER-2013 dataset to detect 7 emotions:
`happy`, `sad`, `angry`, `neutral`, `surprise`, `fear`, `disgust`

### Music Selection

```
Detected Emotion → Emotion Map → Music Folder → Random Song → Play
```

If the detected emotion is `surprise`, it maps to `happy`. `fear` and `disgust` map to `neutral`.

## Web App UI

```
┌──────────────────────────────────┐
│     😊 Emotion Music Player      │
│  Show your face to play music    │
│                                  │
│  ┌──────────┐  ┌──────────┐     │
│  │ 📷 Cam   │  │ 📁 Photo │     │
│  │ Preview  │  │ Upload   │     │
│  └──────────┘  └──────────┘     │
│                                  │
│  ── Result Page ──               │
│  ┌──────────────────────┐        │
│  │ 😊 Happy             │        │
│  │ 5 tracks             │        │
│  │                      │        │
│  │ ♪ Song Name          │        │
│  │ ♪ Song Name        ▶│        │
│  │ ♪ Song Name          │        │
│  │ ...                  │        │
│  └──────────────────────┘        │
│                                  │
│  ┌── Bottom Player Bar ──┐       │
│  │ Song Name             │       │
│  │ ⏮  ▶  ⏭             │       │
│  │ ████████░░░░ 1:23/4:56│       │
│  └──────────────────────┘        │
└──────────────────────────────────┘
```

## Desktop App

The Tkinter desktop app provides:
- Start / Stop / Next Song buttons
- Pause/Resume toggle
- Volume slider
- Real-time emotion display
- Status indicator (Playing / Paused / Stopped)

## Customization

### Add Your Own Music

Place `.mp3` files in the corresponding folder under `music/`:

```
music/
├── happy/     # → your happy songs
├── sad/       # → your sad songs
├── angry/     # → your angry songs
└── neutral/   # → your neutral songs
```

### Change Emotion Mapping

Edit the `EMOTION_MAP` dictionary in `app.py`:

```python
EMOTION_MAP = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "neutral": "neutral",
    "surprise": "happy",    # surprise → happy folder
    "fear": "neutral",
    "disgust": "neutral"
}
```

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Show upload/capture page |
| `/` | POST | Upload image → detect emotion → show player |
| `/music/<folder>/<song>` | GET | Serve MP3 file |

## Notes

- First run loads TensorFlow + FER model (~10-15 seconds)
- Web app uses HTML5 Audio for playback (works in all modern browsers)
- Desktop app uses Pygame for playback
- No API keys required — all processing is local
