from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import projects, users, auth_routes
from database import engine
from model.models import Base
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

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
# ROUTERS
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
