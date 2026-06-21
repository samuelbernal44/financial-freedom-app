# frontend/src/components/debt_card.py
import flet as ft


def crear_tarjeta_deuda(name: str, total_amount: float, interest_rate: float, pacted_months: int) -> ft.Card:
    """
    Usa ft.Card nativo con textos puros para evitar errores de íconos y 
    bugs de renderizado en Windows.
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.ListTile(
                        title=ft.Text(
                            name, weight=ft.FontWeight.BOLD, size=18),
                        subtitle=ft.Text(
                            f"Saldo: ${total_amount:,.2f}", size=16),
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(f"  Tasa: {interest_rate}% EA", size=13),
                            ft.Text(
                                f"Plazo: {pacted_months} meses  ", size=13),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
                spacing=10,
                tight=True
            ),
            padding=15
        )
    )
