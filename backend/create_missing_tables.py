from database import engine
from model.models import Base

print("Creando tablas faltantes sin borrar las existentes...")
Base.metadata.create_all(bind=engine)
print("Proceso terminado.")


from sqlalchemy import inspect
from database import engine

inspector = inspect(engine)
tables = inspector.get_table_names()

print("Tablas encontradas:")
for t in tables:
    print("-", t)

#----------------------------

from database import SessionLocal
from model.models import (
    ExperimentResult,
    ExperimentDimensionPriority,
    ExperimentSubdimensionPriority,
    ExperimentMatrixRelation,
    ExperimentRequirementScore
)

db = SessionLocal()

try:
    # 1. Crear cabecera del resultado
    result = ExperimentResult(
        user_id=1,
        project_id=1
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    print(f"ExperimentResult creado con id={result.id}")

    # 2. Guardar prioridad de una dimensión
    dim_priority = ExperimentDimensionPriority(
        result_id=result.id,
        dimension_id=101,
        priority_order=1,
        weight=3
    )
    db.add(dim_priority)

    # 3. Guardar prioridad de una subdimensión
    sub_priority = ExperimentSubdimensionPriority(
        result_id=result.id,
        subdimension_id=1001,
        priority_label="Alta",
        priority_value=3
    )
    db.add(sub_priority)

    # 4. Guardar una relación de matriz
    matrix_relation = ExperimentMatrixRelation(
        result_id=result.id,
        requirement_id=1,
        subdimension_id=1001,
        is_related=1
    )
    db.add(matrix_relation)

    # 5. Guardar score de requisito
    req_score = ExperimentRequirementScore(
        result_id=result.id,
        requirement_id=1,
        ranking_position=1,
        score=10.5
    )
    db.add(req_score)

    db.commit()
    print("Datos de prueba insertados correctamente.")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()
 