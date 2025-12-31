#!/bin/bash
# AI Music Generator - Start Script pentru macOS/Linux

echo ""
echo "========================================"
echo "  🎵 AI Music Generator - Startup"
echo "========================================"
echo ""

# Verifica daca sunt in directorul corect
if [ ! -d "backend" ]; then
    echo "❌ Error: Executa din root dir ai-music-generator"
    exit 1
fi

echo "✓ Directoare verificate"
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nu gasit. Instaleaza Python 3.14+"
    exit 1
fi
echo "✓ Python3 gasit"

# Verifica venv
if [ ! -d "backend/venv" ]; then
    echo "📦 Creez mediu virtual..."
    cd backend
    python3 -m venv venv
    cd ..
fi
echo "✓ Virtual environment exista"

echo ""
echo "========================================"
echo "  Pornire Backend (FastAPI)..."
echo "========================================"
echo ""

# Activare venv si pornire backend
cd backend
source venv/bin/activate
pip install -q -r requirements.txt 2>/dev/null

echo "✓ Backend pornit pe http://127.0.0.1:8000"
echo ""
echo "========================================"
echo "  ✨ Setup complet!"
echo "========================================"
echo ""
echo "📖 Docs: Citeste README.md pentru detalii"
echo "🎹 Frontend: Deschide frontend/index.html cu Live Server"
echo "🛑 Stop: Ctrl+C pentru a opri backend-ul"
echo ""

# Pornire FastAPI server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
