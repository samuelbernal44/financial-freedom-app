# backend/app/api/v1/endpoints/incomes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.crud.crud_income import crud_income
from backend.app.schemas.income_schema import IncomeBase, IncomeResponse

router = APIRouter()


@router.post("/", response_model=IncomeResponse)
def save_financial_profile(income_in: IncomeBase, db: Session = Depends(get_db)):
    """
    Crea o actualiza el perfil financiero de ingresos y gastos fijos/eventuales.
    """
    db_profile = crud_income.save_profile(db=db, income_in=income_in)

    # Calculamos dinámicamente el excedente neto para la respuesta
    net_surplus = db_profile.fixed_income - db_profile.fixed_expenses

    return IncomeResponse(
        id=db_profile.id,
        fixed_income=db_profile.fixed_income,
        fixed_expenses=db_profile.fixed_expenses,
        eventual_incomes=db_profile.eventual_incomes,
        net_surplus_base=net_surplus
    )


@router.get("/", response_model=IncomeResponse)
def read_financial_profile(db: Session = Depends(get_db)):
    """
    Obtiene el perfil financiero único del usuario.
    """
    db_profile = crud_income.get_profile(db=db)
    if not db_profile:
        raise HTTPException(
            status_code=404, detail="Perfil financiero no configurado aún")

    net_surplus = db_profile.fixed_income - db_profile.fixed_expenses
    return IncomeResponse(
        id=db_profile.id,
        fixed_income=db_profile.fixed_income,
        fixed_expenses=db_profile.fixed_expenses,
        eventual_incomes=db_profile.eventual_incomes,
        net_surplus_base=net_surplus
    )
