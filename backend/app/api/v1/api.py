# backend/app/api/v1/api.py
from fastapi import APIRouter
from backend.app.api.v1.endpoints import debts, incomes, simulation

api_router = APIRouter()

# Acoplamos los submódulos asignándoles un prefijo URL y etiquetas para la documentación
api_router.include_router(debts.router, prefix="/debts", tags=["Deudas"])
api_router.include_router(
    incomes.router, prefix="/incomes", tags=["Ingresos y Gastos"])
api_router.include_router(simulation.router, prefix="/simulation",
                          tags=["Simulador de Libertad Financiera"])
