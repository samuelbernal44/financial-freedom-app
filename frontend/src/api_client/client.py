# frontend/src/api_client/client.py
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"


class APIClient:

    @staticmethod
    def obtener_deudas():
        """Consume el endpoint GET /debts/"""
        try:
            response = requests.get(f"{BASE_URL}/debts/")
            if response.status_code == 200:
                return response.json()
            return []
        except requests.exceptions.ConnectionError:
            return None  # El backend está apagado

    @staticmethod
    def obtener_perfil_financiero():
        """Consume el endpoint GET /incomes/"""
        try:
            response = requests.get(f"{BASE_URL}/incomes/")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.ConnectionError:
            return None

    @staticmethod
    def guardar_configuracion(ingresos_fijos: float, gastos_fijos: float) -> bool:
        """
        Envía los parámetros al backend usando los nombres de campos exactos (inglés)
        que el esquema de FastAPI requiere.
        """
        try:
            url = f"{BASE_URL}/incomes/"

            # CORREGIDO: Mapeo exacto de llaves según el esquema del backend
            payload = {
                "fixed_income": ingresos_fijos,
                "fixed_expenses": gastos_fijos,
                "eventual_incomes": {}  # Enviamos el diccionario vacío requerido por el esquema
            }

            print(f"[DEBUG] Enviando a {url} -> {payload}")
            response = requests.post(url, json=payload, timeout=5)
            print(
                f"[DEBUG] Código de estado del Servidor: {response.status_code}")

            if response.status_code not in [200, 201]:
                print(
                    f"[DEBUG] Respuesta detallada del Servidor: {response.text}")

            return response.status_code in [200, 201]
        except Exception as e:
            print(f"[DEBUG] Error crítico de conexión o ejecución: {e}")
            return False
