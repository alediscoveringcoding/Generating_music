# 🚀 Quick Start Guide - AI Music Generator

**Timp estimat instalare**: 15-20 minute

## ⚡ Fast Setup (4 pași)

### 1️⃣ Pregătire Mediu Python

```powershell
# Navigează la proiect
cd "C:\Users\Einsteinn\Documents\Albumu meu\ai-music-generator\backend"

# Crează mediu virtual
python -m venv venv

# Activează (Choose one):
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
```

### 2️⃣ Instalează Dependențe

```powershell
# Asigură-te că venv e activ (trebuie să vezi (venv) în prompt)
pip install -r requirements.txt

# Așteptă 5-10 minute pentru TensorFlow...
```

### 3️⃣ Descarcă Model AI

Opțiunile disponibile:

**Opțiunea A: Descărcare Manuală** (Recomandată)
1. Vizitează: https://storage.googleapis.com/magenta-models/melody_rnn/basic_rnn.mag
2. Salvează în: `ai-music-generator/backend/models/basic_rnn.mag`

**Opțiunea B: Script Powershell** (Automată)
```powershell
# Din folderul backend
mkdir models -Force

# Descarcă checkpoint
Invoke-WebRequest -Uri "https://storage.googleapis.com/magenta-models/melody_rnn/basic_rnn.mag" `
                  -OutFile "models/basic_rnn.mag"

echo "✓ Model descărcat!"
```

### 4️⃣ Pornește Serverele

**Terminal 1 - Backend (FastAPI)**
```powershell
cd "C:\Users\Einsteinn\Documents\Albumu meu\ai-music-generator\backend"
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

✅ Așteptă mesaj: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 - Frontend (Live Server)**
1. Deschide VS Code
2. Navigează la `frontend/index.html`
3. Click-dreapta → "Open with Live Server"
4. Se deschide automat în browser

🎉 **Gata!** Accesează: `http://localhost:5500`

---

## 🎵 Prima Generare (5 Clickuri)

1. Deschide aplicația
2. Selectează gen: **Pop**
3. Click: **🎹 Generează Muzică**
4. Așteptă 30-60 secunde
5. Ascultă rezultatul!

---

## 📋 Checklist Troubleshooting

- [ ] Python 3.14+ instalat? `python --version`
- [ ] venv activ? (Trebuie să vezi `(venv)` în prompt)
- [ ] Dependencies instalate? `pip list | grep magenta`
- [ ] Model descărcat? `Test-Path backend/models/basic_rnn.mag`
- [ ] Backend rulează? `http://127.0.0.1:8000/health` returnează green
- [ ] Frontend accesibil? Browser se deschide automat

---

## 🎓 Următorii Pași

După instalare:

1. **Explorează Genuri** - Testează toate 8 genurile
2. **Opțiuni Avansate** - Joacă cu Temperature și Steps
3. **Istoric** - Revine la generări anterioare
4. **Download** - Salvează fișierele MIDI favorite
5. **Documentație** - Citește `README.md` complet

---

## 🆘 Probleme Rapide

### `ModuleNotFoundError: No module named 'magenta'`
```powershell
.\venv\Scripts\Activate.ps1  # Activează venv
pip install -r requirements.txt --upgrade
```

### `Connection refused 127.0.0.1:8000`
```powershell
# Backend nu e pornit - Ruleaza Terminal 1 din nou
cd backend && .\venv\Scripts\Activate.ps1 && uvicorn main:app --reload
```

### `basic_rnn.mag not found`
```powershell
# Model nu e descărcat
# Ruleaza Opțiunea B din Pasul 3
Invoke-WebRequest -Uri "https://storage.googleapis.com/magenta-models/melody_rnn/basic_rnn.mag" `
                  -OutFile "backend/models/basic_rnn.mag"
```

### `Port 8000 already in use`
```powershell
# Găsește procesul
netstat -ano | findstr :8000
# Opreștelo (înlocuiește PID)
taskkill /PID 1234 /F
# Restart backend
```

---

## 📚 Resurse Suplimentare

- 📖 **Documentație Completă**: `README.md`
- 🎓 **API Docs**: `http://127.0.0.1:8000/docs` (Swagger UI)
- 🔗 **Magenta Docs**: https://magenta.tensorflow.org/
- 💬 **FastAPI Help**: https://fastapi.tiangolo.com/

---

**Instalare finalizată? 🎉 Generează prima muzică și bucură-te! 🎵**
