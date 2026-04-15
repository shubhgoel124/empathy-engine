Live Link: [https://shubhgoel124-empathy-engine-v2.hf.space/](url)

If this link dosent work from here copy it and paste it to your browser or you can click on the link in the about section

# 🧠 The Empathy Engine

**AI-driven Text-to-Speech that dynamically modulates vocal characteristics based on detected emotion.**

The Empathy Engine bridges the gap between text-based sentiment and expressive, human-like audio output. Instead of monotonic delivery, it analyzes the emotional content of text and programmatically adjusts **Pitch**, **Volume**, and **Speech Rate** to achieve emotional resonance — making AI sound genuinely enthusiastic, patient, urgent, or calm depending on the context.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Granular Emotion Detection** | Classifies text into 7 emotions: Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral |
| **3-Parameter Vocal Modulation** | Dynamically adjusts Pitch (semitones), Volume (dB), and Rate (speed multiplier) |
| **Intensity Scaling** | Modulation scales with classifier confidence — stronger emotions produce more dramatic vocal changes |
| **Full Emotion Spectrum** | Displays confidence scores for all 7 emotions, not just the top prediction |
| **Web Interface** | Premium glassmorphic UI with live particle effects, animated emotion bars, and embedded audio player |
| **Zero API Keys Required** | Runs entirely on open-source models and free APIs — no paid subscriptions needed |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Web Interface                     │
│        (Vanilla HTML / CSS / JavaScript)              │
└──────────────────────┬──────────────────────────────┘
                       │ POST /api/synthesize
                       ▼
┌─────────────────────────────────────────────────────┐
│                FastAPI Backend                        │
│                                                      │
│  ┌──────────────────┐    ┌───────────────────────┐  │
│  │ Emotion Detector │    │    Empathy TTS Engine  │  │
│  │                  │    │                        │  │
│  │  HuggingFace     │───▶│  1. Google TTS (base)  │  │
│  │  DistilRoBERTa   │    │  2. PitchShift (DSP)   │  │
│  │                  │    │  3. Gain (DSP)          │  │
│  │  Returns:        │    │  4. Rate Change (NumPy) │  │
│  │  - emotion       │    │                        │  │
│  │  - confidence    │    │  Returns: .wav audio    │  │
│  │  - all 7 scores  │    └───────────────────────┘  │
│  └──────────────────┘                                │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Emotion-to-Voice Mapping

The core design decision: each emotion maps to a **base profile** of vocal parameters. These base values are then **scaled by the classifier's confidence score** (0.0–1.0), implementing intensity scaling.

| Emotion | Base Pitch | Base Volume | Base Rate | Rationale |
|---------|-----------|-------------|-----------|-----------|
| **Joy** | +3.0 st | +2.0 dB | 1.18x | Higher pitch and faster pace convey excitement |
| **Sadness** | -4.0 st | -3.0 dB | 0.80x | Lower, quieter, and slower reflects grief |
| **Anger** | -2.0 st | +5.0 dB | 1.25x | Loud, fast, and deep pitch signals aggression |
| **Fear** | +4.0 st | -1.5 dB | 1.22x | High-pitched and fast, but quieter (whisper-like) |
| **Surprise** | +5.0 st | +2.5 dB | 1.12x | Dramatic pitch spike conveys shock |
| **Disgust** | -3.0 st | +0.5 dB | 0.88x | Low and slow signals displeasure |
| **Neutral** | 0.0 st | 0.0 dB | 1.00x | No modulation for neutral delivery |

### Intensity Scaling Formula

```
actual_pitch = base_pitch × confidence
actual_gain  = base_gain  × confidence
actual_rate  = 1.0 + (base_rate - 1.0) × confidence
```

**Example:** "This is good" (Joy, 62% confidence) → Pitch: +1.86 st, Gain: +1.24 dB, Rate: 1.11x  
**Example:** "This is the best news ever!" (Joy, 97% confidence) → Pitch: +2.91 st, Gain: +1.94 dB, Rate: 1.17x

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend Framework | **FastAPI** | Async REST API server |
| Emotion Detection | **HuggingFace Transformers** (`j-hartmann/emotion-english-distilroberta-base`) | 7-class emotion classification using DistilRoBERTa |
| Base TTS | **gTTS** (Google Text-to-Speech) | Generates clean baseline speech audio |
| Audio DSP | **Pedalboard** (by Spotify) | Professional-grade pitch shifting and gain adjustment |
| Rate Modulation | **NumPy** | Sample-level interpolation for speech rate manipulation |
| Frontend | **Vanilla HTML/CSS/JS** | Glassmorphic UI with particle effects and animated charts |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Internet connection (for gTTS and first-time model download)

### Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd empathy-engine

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
cd backend
uvicorn app:app --reload
```

> **Note:** On the first run, the system downloads the DistilRoBERTa emotion model (~328 MB). Subsequent startups are instant.

### 5. Open in Browser

Navigate to **http://127.0.0.1:8000/**

---

## 📝 Usage

1. Type or paste any English text into the input area
2. Click **"Generate Emotional Voice"**
3. The system will:
   - Classify the text across 7 emotions (displayed as animated bars)
   - Show the confidence score and intensity scaling percentage
   - Display the exact Pitch, Volume, and Rate parameters applied
   - Generate and auto-play the emotionally modulated audio

### Example Inputs to Try

| Input | Expected Emotion | Notable Effect |
|-------|-----------------|----------------|
| "I just got promoted, this is incredible!" | Joy | Higher pitch, faster pace |
| "I am so devastated by this terrible loss." | Sadness | Lower pitch, slower, quieter |
| "This is absolutely unacceptable and infuriating!" | Anger | Loud, fast, deep voice |
| "I'm terrified of what might happen tomorrow." | Fear | High pitch, fast, hushed |
| "The meeting starts at 9am in the conference room." | Neutral | No vocal modulation |

---

## 📁 Project Structure

```
empathy-engine/
├── backend/
│   ├── app.py          # FastAPI server and REST endpoint
│   ├── emotion.py      # HuggingFace emotion classifier wrapper
│   └── tts.py          # TTS synthesis + DSP modulation pipeline
├── frontend/
│   ├── index.html      # UI layout with analytics dashboard
│   ├── style.css       # Premium glassmorphic design system
│   └── script.js       # API integration, particles, charts
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🎨 Design Choices

### Why HuggingFace over TextBlob/VADER?
TextBlob and VADER only provide positive/negative/neutral sentiment polarity. The challenge requires granular emotions like "surprised" or "fearful." DistilRoBERTa was specifically fine-tuned on emotion datasets and provides 7-class classification with probability scores — enabling both granular detection and intensity scaling.

### Why gTTS + Pedalboard instead of pyttsx3?
`pyttsx3` produces robotic-sounding audio with limited parameter control. By using gTTS for high-quality baseline speech and Pedalboard (Spotify's audio DSP library) for post-processing, we get both natural-sounding voices AND precise control over pitch shifting and gain — similar to how a music producer would process audio in a DAW.

### Why NumPy for Rate instead of a library?
Speed/rate modulation requires resampling the audio signal. Rather than adding a heavy dependency like `librosa` or requiring system `ffmpeg`, we use NumPy's `interp` function for lightweight, pure-Python sample interpolation that works everywhere without system dependencies.

### Why base64 audio in JSON instead of streaming?
The API returns a rich JSON payload with emotion scores, parameters, and audio. This allows the frontend to render the full analytics dashboard (emotion spectrum, intensity bar, parameter cards) in a single request-response cycle without needing separate API calls.
