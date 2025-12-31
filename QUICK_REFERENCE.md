# 🎵 QUICK REFERENCE CARD

## 🚀 START IN 60 SECONDS

```powershell
cd "C:\Users\Einsteinn\Documents\Albumu meu\ai-music-generator"
.\START.bat
# ✓ Done! Browser opens automatically
```

---

## 📍 IMPORTANT PATHS

```
C:\Users\Einsteinn\Documents\Albumu meu\ai-music-generator\
├─ backend/main.py              ← FastAPI server
├─ frontend/index.html          ← Web interface
├─ backend/models/basic_rnn.mag ← ⬇️ DOWNLOAD THIS (500MB)
└─ backend/generated_music/     ← MIDI files saved here
```

---

## 🔌 ENDPOINTS (When running)

| Endpoint | URL |
|----------|-----|
| Frontend | http://localhost:5500 |
| Backend | http://127.0.0.1:8000 |
| API Docs | http://127.0.0.1:8000/docs |
| Health | http://127.0.0.1:8000/health |

---

## 📖 DOCUMENTATION GUIDE

| Read This | For | Time |
|-----------|-----|------|
| 00_START_HERE.txt | Overview | 5 min |
| GETTING_STARTED.md | Start here | 5 min |
| QUICK_START.md | Setup | 15 min |
| README.md | Everything | 45 min |

---

## 🎯 3-STEP GENERATION

1. **Select Genre** → Dropdown menu
2. **Generate** → Click button (or press Space)
3. **Listen** → Player auto-plays

---

## ⌨️ KEYBOARD SHORTCUTS

| Key | Action |
|-----|--------|
| Space | Generate music |
| Ctrl+Shift+H | Reload history |
| F12 | Developer tools |

---

## 🆘 QUICK FIXES

| Problem | Solution |
|---------|----------|
| "Python not found" | Install from python.org |
| "Port 8000 in use" | Kill process: `taskkill /PID 1234 /F` |
| "Module not found" | Activate venv: `.\venv\Scripts\Activate.ps1` |
| "Model not found" | Download basic_rnn.mag to backend/models/ |
| "Connection refused" | Start backend: `uvicorn main:app --reload` |

---

## 📊 GENRES AT A GLANCE

Classical, Pop, Jazz, Rock, Rap, Electronic, Ambient, Folk

---

## 🔧 MANUAL START (If START.bat doesn't work)

```powershell
# Terminal 1: Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Frontend
# Open frontend/index.html with Live Server (VS Code)
```

---

## 📋 FILE CHECKLIST

- [ ] Project folder exists
- [ ] Python 3.14+ installed
- [ ] START.bat available
- [ ] backend/main.py exists
- [ ] frontend/index.html exists
- [ ] requirements.txt exists
- [ ] Models folder exists (download model here)
- [ ] Documentation files exist

---

## 🎓 LEARNING PATH

1. Run START.bat → 1 minute
2. Generate Pop song → 2 minutes
3. Read QUICK_START.md → 15 minutes
4. Explore all genres → 15 minutes
5. Read README.md → 45 minutes
6. Customize code → ongoing

**Total Time to Master**: ~80 minutes

---

## 💻 API QUICK TEST

```bash
# Check if backend is running
curl http://127.0.0.1:8000/health

# Get all genres
curl http://127.0.0.1:8000/genres

# Generate music (Pop genre)
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"genre":"pop","temperature":1.0,"steps":256,"seed_note":60}'
```

---

## 🎵 GENRES QUICK REFERENCE

| Genre | Vibe | Best For |
|-------|------|----------|
| Classical | Formal | Relaxation |
| Pop | Catchy | Energetic |
| Jazz | Improvisational | Sophisticated |
| Rock | Powerful | Intense |
| Rap | Rhythmic | Uptempo |
| Electronic | Synthetic | Modern |
| Ambient | Soothing | Background |
| Folk | Traditional | Acoustic |

---

## 📱 RESPONSIVE DESIGN

✅ Works on:
- Desktop (1920x1080+)
- Tablet (768-1024px)
- Mobile (320px+)

---

## 🔐 SECURITY NOTES

✅ Implemented:
- Input validation
- CORS protection
- Path traversal prevention
- Genre whitelist
- Error handling

---

## 🚀 DEPLOYMENT READY

- ✅ Production code
- ✅ Error handling
- ✅ Logging
- ✅ Comments
- ✅ Type hints
- ✅ Documentation

---

## 📊 PERFORMANCE TIPS

- First generation: 30-60 sec (normal)
- Clear venv & reinstall if slow
- Use Chrome/Edge for best experience
- Close other applications for faster generation

---

## 📞 SUPPORT HIERARCHY

1. **Check docs** (8 files)
2. **Search error** (Google)
3. **Check console** (F12)
4. **Read troubleshooting** (INSTALLATION_GUIDE.md)
5. **Verify setup** (QUICK_START.md)

---

## 🎉 SUCCESS = 

✅ Backend running  
✅ Frontend accessible  
✅ Can generate music  
✅ Can download MIDI  
✅ Can view history

---

**Location**: C:\Users\Einsteinn\Documents\Albumu meu\ai-music-generator  
**Version**: 1.0.0  
**Status**: ✅ Ready  
**Last Updated**: December 30, 2025

**👉 START WITH**: 00_START_HERE.txt or GETTING_STARTED.md
