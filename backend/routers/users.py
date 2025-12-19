# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import List
from pydantic import BaseModel
from model.models import User, Project, UserProject
from auth import get_current_user, admin_required, hash_password, verify_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# DTOs
# =========================
class UserCreateDTO(BaseModel):
    email: str
    password: str

class UserDTO(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        orm_mode = True

class LoginDTO(BaseModel):
    email: str
    password: str

class AssignRandomDTO(BaseModel):
    count: int = 3

class AssignProjectsDTO(BaseModel):
    project_ids: List[int]

# =========================
# Crear usuario
# =========================
@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateDTO, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed, role="user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# =========================
# Login
# =========================
@router.post("/login")
def login(data: LoginDTO, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == data.email).first()
    if not db_user or not verify_password(data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user_id": db_user.id, "email": db_user.email, "role": db_user.role}

# =========================
# Asignar `count` random projects
# =========================
@router.post("/{user_id}/assign_random", status_code=200)
def assign_random_projects(user_id: int, body: AssignRandomDTO, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    all_projects = [p.id for p in db.query(Project).all()]
    if not all_projects:
        raise HTTPException(status_code=400, detail="No projects available to assign")

    assigned = {up.project_id for up in db.query(UserProject).filter(UserProject.user_id == user_id).all()}
    candidates = [pid for pid in all_projects if pid not in assigned]

    import random
    take = min(body.count, len(candidates))
    chosen = random.sample(candidates, take) if take > 0 else []

    created = []
    for pid in chosen:
        up = UserProject(user_id=user_id, project_id=pid)
        db.add(up)
        created.append(pid)

    db.commit()
    return {"assigned_project_ids": created}

# =========================
# Listar proyectos asignados a un usuario
# =========================
@router.get("/{user_id}/projects")
def get_user_projects(user_id: int, db: Session = Depends(get_db)):
    ups = db.query(UserProject).filter(UserProject.user_id == user_id).all()
    project_ids = [up.project_id for up in ups]
    projects = db.query(Project).filter(Project.id.in_(project_ids)).all()
    result = []
    for p in projects:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "guidelines": p.guidelines.split(";") if p.guidelines else [],
            "requirements_count": len(p.requirements) if hasattr(p, "requirements") else 0
        })
    return result

# =========================
# Listar todos los usuarios (solo admin)
# =========================
@router.get("/")
def get_all_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    admin_required(current_user)
    return db.query(User).all()

# =========================
# Asignar proyectos específicos a un usuario (manual)
# =========================
@router.post("/{user_id}/assign", status_code=200)
def assign_specific_projects(
    user_id: int,
    body: AssignProjectsDTO,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    admin_required(current_user)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(UserProject).filter(UserProject.user_id == user_id).delete()

    for pid in body.project_ids:
        exists = db.query(Project).filter(Project.id == pid).first()
        if not exists:
            raise HTTPException(status_code=400, detail=f"Project {pid} not found")
        db.add(UserProject(user_id=user_id, project_id=pid))

    db.commit()
    return {"assigned": body.project_ids}
