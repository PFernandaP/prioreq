from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///test.db")
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS users"))
    conn.execute(text("DROP TABLE IF EXISTS user_projects"))
    conn.commit()  # <- esto asegura que se guarde el cambio
