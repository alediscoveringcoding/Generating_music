#!/usr/bin/env python3
code = """#!/usr/bin/env python3

import os
import json
import logging
import wave
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GENRE_SETTINGS = {
    "classical": {"temperature": 0.8, "steps": 320, "timbre": "sine", "reverb": 0.5, "base_freq": 60, "attack": 0.05, "release": 0.3},
    "pop": {"temperature": 1.0, "steps": 256, "timbre": "sine", "reverb": 0.2, "base_freq": 80, "attack": 0.02, "release": 0.2},
    "jazz": {"temperature": 1.2, "steps": 300, "timbre": "sine", "reverb": 0.4, "base_freq": 70, "attack": 0.08, "release": 0.4},
    "rock": {"temperature": 1.1, "steps": 280, "timbre": "square", "reverb": 0.25, "base_freq": 100, "attack": 0.01, "release": 0.15},
    "rap": {"temperature": 0.9, "steps": 240, "timbre": "sawtooth", "reverb": 0.1, "base_freq": 110, "attack": 0.005, "release": 0.1},
    "electronic": {"temperature": 1.3, "steps": 350, "timbre": "square", "reverb": 0.35, "base_freq": 90, "attack": 0.01, "release": 0.25},
    "ambient": {"temperature": 0.7, "steps": 400, "timbre": "sine", "reverb": 0.8, "base_freq": 50, "attack": 0.2, "release": 0.5},
    "folk": {"temperature": 0.95, "steps": 300, "timbre": "sine", "reverb": 0.3, "base_freq": 75, "attack": 0.03, "release": 0.25}
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_music")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "music_history.json")


def gen_wave(freq, samples, timbre, sr=44100):
    t = np.arange(samples, dtype=np.float32) / sr
    if timbre == "sine":
        return np.sin(2 * np.pi * freq * t)
    elif timbre == "square":
        return np.sign(np.sin(2 * np.pi * freq * t))
    elif timbre == "sawtooth":
        return 2 * (t * freq - np.floor(t * freq + 0.5))
    else:
        return np.sin(2 * np.pi * freq * t)


def apply_adsr(wave_data, attack, release, sr=44100):
    samples = len(wave_data)
    envelope = np.ones(samples, dtype=np.float32)
    attack_samples = int(attack * sr)
    release_samples = int(release * sr)
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    if release_samples > 0:
        envelope[-release_samples:] = np.linspace(1, 0, release_samples)
    return wave_data * envelope


def generate_music(genre, temperature=1.0, steps=256, seed_note=60, sr=44100):
    try:
        if genre not in GENRE_SETTINGS:
            raise ValueError(f"Unknown genre: {genre}")
        settings = GENRE_SETTINGS[genre]
        base_freq = settings["base_freq"] + (temperature - 1.0) * 20
        duration = steps / 100.0
        num_samples = int(sr * duration)
        wave_data = gen_wave(base_freq, num_samples, settings["timbre"], sr)
        wave_data = apply_adsr(wave_data, settings["attack"], settings["release"], sr)
        for harmonic in [2, 3]:
            harmonic_data = gen_wave(base_freq * harmonic, num_samples, settings["timbre"], sr)
            harmonic_data = apply_adsr(harmonic_data, settings["attack"], settings["release"], sr)
            wave_data += harmonic_data * (0.5 / harmonic)
        reverb_amount = settings["reverb"]
        if reverb_amount > 0:
            delay_samples = int(sr * 0.05)
            delayed = np.zeros_like(wave_data)
            delayed[delay_samples:] = wave_data[:-delay_samples]
            wave_data = wave_data * (1 - reverb_amount) + delayed * reverb_amount
        max_val = np.max(np.abs(wave_data))
        if max_val > 1.0:
            wave_data = wave_data / max_val
        wave_data = np.int16(wave_data * 32767)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{genre}_{timestamp}.wav"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with wave.open(str(filepath), 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sr)
            wav_file.writeframes(wave_data.tobytes())
        logger.info(f"Generated music: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error generating music: {str(e)}")
        raise


def save_to_history(genre, filename, temperature, steps):
    try:
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        history.append({"timestamp": datetime.now().isoformat(), "genre": genre, "filename": filename, "temperature": temperature, "steps": steps})
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving to history: {str(e)}")


def get_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Error reading history: {str(e)}")
        return []


def get_all_genres():
    return list(GENRE_SETTINGS.keys())


class MusicGenerator:
    def __init__(self):
        self.sample_rate = 44100
        self.genres = get_all_genres()
    
    def generate(self, genre, temperature=1.0, steps=256, seed_note=60):
        try:
            filename = generate_music(genre, temperature, steps, seed_note, self.sample_rate)
            save_to_history(genre, filename, temperature, steps)
            return filename
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise
    
    def get_genres(self):
        return self.genres
    
    def get_file_path(self, filename):
        return os.path.join(OUTPUT_DIR, filename)


def get_generator():
    return MusicGenerator()
"""

with open("music_generator.py", "w") as f:
    f.write(code)
print("File created successfully")
