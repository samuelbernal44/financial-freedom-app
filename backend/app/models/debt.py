# backend/app/models/debt.py
from sqlalchemy import Column, Integer, String, Float
from backend.app.core.database import Base


class DebtModel(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    pacted_months = Column(Integer, nullable=False)
    # Guardada en formato YYYY-MM-DD
    acquisition_date = Column(String, nullable=False)
