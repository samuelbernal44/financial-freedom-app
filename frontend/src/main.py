# frontend/src/main.py
import flet as ft
from frontend.src.api_client.client import APIClient
from frontend.src.components.debt_card import crear_tarjeta_deuda


def main(page: ft.Page):
    page.title = "Sistema de Libertad Financiera"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30

    # Inicialización del SnackBar Global en el árbol de la página
    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor=ft.Colors.GREEN_700,
        duration=3000
    )

    # Grilla adaptativa global para las tarjetas de deuda
    cards_grid = ft.ResponsiveRow(spacing=20)

   # ==========================================
    # LOGICA DE CARGA DINÁMICA (REPARADA)
    # ==========================================
    def cargar_datos_ui(e=None):
        """Limpia la grilla, consulta al backend y renderiza las deudas actuales."""
        page.cursor = "wait"
        cards_grid.controls.clear()
        page.update()

        try:
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
        except Exception as err:
            print(f"Error inesperado al renderizar UI de deudas: {err}")
        finally:
            # FORCE: Garantiza que el cursor regrese a la flecha normal pase lo que pase
            page.cursor = "default"
            page.update()

    # ==========================================
    # COMPORTAMIENTO: CONFIGURACIÓN (MODAL ALINEADO CON EL BACKEND)
    # ==========================================
    def abrir_configuracion(e):
        """Despliega el panel de configuración avanzado conectado a las variables del backend."""

        # --- 1. SECCIÓN: Estructura de Caja Fija ---
        ingresos_fijos_input = ft.TextField(
            label="Ingresos Fijos Mensuales ($)",
            value="4500000",
            width=230,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        gastos_fijos_input = ft.TextField(
            label="Gastos Fijos Mensuales ($)",
            value="3000000",
            width=230,
            keyboard_type=ft.KeyboardType.NUMBER
        )

        bloque_flujo_caja = ft.Column([
            ft.Text("1. Capacidad Base Constante (Estructura de Caja)",
                    weight=ft.FontWeight.BOLD, size=15),
            ft.Text(
                "El modelo cruzará estos valores automáticamente en el backend para calcular "
                "tu excedente neto mensual disponible.",
                color=ft.Colors.GREY_400,
                size=12
            ),
            ft.Row([
                ingresos_fijos_input,
                gastos_fijos_input
            ], alignment=ft.MainAxisAlignment.START, spacing=15)
        ], spacing=8)

        # --- 2. SECCIÓN: Agenda de Capital Extraordinario ---
        mes_extra_dropdown = ft.Dropdown(
            label="Mes de Ejecución",
            width=140,
            options=[ft.dropdown.Option(
                str(i), f"Mes {i}") for i in range(1, 25)],
            value="6"
        )

        monto_extra_input = ft.TextField(
            label="Monto Extra ($)",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER,
            value="1000000"
        )

        def agregar_ingreso_lista(e_click):
            pass

        bloque_ingresos_extras = ft.Column([
            ft.Text("2. Agenda de Capital Extraordinario",
                    weight=ft.FontWeight.BOLD, size=15),
            ft.Text(
                "Planifica inyecciones de capital conocidas (Primas, bonos, etc.). "
                "El modelo integrará estos eventos directamente en la línea de tiempo del backend.",
                color=ft.Colors.GREY_400,
                size=12
            ),
            ft.Row([
                mes_extra_dropdown,
                monto_extra_input,
                ft.Button("Planificar", on_click=agregar_ingreso_lista)
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            ft.Text(
                "💡 Flexibilidad total: Si recibes un ingreso imprevisto en el futuro, "
                "podrás inyectarlo sobre la marcha en la simulación.",
                italic=True, size=11, color=ft.Colors.BLUE_200
            )
        ], spacing=8)

        contenido_panel = ft.Container(
            content=ft.Column([
                bloque_flujo_caja,
                ft.Divider(height=25, color=ft.Colors.GREY_700),
                bloque_ingresos_extras
            ], spacing=15, scroll=ft.ScrollMode.AUTO),
            width=500,
            height=380,
            padding=10
        )

        # --- Lógica de Persistencia Directa a API con Control de Cursor ---
        def procesar_guardado(e_click):
            try:
                ingresos = float(ingresos_fijos_input.value)
                gastos = float(gastos_fijos_input.value)

                # 1. Cambiamos el estado del botón y ponemos cursor en espera
                btn_guardar.text = "Guardando..."
                btn_guardar.disabled = True
                page.cursor = "wait"
                page.update()

                exito = APIClient.guardar_configuracion(
                    ingresos_fijos=ingresos, gastos_fijos=gastos)

                # 2. LIBERAMOS EL CURSOR INMEDIATAMENTE (Volver a la normalidad)
                page.cursor = "default"

                if exito:
                    # Cerramos el modal de configuración original
                    setattr(dialogo_config, "open", False)
                    page.update()

                    # Creamos el nuevo modal de éxito con botón de Aceptar
                    dialogo_exito = ft.AlertDialog(
                        title=ft.Text("Registro Exitoso",
                                      weight=ft.FontWeight.BOLD),
                        content=ft.Text(
                            "Los parámetros financieros se han registrado correctamente en el backend."),
                        actions=[
                            ft.Button(
                                "Aceptar",
                                on_click=lambda _: setattr(
                                    dialogo_exito, "open", False) or page.update()
                            )
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )

                    page.overlay.append(dialogo_exito)
                    dialogo_exito.open = True
                    page.update()

                else:
                    # Si falla, restauramos el botón y actualizamos
                    btn_guardar.text = "Guardar Parámetros"
                    btn_guardar.disabled = False
                    dialogo_config.title = ft.Text(
                        "⚠️ Error al guardar en API")
                    page.update()

            except ValueError:
                page.cursor = "default"  # Liberar también en caso de error de tipeo
                btn_guardar.text = "Guardar Parámetros"
                btn_guardar.disabled = False
                dialogo_config.title = ft.Text(
                    "⚠️ Ingresa solo números válidos")
                page.update()

        # Instanciamos el botón de guardado fuera para poder mutar sus estados visuales
        btn_guardar = ft.Button("Guardar Parámetros",
                                on_click=procesar_guardado)

        # --- Diálogo Emergente Estructurado ---
        dialogo_config = ft.AlertDialog(
            title=ft.Text("Parámetros del Modelo de Simulación"),
            content=contenido_panel,
            actions=[
                btn_guardar,
                ft.Button("Cancelar", on_click=lambda _: setattr(
                    dialogo_config, "open", False) or page.update())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialogo_config)
        dialogo_config.open = True
        page.update()

    # ==========================================
    # 3. BARRA DE MENÚ / NAVEGACIÓN SUPERIOR
    # ==========================================
    page.appbar = ft.AppBar(
        title=ft.Text("Módulo de Optimización", weight=ft.FontWeight.W_500),
        center_title=False,
        bgcolor="#1e1e2e",
        actions=[
            ft.Button("Actualizar", on_click=cargar_datos_ui),
            ft.Button("Configuración", on_click=abrir_configuracion),
        ],
    )

    # Encabezado principal del Dashboard
    header = ft.Column([
        ft.Text("Dashboard de Deudas", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Visualización modular del inventario financiero actual.",
                color=ft.Colors.GREY_400),
        ft.Divider(height=20)
    ])

    # ==========================================
    # 4. PANEL DE INTERACCIÓN (ESTRATEGIA)
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

        resultado_texto.value = (
            f"✅ Simulación procesada con éxito.\n"
            f"Estrategia activa: {estrategia.upper()} con un aporte extra de ${int(excedente):,.2f}/mes.\n"
            f"¡El motor modular de backend está listo para procesar el cronograma!"
        )
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

    # Inyección de componentes en la vista base
    page.add(
        header,
        cards_grid,
        ft.Divider(height=30, color="transparent"),
        ft.Text("Panel de Simulación Interactiva",
                size=20, weight=ft.FontWeight.BOLD),
        panel_controles,
        ft.Container(content=resultado_texto, padding=10)
    )

    page.update()
    cargar_datos_ui()


if __name__ == "__main__":
    ft.run(main)
