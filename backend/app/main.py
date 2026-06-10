# backend/app/main.py
from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.api.v1.api import api_router

# Creamos las tablas de la base de datos SQLite al arrancar la app
# En entornos de producción avanzados se usarían migraciones con Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Incluimos el enrutador de la versión 1 de la API
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a la API de Libertad Financiera. Dirígete a /docs para ver la documentación interactiva."}
