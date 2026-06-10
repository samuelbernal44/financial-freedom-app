# backend/app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial Freedom API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Aquí añadiremos más adelante las credenciales de Base de Datos

    class Config:
        env_file = ".env"  # Permite leer variables desde un archivo .env externo


settings = Settings()
