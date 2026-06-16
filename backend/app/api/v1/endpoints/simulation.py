# backend/app/api/v1/endpoints/simulation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.crud.crud_debt import crud_debt
from backend.app.crud.crud_income import crud_income
from backend.app.services.debt_optimizer import DebtOptimizerService
from backend.app.schemas.simulation_schema import SimulationResponse

router = APIRouter()


@router.get("/", response_model=SimulationResponse)
def run_financial_simulation(estrategia: str = "avalancha", db: Session = Depends(get_db)):
    """
    Ejecuta el motor de optimización financiera. Lee las deudas e ingresos actuales de la base de datos
    y simula la estrategia elegida ('avalancha' o 'bola_de_nieve') para proyectar la liquidación a cero.
    """
    # 1. Obtener deudas de la base de datos
    db_debts = crud_debt.get_all(db=db)
    if not db_debts:
        raise HTTPException(
            status_code=400, detail="No tienes deudas registradas para simular.")

    # 2. Obtener perfil de ingresos/gastos
    db_profile = crud_income.get_profile(db=db)
    if not db_profile:
        raise HTTPException(
            status_code=400, detail="Primero debes configurar tu perfil de ingresos y gastos.")

    # 3. Mapear los modelos de la base de datos a diccionarios simples para el optimizador
    lista_deudas = [
        {
            "name": d.name,
            "total_amount": d.total_amount,
            "interest_rate": d.interest_rate,
            "pacted_months": d.pacted_months
        } for d in db_debts
    ]

    # 4. Asegurarnos de mapear correctamente las llaves del JSON de ingresos eventuales a enteros
    eventual_incomes_mapped = {int(k): float(
        v) for k, v in db_profile.eventual_incomes.items()} if db_profile.eventual_incomes else {}

    # 5. Correr el algoritmo de optimización
    resultado = DebtOptimizerService.simular_liquidacion_total(
        lista_deudas=lista_deudas,
        ingreso_fijo=db_profile.fixed_income,
        gasto_fijo=db_profile.fixed_expenses,
        ingresos_eventuales=eventual_incomes_mapped,
        estrategia=estrategia
    )

    return resultado
