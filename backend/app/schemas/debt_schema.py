# backend/app/schemas/debt_schema.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# Esquema Base: Define los campos comunes que comparten la creación y la lectura


class DebtBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Nombre de la entidad o deuda")
    total_amount: float = Field(..., gt=0,
                                description="Monto total original o saldo actual de la deuda")
    interest_rate: float = Field(..., ge=0,
                                 description="Tasa de interés Efectiva Anual (EA) en porcentaje")
    pacted_months: int = Field(..., gt=0,
                               description="Número de cuotas o meses pactados para el pago")
    acquisition_date: str = Field(
        ..., description="Fecha de adquisición de la deuda en formato AAAA-MM-DD")

    # Validador personalizado para asegurar que la fecha tenga el formato correcto
    @field_validator('acquisition_date')
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError(
                "La fecha debe tener el formato estricto YYYY-MM-DD")

# Esquema para cuando el cliente CREA una nueva deuda (Entrada)


class DebtCreate(DebtBase):
    pass  # Hereda todo lo de DebtBase sin modificaciones

# Esquema para cuando la API RESPONDE con la información de la deuda (Salida)


class DebtResponse(DebtBase):
    id: int = Field(...,
                    description="Identificador único de la deuda en la base de datos")

    class Config:
        # Permite que Pydantic lea modelos de bases de datos ORM (como SQLAlchemy) directamente
        from_attributes = True
