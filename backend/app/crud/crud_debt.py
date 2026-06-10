# backend/app/crud/crud_debt.py
from sqlalchemy.orm import Session
from backend.app.models.debt import DebtModel
from backend.app.schemas.debt_schema import DebtCreate


class CRUDDebt:

    @staticmethod
    def get_by_id(db: Session, debt_id: int):
        """Busca una deuda específica por su ID."""
        return db.query(DebtModel).filter(DebtModel.id == debt_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        """Obtiene el listado de todas las deudas con soporte para paginación."""
        return db.query(DebtModel).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, debt_in: DebtCreate) -> DebtModel:
        """Crea y persiste una nueva deuda en la base de datos."""
        db_debt = DebtModel(
            name=debt_in.name,
            total_amount=debt_in.total_amount,
            interest_rate=debt_in.interest_rate,
            pacted_months=debt_in.pacted_months,
            acquisition_date=debt_in.acquisition_date
        )
        db.add(db_debt)
        db.commit()
        # Refresca el objeto para obtener el ID generado por la BD
        db.refresh(db_debt)
        return db_debt

    @staticmethod
    def update(db: Session, db_debt: DebtModel, update_data: dict) -> DebtModel:
        """Actualiza los campos de una deuda existente."""
        for field, value in update_data.items():
            if hasattr(db_debt, field):
                setattr(db_debt, field, value)
        db.commit()
        db.refresh(db_debt)
        return db_debt

    @staticmethod
    def delete(db: Session, debt_id: int) -> bool:
        """Elimina una deuda por su ID y retorna True si la operación fue exitosa."""
        db_debt = db.query(DebtModel).filter(DebtModel.id == debt_id).first()
        if db_debt:
            db.delete(db_debt)
            db.commit()
            return True
        return False


crud_debt = CRUDDebt()
