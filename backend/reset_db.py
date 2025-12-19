# reset_db.py
import os
from database import engine
from model.models import Base

# Nombre del archivo de la base de datos
db_file = "./test.db"  # <- cambia esto si tu DB tiene otro nombre

# 1️⃣ Borrar archivo antiguo si existe
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"Archivo de base de datos '{db_file}' eliminado.")
else:
    print(f"No existe archivo de base de datos '{db_file}', se creará uno nuevo.")

# 2️⃣ Crear todas las tablas
print("Creando todas las tablas...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente.")
