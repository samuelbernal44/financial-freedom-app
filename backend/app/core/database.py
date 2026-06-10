# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Ruta de la base de datos local (se creará un archivo llamado sql_app.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# El argumento 'check_same_thread' solo es necesario para SQLite
engine = create_engine(
    # Para cambiar a PostgreSQL en el futuro, solo se cambia esta URL desde config.py
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cada instancia de la clase SessionLocal será una sesión de base de datos activa
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la cual heredarán todos nuestros modelos ORM
Base = declarative_base()

# Dependencia para obtener la sesión de BD en los endpoints (la usaremos en la capa API)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
