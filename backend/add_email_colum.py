from sqlalchemy.orm import Session
from database import engine
from model.models import Project  # asegúrate de importar tu modelo Project

session = Session(bind=engine)

projects = session.query(Project).all()

if not projects:
    print("No hay proyectos en la base de datos 'projects'.")
else:
    for p in projects:
        print(f"ID: {p.id}, Name: {p.name}")  # imprime solo lo esencial
