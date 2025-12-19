from sqlalchemy.orm import Session
from model.models import Project, Requirement

def get_projects(db: Session):
    return db.query(Project).all()

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def create_project(db: Session, name: str, description: str, guidelines: str, requirements: list):
    project = Project(
        name=name,
        description=description,
        guidelines=guidelines,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Crear los requisitos asociados
    for req in requirements:
        new_req = Requirement(
            project_id=project.id,
            displayId=req.displayId,
            description=req.description
        )
        db.add(new_req)  # 👈 ahora está dentro del for

    db.commit()
    db.refresh(project)
    return project
