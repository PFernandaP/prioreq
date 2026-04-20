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

from typing import List


class MatrixRelationIn(BaseModel):
    requirement_id: int
    subdimension_id: int
    is_related: int = 1


class DimensionPriorityIn(BaseModel):
    dimension_id: int
    priority_order: int
    weight: int


class SubdimensionPriorityIn(BaseModel):
    subdimension_id: int
    priority_label: str
    priority_value: int


class RequirementScoreIn(BaseModel):
    requirement_id: int
    ranking_position: int
    score: float


class ExperimentResultCreate(BaseModel):
    user_id: int
    project_id: int
    matrix_relations: List[MatrixRelationIn]
    dimension_priorities: List[DimensionPriorityIn]
    subdimension_priorities: List[SubdimensionPriorityIn]
    requirement_scores: List[RequirementScoreIn]
