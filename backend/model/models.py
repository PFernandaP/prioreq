from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import UniqueConstraint

# -------------------------
# PROJECT
# -------------------------
class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    #area = Column(String, nullable=True)   # <<--- NUEVO
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
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

    # Relación hacia UserProject
    assigned_projects = relationship("UserProject", back_populates="user")

class UserProject(Base):
    __tablename__ = "user_projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Relaciones correctas
    user = relationship("User", back_populates="assigned_projects")
    project = relationship("Project")

class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_experiment_user_project"),
    )


class ExperimentDimensionPriority(Base):
    __tablename__ = "experiment_dimension_priorities"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("experiment_results.id"), nullable=False)
    dimension_id = Column(Integer, nullable=False)
    priority_order = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)


class ExperimentSubdimensionPriority(Base):
    __tablename__ = "experiment_subdimension_priorities"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("experiment_results.id"), nullable=False)
    subdimension_id = Column(Integer, nullable=False)
    priority_label = Column(String, nullable=False)
    priority_value = Column(Integer, nullable=False)


class ExperimentMatrixRelation(Base):
    __tablename__ = "experiment_matrix_relations"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("experiment_results.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    subdimension_id = Column(Integer, nullable=False)
    is_related = Column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint(
            "result_id",
            "requirement_id",
            "subdimension_id",
            name="uq_result_requirement_subdimension"
        ),
    )


class ExperimentRequirementScore(Base):
    __tablename__ = "experiment_requirement_scores"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("experiment_results.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    ranking_position = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "result_id",
            "requirement_id",
            name="uq_result_requirement_score"
        ),
    )
