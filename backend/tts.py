from gtts import gTTS
import uuid
import os
import asyncio
import numpy as np
from pedalboard import Pedalboard, PitchShift, Gain
from pedalboard.io import AudioFile

VOICE_PROFILES = {
    "joy":      {"pitch": 3.0,  "gain": 2.0,  "rate": 1.18},
    "sadness":  {"pitch": -4.0, "gain": -3.0, "rate": 0.80},
    "anger":    {"pitch": -2.0, "gain": 5.0,  "rate": 1.25},
    "fear":     {"pitch": 4.0,  "gain": -1.5, "rate": 1.22},
    "surprise": {"pitch": 5.0,  "gain": 2.5,  "rate": 1.12},
    "disgust":  {"pitch": -3.0, "gain": 0.5,  "rate": 0.88},
    "neutral":  {"pitch": 0.0,  "gain": 0.0,  "rate": 1.00}
}

def change_rate(audio, rate_factor):
    if rate_factor == 1.0:
        return audio
    channels, length = audio.shape
    new_length = int(length / rate_factor)
    old_indices = np.arange(length)
    new_indices = np.linspace(0, length - 1, new_length)
    result = np.zeros((channels, new_length), dtype=np.float32)
    for ch in range(channels):
        result[ch] = np.interp(new_indices, old_indices, audio[ch].astype(np.float32))
    return result

def compute_audio_parameters(emotion, confidence):
    base_profile = VOICE_PROFILES.get(emotion, VOICE_PROFILES["neutral"])
    
    pitch = round(base_profile["pitch"] * confidence, 2)
    gain = round(base_profile["gain"] * confidence, 2)
    
    rate = round(1.0 + (base_profile["rate"] - 1.0) * confidence, 3)
    
    return {"pitch_st": pitch, "gain_db": gain, "rate": rate}

def synthesize_audio(text, emotion, confidence):
    params = compute_audio_parameters(emotion, confidence)
    
    temp_file = f"temp_{uuid.uuid4().hex}.mp3"
    out_file = f"output_{uuid.uuid4().hex}.wav"

    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(temp_file)

    board = Pedalboard([
        PitchShift(semitones=params["pitch_st"]),
        Gain(gain_db=params["gain_db"])
    ])

    with AudioFile(temp_file) as f:
        audio_data = f.read(f.frames)
        sample_rate = f.samplerate

    effected_audio = board(audio_data, sample_rate)
    
    effected_audio = change_rate(effected_audio, params["rate"])

    with AudioFile(out_file, 'w', sample_rate, effected_audio.shape[0]) as f:
        f.write(effected_audio)

    if os.path.exists(temp_file):
        os.remove(temp_file)

    return out_file, params
