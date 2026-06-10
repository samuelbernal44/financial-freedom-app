# backend/app/models/income.py
from sqlalchemy import Column, Integer, Float, JSON
from backend.app.core.database import Base


class IncomeModel(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    fixed_income = Column(Float, nullable=False)
    fixed_expenses = Column(Float, nullable=False)

    # Almacenamos el diccionario de meses e ingresos eventuales como un objeto JSON nativo
    # Ejemplo: {"6": 1500000.0, "12": 2000000.0} (Mes 6: Prima de mitad de año, Mes 12: Aguinaldo)
    eventual_incomes = Column(JSON, nullable=True, default=dict)
