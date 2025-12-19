from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routers import projects, users, auth_routes
from database import engine
from model.models import Base
import json
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "dist" / "browser"

app = FastAPI()

# ======================
# BASE DE DATOS
# ======================
Base.metadata.create_all(bind=engine)

# ======================
# CORS
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# ======================
# ROUTERS DE API
# ======================
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth_routes.router)

# ======================
# JSON ENDPOINTS
# ======================
@app.get("/dimensions/json")
def get_dimensions_json():
    with open(BASE_DIR / "dimsub.json", "r", encoding="utf-8") as f:
        return json.load(f).get("dimensions", [])

@app.get("/subdimensions/json")
def get_subdimensions_json():
    with open(BASE_DIR / "dimsub.json", "r", encoding="utf-8") as f:
        return json.load(f).get("subdimensions", [])

# ======================
# FRONTEND ANGULAR
# ======================
# Monta todo el frontend, sirve index.html automáticamente como SPA fallback
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# SPA fallback: solo si no existe el archivo solicitado
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = FRONTEND_DIR / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(FRONTEND_DIR / "index.html")
