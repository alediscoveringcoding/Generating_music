# 🏗️ PROJECT STRUCTURE & OVERVIEW

```
ai-music-generator/
│
├── 📁 backend/
│   ├── main.py                    # FastAPI server (endpoints REST)
│   ├── music_generator.py         # Logica generare Magenta
│   ├── requirements.txt           # Dependențe Python
│   ├── .env.example              # Template env variables
│   │
│   ├── 📁 models/
│   │   └── basic_rnn.mag         # ⬇️ Descarcă model Magenta
│   │
│   └── 📁 generated_music/
│       ├── *.mid                 # Fișiere MIDI generate
│       └── generation_history.json # Istoric generări
│
├── 📁 frontend/
│   ├── index.html                # Interfață web
│   ├── style.css                 # Design modern (dark theme)
│   └── script.js                 # Logică client JavaScript
│
├── 📁 docs/
│   ├── README.md                 # Documentație completă
│   ├── QUICK_START.md            # Setup rapid (15 min)
│   ├── INSTALLATION_GUIDE.md     # Instalare detaliat
│   └── API_REFERENCE.md          # Endpoints documentation
│
├── 📄 config.json                # Configurare aplicație
├── 📄 .env.example              # Template variabile mediu
├── 📄 .gitignore                # Git ignore patterns
│
├── 🚀 START.bat                  # Script startup Windows
└── 🚀 start.sh                   # Script startup Unix
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ HTML5 / CSS3 / Vanilla JavaScript                    │  │
│  │ ├─ Genre Selection Dropdown                          │  │
│  │ ├─ Advanced Parameters (Temperature, Steps, Seed)   │  │
│  │ ├─ Generation Button + Audio Player                 │  │
│  │ ├─ Generation History List                          │  │
│  │ └─ Real-time Statistics Dashboard                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ⬇️ HTTP REST
                   (JSON Request/Response)
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ /generate (POST)                                     │  │
│  │ /genres (GET)                                        │  │
│  │ /download/{filename} (GET)                           │  │
│  │ /history (GET)                                       │  │
│  │ /delete/{filename} (DELETE)                          │  │
│  │ /stats (GET)                                         │  │
│  │ /health (GET)                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ⬇️
│  ┌──────────────────────────────────────────────────────┐  │
│  │              MusicGenerator Class                    │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │ • Load/Initialize Magenta Model              │   │  │
│  │  │ • Generate Sequence (melody_rnn)             │   │  │
│  │  │ • Convert to MIDI (note_seq)                 │   │  │
│  │  │ • Save File + Metadata                       │   │  │
│  │  │ • Manage History (JSON)                      │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ⬇️
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AI/ML Components (Magenta/TensorFlow)       │  │
│  │  ├─ Melody RNN Model (trained)                      │  │
│  │  ├─ Temperature Sampling (creativity)               │  │
│  │  ├─ Sequence Generation                             │  │
│  │  └─ MIDI Serialization                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ⬇️
┌─────────────────────────────────────────────────────────────┐
│                    STORAGE & FILES                           │
│  ├─ generated_music/*.mid (MIDI files)                      │
│  ├─ generation_history.json (metadata)                      │
│  └─ models/basic_rnn.mag (AI checkpoint)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 API Endpoints Map

```
FastAPI Server (http://127.0.0.1:8000)
│
├── 📌 GET /                         → API Info
├── 🎵 GET /genres                   → List all genres + details
├── 🎵 GET /genre/{name}             → Genre specific info
│
├── 🎹 POST /generate                → Generate music
├── 🎹 GET /generate/{genre}         → Quick generate (deprecated)
│
├── 📥 GET /download/{filename}      → Download MIDI file
├── 📜 GET /history?limit=10         → Generation history
├── 🗑️ DELETE /delete/{filename}     → Remove file
│
├── 📊 GET /stats                    → Usage statistics
├── 💚 GET /health                   → Server health check
│
└── 📖 GET /docs                     → Swagger UI (interactive)
    GET /redoc                       → ReDoc (alternative UI)
    GET /openapi.json               → OpenAPI spec
```

---

## 💾 Key Files Explanation

### Backend

| File | Rol | Linie cod |
|------|-----|-----------|
| `main.py` | FastAPI server + routes | ~285 |
| `music_generator.py` | Magenta logic + history | ~450 |
| `requirements.txt` | Dependențe Python | ~9 |

### Frontend

| File | Rol | Linie cod |
|------|-----|-----------|
| `index.html` | Markup + structure | ~150 |
| `style.css` | Design + animations | ~700 |
| `script.js` | Client logic + API calls | ~500 |

### Documentation

| File | Conținut |
|------|----------|
| `README.md` | Documentație completă |
| `QUICK_START.md` | Setup rapid |
| `INSTALLATION_GUIDE.md` | Instalare detaliat |
| `config.json` | Configurări aplicație |

---

## 🔐 Security Features

✅ **CORS Configuration**
- Permite frontend să comunice cu backend
- Restricții pe origin dacă necesare

✅ **Path Validation**
- Previne path traversal attacks (delete/download)
- Validare filename sigură

✅ **Input Validation**
- Pydantic models pentru validare
- Range checks (temperature, steps, seed_note)
- Genre whitelist validation

✅ **Error Handling**
- Try/catch comprehensive
- Proper HTTP status codes
- Informative error messages

---

## 📈 Performance Metrics

```
Generare Muzică:
├─ First run: 30-60 sec (model initialization)
├─ Subsequent: 15-30 sec
├─ Depinde de:
│  ├─ Steps (100-500)
│  ├─ System RAM (4GB+ ideal)
│  └─ CPU cores

File Size:
├─ Typical MIDI: 3-10 KB
├─ Storage: ~1 MB per 100 files

Memory Usage:
├─ Backend: ~500 MB (Magenta loaded)
├─ Frontend: ~50 MB (browser)
```

---

## 🔄 Architecture Decisions

### 1. **Vanilla JavaScript vs Framework**
- ✅ Vanilla JS: No build process, simpler deployment
- ❌ React/Vue: Overkill pentru app simplă

### 2. **FastAPI vs Django/Flask**
- ✅ FastAPI: Modern, async, auto OpenAPI docs
- ❌ Django: Too heavy for microservice
- ❌ Flask: Less type-safe

### 3. **Local Models vs Cloud API**
- ✅ Local: Privacy, offline capability, cost-free
- ❌ Cloud: Latency, API costs, vendor lock-in

### 4. **MIDI vs WAV/MP3**
- ✅ MIDI: Small files, editable, lightweight
- ❌ WAV: Large files, not editable
- ❌ MP3: Need encoding, licensing issues

---

## 🚀 Deployment Options

### Option 1: Local (Current)
- Pro: Simple, offline, full control
- Con: Requires local Python setup

### Option 2: Docker Container
```bash
docker build -t music-generator .
docker run -p 8000:8000 -p 5500:5500 music-generator
```

### Option 3: Cloud Deployment
- Heroku, Railway, Render (Python backend)
- Vercel, Netlify (static frontend)
- AWS Lambda (serverless generation)

### Option 4: Electron Desktop App
- Wrap frontend + backend in Electron
- Distribuit ca standalone exe

---

## 📊 Technology Stack Summary

```
┌─ Frontend ─────────────────┐
│ HTML5 / CSS3 / JS (Vanilla)│
│ Audio API / Fetch API      │
│ Responsive Design          │
└────────────────────────────┘
         ⬇️ HTTP
┌─ Backend ──────────────────┐
│ Python 3.9+                │
│ FastAPI (Web Framework)    │
│ Pydantic (Validation)      │
└────────────────────────────┘
         ⬇️ Library
┌─ AI/ML ────────────────────┐
│ Magenta (Google)           │
│ TensorFlow (Deep Learning) │
│ note-seq (MIDI proc.)      │
└────────────────────────────┘
         ⬇️ Output
┌─ Storage ──────────────────┐
│ MIDI Files (local)         │
│ JSON History               │
│ Model Checkpoint           │
└────────────────────────────┘
```

---

## 🎓 Learning Resources

Daca vrei sa intelegi arhitectura:

1. **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
2. **Magenta Guide**: https://magenta.tensorflow.org/
3. **Modern CSS**: https://developer.mozilla.org/en-US/docs/Learn/CSS
4. **JavaScript Async**: https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous
5. **MIDI Format**: https://en.wikipedia.org/wiki/MIDI

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: December 30, 2025
