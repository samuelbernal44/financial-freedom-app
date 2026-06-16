# backend/app/schemas/simulation_schema.py
from pydantic import BaseModel, Field
from typing import List, Dict


class DebtStatus(BaseModel):
    nombre: str
    saldo_restante: float


class MonthlyProgress(BaseModel):
    mes: int
    interes_total_mes: float
    excedente_aplicado: float
    estado_deudas: List[DebtStatus]


class SimulationResponse(BaseModel):
    estrategia_aplicada: str
    meses_hasta_libertad: int
    total_intereses_pagados: float
    cronograma_mes_a_mes: List[MonthlyProgress]
