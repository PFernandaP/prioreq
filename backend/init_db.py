# init_db.py
from database import engine
from model.models import Base

print("Creando todas las tablas...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente.")
