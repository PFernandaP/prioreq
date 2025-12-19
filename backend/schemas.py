from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(BaseModel):
    email: str
    password: str   # sin is_admin

class UserLogin(BaseModel):
    email: str
    password: str   # login usa esto

class UserOut(BaseModel):
    id: int
    email: str
    role: str  # "admin" o "user"

    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    name: str
    description: str
    area: str

class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        orm_mode = True
