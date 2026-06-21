# frontend/src/main.py
import flet as ft
from frontend.src.api_client.client import APIClient
# IMPORTAMOS LA NUEVA FUNCIÓN
from frontend.src.components.debt_card import crear_tarjeta_deuda


def main(page: ft.Page):
    page.title = "Sistema de Libertad Financiera"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30

    header = ft.Column([
        ft.Text("Dashboard de Deudas", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Visualización modular del inventario financiero actual.",
                color=ft.Colors.GREY_400),
        ft.Divider(height=20)
    ])

    cards_grid = ft.ResponsiveRow(spacing=20)

    deudas = APIClient.obtener_deudas()

    if deudas is None:
        cards_grid.controls.append(
            ft.Container(
                content=ft.Text(
                    "⚠️ Error: No se pudo conectar con el servidor Backend.", color=ft.Colors.RED_400),
                padding=20,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_900),
                border_radius=8
            )
        )
    elif len(deudas) == 0:
        cards_grid.controls.append(
            ft.Text("No hay deudas registradas aún.",
                    italic=True, color=ft.Colors.GREY_500)
        )
    else:
        for d in deudas:
            card = crear_tarjeta_deuda(
                name=str(d["name"]),
                total_amount=float(d["total_amount"]),
                interest_rate=float(d["interest_rate"]),
                pacted_months=int(d["pacted_months"])
            )
            # Aplicamos la columna directamente a la tarjeta nativa
            card.col = {"sm": 12, "md": 6, "lg": 4}
            cards_grid.controls.append(card)

    page.add(header, cards_grid)
    page.update()


if __name__ == "__main__":
    ft.run(main)
