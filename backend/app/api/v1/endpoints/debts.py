# backend/app/api/v1/endpoints/debts.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.crud.crud_debt import crud_debt
from backend.app.schemas.debt_schema import DebtCreate, DebtResponse

router = APIRouter()


@router.post("/", response_model=DebtResponse, status_code=status.HTTP_201_CREATED)
def create_debt(debt_in: DebtCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva deuda en el sistema.
    """
    return crud_debt.create(db=db, debt_in=debt_in)


@router.get("/", response_model=List[DebtResponse])
def read_debts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene el listado de todas las deudas registradas.
    """
    return crud_debt.get_all(db=db, skip=skip, limit=limit)


@router.get("/{debt_id}", response_model=DebtResponse)
def read_debt(debt_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle de una deuda específica por su ID.
    """
    db_debt = crud_debt.get_by_id(db=db, debt_id=debt_id)
    if not db_debt:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")
    return db_debt


@router.delete("/{debt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_debt(debt_id: int, db: Session = Depends(get_db)):
    """
    Elimina una deuda del sistema.
    """
    success = crud_debt.delete(db=db, debt_id=debt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")
    return None
