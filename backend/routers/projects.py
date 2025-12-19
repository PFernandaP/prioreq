from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import List
from pydantic import BaseModel
from model.models import Project, Requirement, User, UserProject
from typing import Optional
from auth_dependencies import admin_required        # ⬅ IMPORTANTE
from auth import get_current_user                  # puedes usarlo si lo necesitas
from schemas import ProjectCreate,UserCreate,UserOut


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# DTOs
# ----------------------------
class RequirementDTO(BaseModel):
    id: int
    displayId: str
    description: str

    class Config:
        from_attributes = True

class RequirementCreateDTO(BaseModel):
    displayId: str
    description: str

class ProjectDTO(BaseModel):
    id: int
    name: str
    description: str
    guidelines: List[str] = []
    requirements: List[RequirementDTO] = []

    class Config:
        from_attributes = True

class ProjectCreateDTO(BaseModel):
    name: str
    description: str
    guidelines: List[str] = []
    requirements: List[RequirementCreateDTO] = []

class ProjectAreaUpdateDTO(BaseModel):
    area: str

class AssignProjectDTO(BaseModel):
    user_id: int
    project_id: int

# -----------------------------------------------------
# PATCH (solo admin): actualizar área
# -----------------------------------------------------
@router.patch("/{project_id}/area", response_model=str, dependencies=[Depends(admin_required)])
def update_project_area(project_id: int, data: ProjectAreaUpdateDTO, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.area = data.area
    db.commit()
    db.refresh(project)
    
    return project.area

# -----------------------------------------------------
# GET (todos): listar proyectos
# -----------------------------------------------------
@router.get("/", response_model=List[ProjectDTO])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    result = []

    for p in projects:
        reqs = [RequirementDTO.from_orm(r) for r in p.requirements]

        # ID local secuencial dentro de cada proyecto
        for idx, r in enumerate(reqs):
            r.id = idx + 1  

        result.append(ProjectDTO(
            id=p.id,
            name=p.name,
            description=p.description,
            guidelines=p.guidelines.split(";") if p.guidelines else [],
            requirements=reqs
        ))
    return result

# -----------------------------------------------------
# DELETE (solo admin)
# -----------------------------------------------------
@router.delete("/{project_id}", status_code=204, dependencies=[Depends(admin_required)])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return

# -----------------------------------------------------
# POST (solo admin)
# -----------------------------------------------------
@router.post("/", response_model=ProjectDTO, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_required)])
def create_project(project: ProjectCreateDTO, db: Session = Depends(get_db)):
    existing = db.query(Project).filter(Project.name == project.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project with same name already exists")

    db_project = Project(
        name=project.name,
        description=project.description,
        guidelines=";".join(project.guidelines) if project.guidelines else ""
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    created_reqs = []
    for r in project.requirements:
        db_req = Requirement(
            project_id=db_project.id,
            displayId=r.displayId,
            description=r.description
        )
        db.add(db_req)
        created_reqs.append(db_req)

    db.commit()
    for r in created_reqs:
        db.refresh(r)

    return ProjectDTO(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        guidelines=project.guidelines,
        requirements=[RequirementDTO.from_orm(r) for r in created_reqs]
    )

# ----------------------------
# Admin: listar TODOS los proyectos
# ----------------------------
@router.get("/all", response_model=List[ProjectDTO])
def list_all_projects(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Verificar permisos de admin
    admin_required(current_user)

    projects = db.query(Project).all()
    result = []
    for p in projects:
        reqs = [RequirementDTO.from_orm(r) for r in p.requirements]
        for idx, r in enumerate(reqs):
            r.id = idx + 1
        result.append(ProjectDTO(
            id=p.id,
            name=p.name,
            description=p.description,
            guidelines=p.guidelines.split(";") if p.guidelines else [],
            requirements=reqs
        ))
    return result


# ----------------------------
# Usuario: listar PROYECTOS ASIGNADOS al usuario actual
# ----------------------------

@router.get("/my-projects")
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects = [link.project for link in current_user.assigned_projects]

    return [
        {
            "id": p.id,
            "name": p.name,
            #"area": p.area,
            "description": p.description,
            "guidelines": p.guidelines.split(";") if p.guidelines else [],
            "requirements": [
                {
                    "displayId": r.displayId,
                    "description": r.description
                }
                for r in p.requirements
            ]
        }
        for p in projects
    ]


@router.post("/assign", dependencies=[Depends(admin_required)])
def assign_project(data: AssignProjectDTO, db: Session = Depends(get_db)):
    # Validar existencia del usuario y proyecto
    user = db.query(User).filter(User.id == data.user_id).first()
    project = db.query(Project).filter(Project.id == data.project_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Verificar si ya estaba asignado
    exists = db.query(UserProject).filter(
        UserProject.user_id == data.user_id,
        UserProject.project_id == data.project_id
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Project already assigned to user")

    new_link = UserProject(
        user_id=data.user_id,
        project_id=data.project_id
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return {"message": "Project assigned successfully"}

@router.get("/{project_id}", response_model=ProjectDTO)
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    reqs = [
        {
            "id": idx + 1,
            "displayId": r.displayId,
            "description": r.description
        }
        for idx, r in enumerate(project.requirements)
    ]

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "guidelines": project.guidelines.split(";") if project.guidelines else [],
        "requirements": reqs
    }
