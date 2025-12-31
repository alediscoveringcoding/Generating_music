# INSTALLATION_GUIDE.md

# 🎵 AI Music Generator - Ghid Instalare Complet

## 📋 Cerințe Minime

- **Windows 10+** / **macOS 10.14+** / **Linux (Ubuntu 18+)**
- **Python 3.9** sau mai nou
- **4 GB RAM** (8 GB recomandat)
- **2 GB spațiu disk** (pentru modele)
- **Internet** (pentru descărcări inițiale)

## 🔧 Instalare Pas cu Pas

### Pasul 1: Verifică Python

```bash
# Windows PowerShell
python --version

# macOS/Linux
python3 --version
```

✅ Trebuie să fie **Python 3.9+**

### Pasul 2: Pregătire Proiect

```bash
# 1. Navighează la folder proiect
cd "C:\Users\Einsteinn\Documents\Albumu meu\ai-music-generator"

# 2. Verifică structură
dir
# Output asteptat:
# backend/
# frontend/
# README.md
# config.json
# START.bat (Windows) sau start.sh (Unix)
```

### Pasul 3: Setup Mediu Virtual

**Windows PowerShell:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1

# Dacă primești error: "cannot be loaded because running scripts is disabled"
# Rulează PowerShell as Administrator și executa:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

✅ Trebuie să vezi `(venv)` în prompt

### Pasul 4: Instalează Dependențe

```bash
# Asigură-te că venv e activ
pip install --upgrade pip
pip install -r requirements.txt

# Așteptă 5-10 minute (TensorFlow + Magenta sunt mari!)
# Output asteptat la final:
# Successfully installed tensorflow-2.15.0 magenta-2.1.2 ...
```

### Pasul 5: Descarcă Modelul Magenta

**Opțiunea A: Manual (Recomandat)**

1. Deschide link: https://storage.googleapis.com/magenta-models/melody_rnn/basic_rnn.mag
2. Fișierul se descarcă automat (`basic_rnn.mag`)
3. Salvează în: `ai-music-generator\backend\models\basic_rnn.mag`

**Opțiunea B: PowerShell Script**

```powershell
# Din folderul backend cu venv activ
mkdir models -Force

# Descarcă model
Invoke-WebRequest -Uri "https://storage.googleapis.com/magenta-models/melody_rnn/basic_rnn.mag" `
                  -OutFile "models\basic_rnn.mag" `
                  -UseBasicParsing

echo "✓ Model descărcat!"
```

**Opțiunea C: wget/curl (Linux/macOS)**

```bash
# Din folderul backend
mkdir -p models
wget https://storage.googleapis.com/magenta-models/melody_rnn/basic_rnn.mag -O models/basic_rnn.mag
# sau
curl -o models/basic_rnn.mag https://storage.googleapis.com/magenta-models/melody_rnn/basic_rnn.mag
```

### Pasul 6: Pornire Backend

```powershell
# Asigură-te că ești în backend/ cu venv activ
cd backend
.\venv\Scripts\Activate.ps1

# Pornire server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

✅ Așteptă mesaj:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Pasul 7: Pornire Frontend

**Opțiunea A: Live Server (Recomandată)**

1. Instalează extensia "Live Server" în VS Code
2. Deschide folderul `ai-music-generator` în VS Code
3. Navighează la `frontend/index.html`
4. Click-dreapta → "Open with Live Server"
5. Se deschide automat în browser

**Opțiunea B: Python HTTP Server**

```powershell
# În alt terminal (din frontend/)
cd frontend
python -m http.server 8080

# Accesează: http://localhost:8080
```

**Opțiunea C: npm http-server (dacă ai Node.js)**

```bash
# Instalează (o singură dată)
npm install -g http-server

# Pornire (din frontend/)
http-server -p 8080
```

### 🎉 Gata! Aplicația rulează

- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:5500 (sau 8080)
- **API Docs**: http://127.0.0.1:8000/docs (Swagger UI)

---

## ⚡ Quick Start cu Batch Script

### Windows (Easiest)

```bash
# Din root folder ai-music-generator
START.bat
```

Scriptul va:
1. ✅ Verifica Python
2. ✅ Crea venv dacă nu există
3. ✅ Instala dependențe
4. ✅ Porni backend automat
5. ✅ Deschide browser

### macOS/Linux

```bash
chmod +x start.sh
./start.sh
```

---

## 🧪 Test Instalare

### Verifică Backend

```bash
# Deschide browser sau PowerShell
curl http://127.0.0.1:8000/health

# Output asteptat:
# {"status":"healthy","service":"AI Music Generator","initialized":true}
```

### Verifică genurile

```bash
curl http://127.0.0.1:8000/genres

# Output: Lista cu 8 genuri muzicale
```

### Prima Generare

1. Deschide frontend în browser
2. Selectează "Pop" din dropdown
3. Click "🎹 Generează Muzică"
4. Așteptă 30-60 secunde
5. Ascultă muzica generată!

---

## 🆘 Troubleshooting

### Error: "Python not found"

```bash
# Descarcă Python de la: https://www.python.org/downloads/
# IMPORTANT: Bifează "Add Python to PATH" la instalare
# Restart terminal după instalare
python --version
```

### Error: "Permission denied" (macOS/Linux)

```bash
# Dă permisiuni
chmod +x start.sh
chmod -R 755 backend/
```

### Error: "Module not found"

```bash
# Asigură-te că venv e activ
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Reinstalează dependențe
pip install -r requirements.txt --upgrade
```

### Error: "Port 8000 in use"

```powershell
# Găsește procesul
netstat -ano | findstr :8000

# Kill-o (înlocuiește PID)
taskkill /PID 1234 /F

# Restart backend
```

### Error: "basic_rnn.mag not found"

Modelul nu e descărcat. Revino la **Pasul 5** și descarcă-l manual.

### Backend slow pe prima pornire

Normal - TensorFlow și Magenta inițializează la prima utilizare (30-60 sec)

---

## 🎓 Pași Următori După Instalare

1. **Citește README.md** - Documentație completă
2. **Testează genuri** - Generează muzică în 8 stiluri
3. **Joacă cu parametrii** - Temperature, Steps, Seed Note
4. **Descarcă MIDI** - Salvează compoziții favorite
5. **Explorează API** - Swagger UI la /docs

---

## 📚 Resurse Suplimentare

- **Documentație**: [README.md](README.md)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **API Reference**: http://127.0.0.1:8000/docs
- **Magenta Docs**: https://magenta.tensorflow.org/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

## ✅ Checklist Final

- [ ] Python 3.9+ instalat
- [ ] Proiect descărcat/clonat
- [ ] Virtual environment creat
- [ ] Dependențe instalate (pip install -r requirements.txt)
- [ ] Model basic_rnn.mag descărcat
- [ ] Backend pornit (http://127.0.0.1:8000)
- [ ] Frontend accesibil (browser)
- [ ] API /health endpoint verde
- [ ] Primul test generare reușit
- [ ] Putem descărca fișiere MIDI

---

**Instalare Completă? 🎉 Distrează-te generând muzică! 🎵**
