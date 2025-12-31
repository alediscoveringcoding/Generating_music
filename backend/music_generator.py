#!/usr/bin/env python3
"""
AI Music Generator - Generator de muzică avansat
Fiecare gen are caracteristici sonore unice și distincte
Durata minimă: 60+ secunde
"""

import os
import json
import logging
import wave
import random
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurări avansate pentru fiecare gen - DURATE LUNGI (60+ secunde)
GENRE_SETTINGS = {
    "classical": {
        "temperature": 0.8,
        "steps": 800,
        "timbre": "orchestral",
        "reverb": 0.6,
        "bpm": 72,
        "key": "C",
        "scale": "major",
        "description": "Muzică clasică orchestrală cu armonii complexe",
        "characteristics": ["strings", "piano", "legato", "dynamics"]
    },
    "pop": {
        "temperature": 1.0,
        "steps": 750,
        "timbre": "bright",
        "reverb": 0.3,
        "bpm": 120,
        "key": "G",
        "scale": "major",
        "description": "Muzică pop modernă cu beat catchy",
        "characteristics": ["synth", "drums", "catchy", "verse-chorus"]
    },
    "jazz": {
        "temperature": 1.3,
        "steps": 900,
        "timbre": "warm",
        "reverb": 0.5,
        "bpm": 110,
        "key": "Bb",
        "scale": "blues",
        "description": "Jazz cu improvizații și acorduri complexe",
        "characteristics": ["swing", "brass", "piano", "walking_bass"]
    },
    "rock": {
        "temperature": 1.1,
        "steps": 700,
        "timbre": "distorted",
        "reverb": 0.35,
        "bpm": 130,
        "key": "E",
        "scale": "pentatonic",
        "description": "Rock energic cu chitare distorsionate",
        "characteristics": ["power_chords", "drums", "guitar_riff", "energy"]
    },
    "rap": {
        "temperature": 0.9,
        "steps": 650,
        "timbre": "bass_heavy",
        "reverb": 0.2,
        "bpm": 90,
        "key": "Am",
        "scale": "minor",
        "description": "Hip-hop cu bass puternic și beat-uri distinctive",
        "characteristics": ["808_bass", "hi_hats", "trap", "boom_bap"]
    },
    "electronic": {
        "temperature": 1.2,
        "steps": 850,
        "timbre": "synthetic",
        "reverb": 0.4,
        "bpm": 128,
        "key": "F",
        "scale": "minor",
        "description": "Muzică electronică cu sintetizatoare și drop-uri",
        "characteristics": ["synth_lead", "arpeggios", "build_up", "drop"]
    },
    "ambient": {
        "temperature": 0.6,
        "steps": 1200,
        "timbre": "ethereal",
        "reverb": 0.85,
        "bpm": 60,
        "key": "D",
        "scale": "dorian",
        "description": "Muzică ambientală relaxantă cu texturi eterice",
        "characteristics": ["pads", "atmosphere", "slow", "reverb_heavy"]
    },
    "folk": {
        "temperature": 0.9,
        "steps": 800,
        "timbre": "acoustic",
        "reverb": 0.35,
        "bpm": 100,
        "key": "C",
        "scale": "major",
        "description": "Folk acustic cu chitară și melodii tradiționale",
        "characteristics": ["acoustic_guitar", "fingerpicking", "natural", "storytelling"]
    }
}

SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "pentatonic": [0, 2, 4, 7, 9],
    "blues": [0, 3, 5, 6, 7, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10]
}

KEY_BASE = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
    "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71,
    "Am": 57, "Bb": 58, "Dm": 62, "Em": 64, "Fm": 65, "Gm": 67
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_music")
os.makedirs(OUTPUT_DIR, exist_ok=True)
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "music_history.json")


def midi_to_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def generate_waveform(freq, duration, sr, timbre, genre):
    t = np.linspace(0, duration, int(sr * duration), dtype=np.float32)
    
    if timbre == "orchestral":
        wave = np.sin(2 * np.pi * freq * t) * 0.5
        wave += np.sin(2 * np.pi * freq * 2 * t) * 0.25
        wave += np.sin(2 * np.pi * freq * 3 * t) * 0.15
        wave += np.sin(2 * np.pi * freq * 4 * t) * 0.1
        vibrato = 1 + 0.003 * np.sin(2 * np.pi * 5.5 * t)
        wave = np.sin(2 * np.pi * freq * vibrato * t) * 0.6 + wave * 0.4
        
    elif timbre == "bright":
        wave = np.sin(2 * np.pi * freq * t) * 0.6
        wave += np.sin(2 * np.pi * freq * 2 * t) * 0.3
        wave += np.sin(2 * np.pi * freq * 3 * t) * 0.15
        shimmer = np.sin(2 * np.pi * freq * 4 * t) * 0.1 * np.sin(2 * np.pi * 2 * t)
        wave += shimmer
        
    elif timbre == "warm":
        wave = np.sin(2 * np.pi * freq * t) * 0.5
        wave += np.sin(2 * np.pi * freq * 2 * t) * 0.35
        wave += np.sin(2 * np.pi * freq * 3 * t) * 0.15 * np.exp(-t * 2)
        
    elif timbre == "distorted":
        wave = np.sin(2 * np.pi * freq * t)
        wave += np.sin(2 * np.pi * freq * 2 * t) * 0.5
        wave = np.tanh(wave * 3) * 0.7
        wave += np.tanh(np.sin(2 * np.pi * freq * 1.5 * t) * 2) * 0.4
        
    elif timbre == "bass_heavy":
        wave = np.sin(2 * np.pi * freq * t) * 0.7
        sub_freq = freq / 2
        wave += np.sin(2 * np.pi * sub_freq * t) * 0.5
        wave += np.sin(2 * np.pi * freq * t) * np.exp(-t * 4) * 0.3
        
    elif timbre == "synthetic":
        wave = np.sin(2 * np.pi * freq * t) * 0.4
        sawtooth = 2 * (t * freq - np.floor(t * freq + 0.5))
        wave += sawtooth * 0.3
        square = np.sign(np.sin(2 * np.pi * freq / 2 * t))
        wave += square * 0.2
        wave += np.sin(2 * np.pi * freq * 1.01 * t) * 0.2
        
    elif timbre == "ethereal":
        wave = np.sin(2 * np.pi * freq * t) * 0.4
        wave += np.sin(2 * np.pi * freq * 2 * t) * 0.2
        lfo = np.sin(2 * np.pi * 0.2 * t)
        wave *= (0.7 + 0.3 * lfo)
        wave += np.sin(2 * np.pi * freq * 1.005 * t) * 0.25
        wave += np.sin(2 * np.pi * freq * 0.995 * t) * 0.25
        
    elif timbre == "acoustic":
        wave = np.sin(2 * np.pi * freq * t) * 0.5
        wave += np.sin(2 * np.pi * freq * 2 * t) * 0.3
        wave += np.sin(2 * np.pi * freq * 3 * t) * 0.15
        wave += np.sin(2 * np.pi * freq * 4 * t) * 0.08
        decay = np.exp(-t * 1.5)
        wave *= decay
    else:
        wave = np.sin(2 * np.pi * freq * t)
    
    return wave


def apply_envelope(wave, attack, decay, sustain, release, sr):
    samples = len(wave)
    envelope = np.ones(samples, dtype=np.float32)
    
    attack_samples = int(attack * sr)
    decay_samples = int(decay * sr)
    release_samples = int(release * sr)
    sustain_samples = samples - attack_samples - decay_samples - release_samples
    
    if sustain_samples < 0:
        sustain_samples = 0
    
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    start = attack_samples
    end = start + decay_samples
    if decay_samples > 0 and end <= samples:
        envelope[start:end] = np.linspace(1, sustain, decay_samples)
    
    start = attack_samples + decay_samples
    end = start + sustain_samples
    if sustain_samples > 0 and end <= samples:
        envelope[start:end] = sustain
    
    if release_samples > 0:
        envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
    
    return wave * envelope


def apply_reverb(wave, amount, sr):
    if amount <= 0:
        return wave
    
    output = wave.copy()
    delays = [int(sr * d) for d in [0.03, 0.05, 0.07, 0.11]]
    gains = [0.4, 0.3, 0.2, 0.15]
    
    for delay, gain in zip(delays, gains):
        if delay < len(wave):
            delayed = np.zeros_like(wave)
            delayed[delay:] = wave[:-delay]
            output += delayed * gain * amount
    
    return output


def generate_drum_pattern(duration, bpm, sr, genre):
    samples = int(sr * duration)
    drums = np.zeros(samples, dtype=np.float32)
    
    beat_duration = 60.0 / bpm
    beat_samples = int(beat_duration * sr)
    sixteenth = beat_samples // 4
    
    kick_env = np.exp(-np.linspace(0, 10, int(sr * 0.15)))
    kick = np.sin(2 * np.pi * 60 * np.linspace(0, 0.15, int(sr * 0.15))) * kick_env
    
    snare_noise = np.random.randn(int(sr * 0.1)) * 0.5
    snare_env = np.exp(-np.linspace(0, 15, int(sr * 0.1)))
    snare = snare_noise * snare_env
    snare += np.sin(2 * np.pi * 200 * np.linspace(0, 0.1, int(sr * 0.1))) * snare_env * 0.5
    
    hihat_noise = np.random.randn(int(sr * 0.05)) * 0.3
    hihat_env = np.exp(-np.linspace(0, 30, int(sr * 0.05)))
    hihat = hihat_noise * hihat_env
    
    if genre == "pop":
        for i in range(int(duration / beat_duration)):
            pos = i * beat_samples
            if pos + len(kick) < samples:
                drums[pos:pos+len(kick)] += kick * 0.8
            if i % 2 == 1 and pos + len(snare) < samples:
                drums[pos:pos+len(snare)] += snare * 0.7
            for j in range(2):
                hh_pos = pos + j * (beat_samples // 2)
                if hh_pos + len(hihat) < samples:
                    drums[hh_pos:hh_pos+len(hihat)] += hihat * 0.4
                    
    elif genre == "rock":
        for i in range(int(duration / beat_duration)):
            pos = i * beat_samples
            if pos + len(kick) < samples:
                drums[pos:pos+len(kick)] += kick * 0.9
            if i % 2 == 1 and pos + len(snare) < samples:
                drums[pos:pos+len(snare)] += snare * 0.85
            for j in range(4):
                hh_pos = pos + j * sixteenth
                if hh_pos + len(hihat) < samples:
                    drums[hh_pos:hh_pos+len(hihat)] += hihat * 0.5
                    
    elif genre == "rap":
        for i in range(int(duration / beat_duration)):
            pos = i * beat_samples
            if pos + len(kick) < samples:
                drums[pos:pos+len(kick)] += kick * 1.0
            kick_pos2 = pos + int(beat_samples * 0.75)
            if kick_pos2 + len(kick) < samples and i % 2 == 0:
                drums[kick_pos2:kick_pos2+len(kick)] += kick * 0.8
            if i % 2 == 1 and pos + len(snare) < samples:
                drums[pos:pos+len(snare)] += snare * 0.7
            for j in range(8):
                hh_pos = pos + j * (beat_samples // 8)
                vol = 0.3 if j % 2 == 0 else 0.2
                if hh_pos + len(hihat) < samples:
                    drums[hh_pos:hh_pos+len(hihat)] += hihat * vol
                    
    elif genre == "electronic":
        for i in range(int(duration / beat_duration)):
            pos = i * beat_samples
            progress = i / max(1, (duration / beat_duration))
            intensity = min(1.0, progress * 1.5) if progress < 0.7 else 1.0
            
            if pos + len(kick) < samples:
                drums[pos:pos+len(kick)] += kick * intensity
            if i % 2 == 1 and pos + len(snare) < samples:
                drums[pos:pos+len(snare)] += snare * 0.6 * intensity
            for j in range(4):
                hh_pos = pos + j * sixteenth
                if hh_pos + len(hihat) < samples:
                    drums[hh_pos:hh_pos+len(hihat)] += hihat * 0.4 * intensity
                    
    elif genre == "jazz":
        ride = np.random.randn(int(sr * 0.08)) * 0.25
        ride_env = np.exp(-np.linspace(0, 20, int(sr * 0.08)))
        ride = ride * ride_env
        
        for i in range(int(duration / beat_duration)):
            pos = i * beat_samples
            if pos + len(ride) < samples:
                drums[pos:pos+len(ride)] += ride * 0.5
            swing_pos = pos + int(beat_samples * 0.66)
            if swing_pos + len(ride) < samples:
                drums[swing_pos:swing_pos+len(ride)] += ride * 0.3
            if i % 4 == 0 and pos + len(kick) < samples:
                drums[pos:pos+len(kick)] += kick * 0.4
            if i % 4 == 2 and pos + len(snare) < samples:
                drums[pos:pos+len(snare)] += snare * 0.35
                
    elif genre == "folk":
        for i in range(int(duration / beat_duration)):
            pos = i * beat_samples
            if i % 4 == 0 and pos + len(kick) < samples:
                drums[pos:pos+len(kick)] += kick * 0.5
            if i % 2 == 1 and pos + len(snare) < samples:
                drums[pos:pos+len(snare)] += snare * 0.3
    
    return drums * 0.6


def generate_bass_line(notes, durations, sr, genre):
    bass = np.array([], dtype=np.float32)
    
    for note, dur in zip(notes, durations):
        freq = midi_to_freq(note - 12)
        t = np.linspace(0, dur, int(sr * dur), dtype=np.float32)
        
        if genre == "rap":
            wave = np.sin(2 * np.pi * freq * t) * 0.8
            wave += np.sin(2 * np.pi * freq / 2 * t) * 0.4
            env = np.exp(-t * 2)
            wave *= env
        elif genre == "rock":
            wave = np.sin(2 * np.pi * freq * t)
            wave = np.tanh(wave * 1.5) * 0.7
        elif genre == "jazz":
            wave = np.sin(2 * np.pi * freq * t) * 0.6
            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.2
        elif genre == "electronic":
            wave = np.sin(2 * np.pi * freq * t) * 0.5
            saw = 2 * (t * freq - np.floor(t * freq + 0.5))
            wave += saw * 0.3
        else:
            wave = np.sin(2 * np.pi * freq * t) * 0.5
            
        bass = np.concatenate([bass, wave])
    
    return bass


def generate_melody(key, scale, duration, bpm, sr, genre, temperature):
    base_note = KEY_BASE.get(key, 60)
    scale_intervals = SCALES.get(scale, SCALES["major"])
    
    melody = np.array([], dtype=np.float32)
    bass_notes = []
    bass_durations = []
    
    current_time = 0
    prev_note_idx = 0
    
    while current_time < duration:
        if genre == "ambient":
            note_dur = random.choice([2.0, 3.0, 4.0])
        elif genre == "electronic":
            note_dur = random.choice([0.25, 0.5, 0.5, 1.0])
        elif genre == "jazz":
            note_dur = random.choice([0.33, 0.5, 0.67, 1.0])
        elif genre == "classical":
            note_dur = random.choice([0.5, 1.0, 1.5, 2.0])
        elif genre == "rap":
            note_dur = random.choice([0.5, 1.0, 1.0, 2.0])
        else:
            note_dur = random.choice([0.5, 0.5, 1.0, 1.0])
        
        if current_time + note_dur > duration:
            note_dur = duration - current_time
        
        if random.random() < temperature * 0.3:
            note_idx = random.randint(0, len(scale_intervals) - 1)
        else:
            step = random.choice([-2, -1, -1, 0, 1, 1, 2])
            note_idx = max(0, min(len(scale_intervals) - 1, prev_note_idx + step))
        
        octave_shift = random.choice([0, 0, 0, 12, -12]) if genre != "ambient" else random.choice([0, 0, 12])
        midi_note = base_note + scale_intervals[note_idx] + octave_shift
        
        freq = midi_to_freq(midi_note)
        wave = generate_waveform(freq, note_dur, sr, GENRE_SETTINGS[genre]["timbre"], genre)
        
        if genre == "classical":
            wave = apply_envelope(wave, 0.1, 0.2, 0.7, 0.3, sr)
        elif genre == "ambient":
            wave = apply_envelope(wave, 0.5, 0.3, 0.8, 0.5, sr)
        elif genre == "electronic":
            wave = apply_envelope(wave, 0.01, 0.1, 0.6, 0.1, sr)
        elif genre == "jazz":
            wave = apply_envelope(wave, 0.05, 0.15, 0.6, 0.2, sr)
        elif genre == "rock":
            wave = apply_envelope(wave, 0.01, 0.1, 0.8, 0.15, sr)
        elif genre == "rap":
            wave = apply_envelope(wave, 0.01, 0.05, 0.7, 0.1, sr)
        else:
            wave = apply_envelope(wave, 0.02, 0.1, 0.7, 0.15, sr)
        
        melody = np.concatenate([melody, wave])
        
        bass_notes.append(base_note + scale_intervals[note_idx % len(scale_intervals)])
        bass_durations.append(note_dur)
        
        prev_note_idx = note_idx
        current_time += note_dur
    
    return melody, bass_notes, bass_durations


def generate_music(genre, temperature=1.0, steps=256, seed_note=60, sr=44100):
    try:
        if genre not in GENRE_SETTINGS:
            raise ValueError(f"Unknown genre: {genre}")
        
        settings = GENRE_SETTINGS[genre]
        random.seed(seed_note + int(temperature * 1000))
        np.random.seed(seed_note)
        
        duration = max(60, steps / 10.0)
        bpm = settings["bpm"]
        key = settings["key"]
        scale = settings["scale"]
        
        logger.info(f"Generating {genre} music: {duration:.1f}s at {bpm} BPM in {key} {scale}")
        
        melody, bass_notes, bass_durations = generate_melody(
            key, scale, duration, bpm, sr, genre, temperature
        )
        
        target_samples = int(sr * duration)
        if len(melody) < target_samples:
            melody = np.pad(melody, (0, target_samples - len(melody)))
        else:
            melody = melody[:target_samples]
        
        bass = generate_bass_line(bass_notes, bass_durations, sr, genre)
        if len(bass) < target_samples:
            bass = np.pad(bass, (0, target_samples - len(bass)))
        else:
            bass = bass[:target_samples]
        
        drums = generate_drum_pattern(duration, bpm, sr, genre)
        if len(drums) < target_samples:
            drums = np.pad(drums, (0, target_samples - len(drums)))
        else:
            drums = drums[:target_samples]
        
        if genre == "classical":
            mix = melody * 0.8 + bass * 0.2
        elif genre == "ambient":
            mix = melody * 0.9 + bass * 0.1
        elif genre == "rap":
            mix = melody * 0.3 + bass * 0.5 + drums * 0.5
        elif genre == "electronic":
            mix = melody * 0.4 + bass * 0.4 + drums * 0.5
        elif genre == "rock":
            mix = melody * 0.5 + bass * 0.35 + drums * 0.45
        elif genre == "jazz":
            mix = melody * 0.5 + bass * 0.35 + drums * 0.25
        else:
            mix = melody * 0.5 + bass * 0.3 + drums * 0.35
        
        mix = apply_reverb(mix, settings["reverb"], sr)
        
        max_val = np.max(np.abs(mix))
        if max_val > 0:
            mix = mix / max_val * 0.9
        
        wave_data = np.int16(mix * 32767)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{genre}_{timestamp}.wav"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with wave.open(str(filepath), 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sr)
            wav_file.writeframes(wave_data.tobytes())
        
        logger.info(f"Generated music: {filename} ({duration:.1f}s)")
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
        
        settings = GENRE_SETTINGS.get(genre, {})
        history.append({
            "timestamp": datetime.now().isoformat(),
            "genre": genre,
            "filename": filename,
            "temperature": temperature,
            "steps": steps,
            "duration": max(60, steps / 10.0),
            "bpm": settings.get("bpm", 120)
        })
        
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
    result = {}
    for genre, settings in GENRE_SETTINGS.items():
        result[genre] = {
            "name": genre.capitalize(),
            "description": settings.get("description", f"Muzică {genre}"),
            "default_temperature": settings.get("temperature", 1.0),
            "default_steps": settings.get("steps", 700),
            "bpm": settings.get("bpm", 120),
            "key": settings.get("key", "C"),
            "scale": settings.get("scale", "major"),
            "timbre": settings.get("timbre", "sine"),
            "reverb": settings.get("reverb", 0.3),
            "characteristics": settings.get("characteristics", [])
        }
    return result


class MusicGenerator:
    def __init__(self):
        self.sample_rate = 44100
        self.genres = get_all_genres()
    
    def generate(self, genre, temperature=1.0, steps=700, seed_note=60):
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
