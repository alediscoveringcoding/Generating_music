"""
FastAPI Backend pentru AI Music Generator
Oferă endpoints REST pentru generare, descărcare și gestionare muzică
"""

import os
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, List
from pathlib import Path

from music_generator import generate_music, get_all_genres, save_to_history, get_history, MusicGenerator, GENRE_SETTINGS, OUTPUT_DIR

# Configurare logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creare aplicație FastAPI
app = FastAPI(
    title="AI Music Generator API",
    description="API pentru generare muzică cu inteligență artificială",
    version="1.0.0"
)

# CORS middleware pentru comunicarea cu frontend-ul
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

# Serve index.html pe /app
@app.get("/app", tags=["Frontend"])
async def serve_frontend():
    """Servește interfața frontend"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Frontend not found")

# Modele Pydantic pentru validare
class GenerateRequest(BaseModel):
    """Request pentru generare muzică"""
    genre: str
    temperature: Optional[float] = None
    steps: Optional[int] = None
    seed_note: Optional[int] = 60


class GenerateResponse(BaseModel):
    """Response pentru generare muzică"""
    success: bool
    message: str
    filename: Optional[str] = None
    filepath: Optional[str] = None
    metadata: Optional[Dict] = None


# Inițializare generator
generator = MusicGenerator()

# Paths
CURRENT_DIR = Path(__file__).parent
GENERATED_MUSIC_DIR = Path(OUTPUT_DIR)


@app.get("/", tags=["Info"])
async def root():
    """Rută principală - informații API"""
    return {
        "name": "AI Music Generator",
        "version": "1.0.0",
        "description": "Generează muzică cu ajutorul inteligenței artificiale",
        "endpoints": {
            "genres": "/genres",
            "generate": "/generate (POST)",
            "download": "/download/{filename}",
            "history": "/history",
            "delete": "/delete/{filename}"
        }
    }


@app.get("/genres", tags=["Info"])
async def list_genres():
    """Returnează lista tuturor genurilor disponibile"""
    try:
        genres = get_all_genres()
        return {
            "success": True,
            "count": len(genres),
            "genres": genres
        }
    except Exception as e:
        logger.error(f"Eroare preluare genuri: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/genre/{genre_name}", tags=["Info"])
async def get_genre_info(genre_name: str):
    """Returnează informații despre un anumit gen"""
    try:
        if genre_name not in GENRE_SETTINGS:
            raise HTTPException(status_code=404, detail=f"Gen necunoscut: {genre_name}")
        
        info = GENRE_SETTINGS.get(genre_name, {})
        return {
            "success": True,
            "genre_info": info
        }
    except Exception as e:
        logger.error(f"Eroare preluare info gen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate", response_model=GenerateResponse, tags=["Generation"])
async def generate_music_post(request: GenerateRequest):
    """Generează muzică pentru genul specificat"""
    try:
        # Validare gen
        if request.genre not in GENRE_SETTINGS:
            raise HTTPException(
                status_code=400,
                detail=f"Gen nedescoperit: {request.genre}. Genuri disponibile: {list(GENRE_SETTINGS.keys())}"
            )
        
        # Validare parametrii
        if request.temperature is not None:
            if not (0.0 <= request.temperature <= 2.0):
                raise HTTPException(status_code=400, detail="Temperature trebuie să fie între 0.0 și 2.0")
        
        if request.steps is not None:
            if not (100 <= request.steps <= 500):
                raise HTTPException(status_code=400, detail="Steps trebuie să fie între 100 și 500")
        
        # Generare muzică
        logger.info(f"Generând muzică pentru genul: {request.genre}")
        filename = generate_music(
            genre=request.genre,
            temperature=request.temperature or GENRE_SETTINGS[request.genre]["temperature"],
            steps=request.steps or GENRE_SETTINGS[request.genre]["steps"],
            seed_note=request.seed_note
        )
        
        save_to_history(request.genre, filename, request.temperature, request.steps)
        
        return GenerateResponse(
            success=True,
            message=f"Muzică generată cu succes pentru genul {request.genre}",
            filename=filename,
            filepath=str(Path(OUTPUT_DIR) / filename),
            metadata={"genre": request.genre, "filename": filename}
        )
        
    except ValueError as e:
        logger.error(f"Eroare validare: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Eroare generare muzică: {e}")
        raise HTTPException(status_code=500, detail=f"Eroare generare: {str(e)}")


@app.get("/generate/{genre}", tags=["Generation"])
async def generate_music_get(
    genre: str,
    temperature: Optional[float] = Query(None, ge=0.0, le=2.0),
    steps: Optional[int] = Query(None, ge=100, le=500),
    seed_note: int = Query(60, ge=0, le=127)
):
    """
    Generează muzică (GET endpoint)
    
    Parameters:
    - genre: Genul muzical (classical, pop, jazz, rock, rap, electronic, ambient, folk)
    - temperature: Creativitate (0.0-2.0), implicit din gen
    - steps: Lungimea melodiei (100-500), implicit din gen
    - seed_note: Nota inițială MIDI (0-127)
    """
    request = GenerateRequest(
        genre=genre,
        temperature=temperature,
        steps=steps,
        seed_note=seed_note
    )
    return await generate_music_post(request)


@app.get("/download/{filename}", tags=["Download"])
async def download_music(filename: str):
    """Descarcă fișierul WAV generat"""
    try:
        file_path = GENERATED_MUSIC_DIR / filename
        
        # Validare cale pentru securitate
        if not str(file_path).startswith(str(GENERATED_MUSIC_DIR)):
            raise HTTPException(status_code=403, detail="Acces interzis")
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Fișier nu găsit")
        
        return FileResponse(
            path=file_path,
            media_type="audio/wav",
            filename=filename
        )
    except Exception as e:
        logger.error(f"Eroare descărcare: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", tags=["History"])
async def get_history_endpoint(limit: int = Query(50, ge=1, le=500)):
    """Returnează istoricul generărilor recente"""
    try:
        history = get_history()[-limit:]
        return {
            "success": True,
            "count": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Eroare preluare istoric: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete/{filename}", tags=["Management"])
async def delete_music(filename: str):
    """Șterge un fișier generat"""
    try:
        # Validare cale
        file_path = GENERATED_MUSIC_DIR / filename
        if not str(file_path).startswith(str(GENERATED_MUSIC_DIR)):
            raise HTTPException(status_code=403, detail="Acces interzis")
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Fișier nu găsit")
        
        file_path.unlink()
        
        return {
            "success": True,
            "message": f"Fișier șters: {filename}"
        }
    except Exception as e:
        logger.error(f"Eroare ștergere: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", tags=["Info"])
async def get_stats():
    """Returnează statistici despre fișierele generate"""
    try:
        generated_files = list(GENERATED_MUSIC_DIR.glob("*.wav"))
        total_size = sum(f.stat().st_size for f in generated_files) / (1024 * 1024)  # MB
        history = get_history()
        
        return {
            "success": True,
            "total_files": len(generated_files),
            "total_size_mb": round(total_size, 2),
            "total_generations": len(history)
        }
    except Exception as e:
        logger.error(f"Eroare statistici: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", tags=["Info"])
async def health_check():
    """Verifică starea serverului"""
    return {
        "status": "healthy",
        "service": "AI Music Generator",
        "version": "2.0",
        "genres": len(GENRE_SETTINGS)
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
