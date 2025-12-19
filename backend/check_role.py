from database import SessionLocal
from model.models import User

db = SessionLocal()

email = "fpizarroseverino424@gmail.com"   # <-- tu correo
email = "fernanditalinda40@gmail.com"

user = db.query(User).filter(User.email == email).first()

if user:
    print("ID:", user.id)
    print("Email:", user.email)
    print("Role:", user.role)
else:
    print("Usuario no encontrado")
