import json
from sqlalchemy.orm import Session
from database import SessionLocal
import crud

db: Session = SessionLocal()

with open("projects.json", "r", encoding="utf-8") as f:
    projects_data = json.load(f)

for p in projects_data:
    # Revisar si el proyecto ya existe por nombre
    existing = crud.get_project_by_name(db, p["name"])
    if existing:
        print(f"Proyecto '{p['name']}' ya existe, se omite.")
        continue

    # Convertir requisitos del JSON a formato esperado por CRUD
    reqs = [{"displayId": r["id"], "description": r["text"]} for r in p.get("requirements", [])]

    # Crear proyecto
    project = crud.create_project(
        db,
        p["name"],
        p.get("description", ""),
        ";".join(p.get("guidelines", [])),
        reqs,
        area=p.get("area")  # 🔹 agregar campo area si tu modelo lo soporta
    )
    print(f"Proyecto '{p['name']}' insertado con ID {project.id}.")

db.close()
print("Todos los proyectos del JSON han sido procesados.")
