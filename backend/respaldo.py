from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

# -------------------------
# PROJECT
# -------------------------
class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    area = Column(String, nullable=True)   # <<--- NUEVO
    description = Column(String)
    guidelines = Column(String)

    requirements = relationship("Requirement", back_populates="project")
    dimensions = relationship("ProjectDimension", back_populates="project", cascade="all, delete")


# -------------------------
# DIMENSIONES DEL PROYECTO
# -------------------------
class ProjectDimension(Base):
    __tablename__ = "project_dimensions"
    __table_args__ = {"extend_existing": True}  # <- agregado

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    dimension_id = Column(Integer, nullable=False)  # ID estático del JSON
    order = Column(Integer, nullable=False)         # orden jerárquico (4,3,2,1)

    project = relationship("Project", back_populates="dimensions")
    subdimensions = relationship("ProjectSubdimension", back_populates="dimension", cascade="all, delete")

# -------------------------
# SUBDIMENSIONES ASIGNADAS
# -------------------------
class ProjectSubdimension(Base):
    __tablename__ = "project_subdimensions"
    __table_args__ = {"extend_existing": True}  # <- agregado

    id = Column(Integer, primary_key=True, index=True)
    project_dimension_id = Column(Integer, ForeignKey("project_dimensions.id"), nullable=False)

    subdimension_id = Column(Integer, nullable=False)  # ID estático del JSON
    value = Column(String, nullable=False)             # Alto / Medio / Bajo

    dimension = relationship("ProjectDimension", back_populates="subdimensions")

# -------------------------
# REQUISITOS DEL PROYECTO
# -------------------------
class Requirement(Base):
    __tablename__ = "requirements"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    displayId = Column(String)
    description = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="requirements")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)      # <<--- obligatorio
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")   # "admin" o "user"


class UserProject(Base):
    __tablename__ = "user_projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)        # Usuario participante
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
