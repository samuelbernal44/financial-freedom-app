# backend/app/crud/crud_income.py
from sqlalchemy.orm import Session
from backend.app.models.income import IncomeModel
from backend.app.schemas.income_schema import IncomeBase


class CRUDIncome:

    @staticmethod
    def get_profile(db: Session):
        """
        Obtiene el perfil financiero actual. 
        Al ser un sistema personal, asumiremos por ahora el primer registro disponible.
        """
        return db.query(IncomeModel).first()

    @staticmethod
    def save_profile(db: Session, income_in: IncomeBase) -> IncomeModel:
        """Crea o actualiza el perfil único de ingresos y gastos."""
        db_profile = db.query(IncomeModel).first()

        if db_profile:
            # Si ya existe, actualizamos los valores
            db_profile.fixed_income = income_in.fixed_income
            db_profile.fixed_expenses = income_in.fixed_expenses
            db_profile.eventual_incomes = income_in.eventual_incomes
        else:
            # Si no existe, creamos el primer registro
            db_profile = IncomeModel(
                fixed_income=income_in.fixed_income,
                fixed_expenses=income_in.fixed_expenses,
                eventual_incomes=income_in.eventual_incomes
            )
            db.add(db_profile)

        db.commit()
        db.refresh(db_profile)
        return db_profile


crud_income = CRUDIncome()
