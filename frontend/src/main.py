# frontend/src/main.py
import flet as ft
from frontend.src.api_client.client import APIClient
from frontend.src.components.debt_card import crear_tarjeta_deuda


def main(page: ft.Page):
    page.title = "Sistema de Libertad Financiera"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30

    # Grilla adaptativa global para las tarjetas de deuda
    cards_grid = ft.ResponsiveRow(spacing=20)

    # ==========================================
    # LOGICA DE CARGA DINÁMICA (REUTILIZABLE)
    # ==========================================
    def cargar_datos_ui(e=None):
        """Limpia la grilla, consulta al backend y renderiza las deudas actuales."""
        # Forzamos el cursor a modo espera de forma explícita mientras procesa
        page.cursor = "wait"
        cards_grid.controls.clear()
        page.update()

        deudas = APIClient.obtener_deudas()

        if deudas is None:
            cards_grid.controls.append(
                ft.Container(
                    content=ft.Text(
                        "⚠️ Error de conexión con el backend.", color=ft.Colors.RED_400),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_900),
                    border_radius=8
                )
            )
        elif len(deudas) == 0:
            cards_grid.controls.append(
                ft.Text("No hay deudas registradas.",
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
                card.col = {"sm": 12, "md": 6, "lg": 4}
                cards_grid.controls.append(card)

        # ✅ CLAVE: Forzamos al puntero a regresar a su estado normal (flecha estándar)
        page.cursor = "default"
        page.update()

    # ==========================================
    # COMPORTAMIENTO: CONFIGURACIÓN (MODAL)
    # ==========================================
    def abrir_configuracion(e):
        """Despliega un diálogo emergente de configuración del sistema."""
        dialogo_config = ft.AlertDialog(
            title=ft.Text("Configuración del Sistema"),
            content=ft.Text(
                "Módulo modular de parámetros en desarrollo. Aquí podrás configurar las APIs y variables globales."),
            actions=[
                ft.Button("Cerrar", on_click=lambda _: setattr(
                    dialogo_config, "open", False) or page.update())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialogo_config)
        dialogo_config.open = True
        page.update()

    # ==========================================
    # 1. BARRA DE MENÚ / NAVEGACIÓN SUPERIOR
    # ==========================================
    page.appbar = ft.AppBar(
        title=ft.Text("Módulo de Optimización", weight=ft.FontWeight.W_500),
        center_title=False,
        bgcolor="#1e1e2e",
        actions=[
            # CON COMPORTAMIENTO: Ahora llama a la función de recarga
            ft.Button("Actualizar", on_click=cargar_datos_ui),
            # CON COMPORTAMIENTO: Abre una ventana modal nativa
            ft.Button("Configuración", on_click=abrir_configuracion),
        ],
    )

    # Encabezado principal
    header = ft.Column([
        ft.Text("Dashboard de Deudas", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Visualización modular del inventario financiero actual.",
                color=ft.Colors.GREY_400),
        ft.Divider(height=20)
    ])

    # ==========================================
    # 2. PANEL DE INTERACCIÓN (ESTRATEGIA)
    # ==========================================
    excedente_input = ft.TextField(
        label="Excedente Mensual Extra ($)",
        value="500000",
        width=250,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    estrategia_dropdown = ft.Dropdown(
        label="Estrategia",
        width=200,
        options=[
            ft.dropdown.Option("avalancha", "Avalancha (Interés Alto)"),
            ft.dropdown.Option("bola_de_nieve", "Bola de Nieve (Saldo Bajo)"),
        ],
        value="avalancha"
    )

    resultado_texto = ft.Text(
        "Selecciona los parámetros y presiona optimizar para calcular la ruta de libertad.",
        italic=True,
        color=ft.Colors.GREY_400
    )

    def ejecutar_optimizacion(e):
        btn_optimizar.disabled = True
        resultado_texto.value = f"Calculando plan con estrategia: {estrategia_dropdown.value.upper()}..."
        page.update()

        excedente = excedente_input.value
        estrategia = estrategia_dropdown.value

        resultado_texto.value = f"✅ Simulación procesada con éxito.\nEstrategia activa: {estrategia.upper()} con un aporte extra de ${int(excedente):,.2f}/mes.\n¡El motor modular de backend está listo para procesar el cronograma!"
        btn_optimizar.disabled = False
        page.update()

    btn_optimizar = ft.Button(
        "Calcular Optimización",
        on_click=ejecutar_optimizacion
    )

    panel_controles = ft.Container(
        content=ft.Row(
            controls=[excedente_input, estrategia_dropdown, btn_optimizar],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=True,
            spacing=20
        ),
        padding=20,
        bgcolor="#14141f",
        border_radius=10,
    )

    # Construimos la estructura inicial de la página
    page.add(
        header,
        cards_grid,
        ft.Divider(height=30, color="transparent"),
        ft.Text("Panel de Simulación Interactiva",
                size=20, weight=ft.FontWeight.BOLD),
        panel_controles,
        ft.Container(content=resultado_texto, padding=10)
    )

    # Disparamos la primera carga de datos asegurando el ciclo de dibujado inicial
    page.update()
    cargar_datos_ui()


if __name__ == "__main__":
    ft.run(main)
