# backend/app/schemas/income_schema.py
from pydantic import BaseModel, Field, field_validator
from typing import Dict


class IncomeBase(BaseModel):
    fixed_income: float = Field(..., ge=0,
                                description="Ingreso mensual fijo neto del usuario")
    fixed_expenses: float = Field(..., ge=0,
                                  description="Gastos mensuales fijos obligatorios")
    # Llave: número del mes (int), Valor: monto extra recibido (float)
    eventual_incomes: Dict[int, float] = Field(
        default_factory=dict,
        description="Diccionario de ingresos eventuales mapeados por el número de mes"
    )

    @field_validator('fixed_expenses')
    @classmethod
    def validate_expenses(cls, value: float, info) -> float:
        # Podemos agregar validaciones cruzadas si fuera necesario más adelante
        return value


class IncomeResponse(IncomeBase):
    id: int
    net_surplus_base: float = Field(
        ..., description="Excedente base calculado (Ingresos - Gastos)")

    class Config:
        from_attributes = True
