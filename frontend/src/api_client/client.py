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
