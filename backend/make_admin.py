from database import SessionLocal
from model.models import User

db = SessionLocal()

# Cambia el ID del usuario que creaste (normalmente el 1)
user = db.query(User).filter(User.id == 1).first()

if not user:
    print("No existe el usuario con ID 1")
else:
    user.role = "admin"
    db.commit()
    print("Usuario convertido a admin correctamente")
