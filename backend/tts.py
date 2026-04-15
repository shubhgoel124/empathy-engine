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

class EmpathyTTS:
    def __init__(self):
        pass

    def compute_params(self, emotion: str, confidence: float) -> dict:
        base = VOICE_PROFILES.get(emotion, VOICE_PROFILES["neutral"])
        scaled_pitch = round(base["pitch"] * confidence, 2)
        scaled_gain = round(base["gain"] * confidence, 2)
        scaled_rate = round(1.0 + (base["rate"] - 1.0) * confidence, 3)
        return {"pitch_st": scaled_pitch, "gain_db": scaled_gain, "rate": scaled_rate}

    async def synthesize(self, text: str, emotion: str, confidence: float) -> tuple:
        params = self.compute_params(emotion, confidence)
        temp_file = f"temp_{uuid.uuid4().hex}.mp3"
        out_file = f"output_{uuid.uuid4().hex}.wav"

        def generate_base():
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(temp_file)

        await asyncio.to_thread(generate_base)

        board = Pedalboard([
            PitchShift(semitones=params["pitch_st"]),
            Gain(gain_db=params["gain_db"])
        ])

        with AudioFile(temp_file) as f:
            audio = f.read(f.frames)
            samplerate = f.samplerate

        effected = board(audio, samplerate)
        effected = change_rate(effected, params["rate"])

        with AudioFile(out_file, 'w', samplerate, effected.shape[0]) as f:
            f.write(effected)

        if os.path.exists(temp_file):
            os.remove(temp_file)

        return out_file, params

tts_engine = EmpathyTTS()
