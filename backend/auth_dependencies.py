# backend/auth_dependencies.py
from fastapi import Depends, HTTPException, status
from auth import get_current_user

def admin_required(current_user = Depends(get_current_user)):
    # get_current_user ya devuelve el objeto User desde la DB
    role = getattr(current_user, "role", None)
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return current_user
