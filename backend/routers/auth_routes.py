from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from model.models import User
from schemas import UserCreate, UserLogin

from auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    token = create_access_token(db_user)

    return {"access_token": token, "token_type": "bearer"}


# =========================
# DEBUG: ver usuarios reales en Railway
# =========================
@router.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role
        }
        for u in users
    ]


# =========================
# DEBUG: revisar un usuario específico
# =========================
@router.get("/debug/user/{email}")
def debug_user(email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        return {"exists": False}

    return {
        "exists": True,
        "id": db_user.id,
        "email": db_user.email,
        "role": db_user.role
    }
