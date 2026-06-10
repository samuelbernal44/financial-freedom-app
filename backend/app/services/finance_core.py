# backend/app/services/finance_core.py
from datetime import datetime
from typing import List, Dict, Any


class FinanceCoreService:

    @staticmethod
    def calcular_tabla_amortizacion(
        monto_original: float,
        tasa_anual_efectiva: float,
        cuotas_pactadas: int,
        fecha_inicio: str
    ) -> List[Dict[str, Any]]:
        """
        Calcula el plan de pagos estándar (Amortización Francesa) para una deuda.
        Devuelve el desglose mes a mes de intereses, abono a capital y saldo restante.
        """
        # Convertir Tasa Efectiva Anual (EA) a Tasa Mensual Vencida (MV)
        tasa_mensual = (1 + tasa_anual_efectiva / 100) ** (1 / 12) - 1

        # Calcular el valor de la cuota mensual fija usando la fórmula estándar de anualidades
        if tasa_mensual > 0:
            cuota_mensual = monto_original * \
                (tasa_mensual * (1 + tasa_mensual) ** cuotas_pactadas) / \
                (((1 + tasa_mensual) ** cuotas_pactadas) - 1)
        else:
            cuota_mensual = monto_original / cuotas_pactadas

        tabla = []
        saldo_pendiente = monto_original
        fecha_actual = datetime.strptime(fecha_inicio, "%Y-%m-%d")

        for mes in range(1, cuotas_pactadas + 1):
            interes_mes = saldo_pendiente * tasa_mensual
            abono_capital = cuota_mensual - interes_mes
            saldo_pendiente -= abono_capital

            # Controlar que el saldo no quede en negativo por decimales
            if saldo_pendiente < 0:
                saldo_pendiente = 0

            tabla.append({
                "mes": mes,
                "fecha_pago": fecha_actual.strftime("%Y-%m-%d"),
                "cuota_total": round(cuota_mensual, 2),
                "interes": round(interes_mes, 2),
                "abono_capital": round(abono_capital, 2),
                "saldo_restante": round(saldo_pendiente, 2)
            })

            # Avanzar al siguiente mes (aproximación lógica)
            # En producción usaremos librerías como dateutil para un manejo exacto de calendarios
            año_nuevo = fecha_actual.year + (fecha_actual.month // 12)
            mes_nuevo = (fecha_actual.month % 12) + 1
            fecha_actual = fecha_actual.replace(
                year=año_nuevo, month=mes_nuevo)

        return tabla

    @staticmethod
    def calcular_excedente_mensual(
        ingresos_fijos: float,
        gastos_fijos: float,
        ingresos_eventuales: Dict[int, float],
        mes_actual: int
    ) -> float:
        """
        Calcula el dinero libre (excedente) disponible en un mes específico 
        para inyectar como pago extraordinario a las deudas.
        """
        excedente_base = ingresos_fijos - gastos_fijos
        extra = ingresos_eventuales.get(mes_actual, 0.0)
        return max(0.0, excedente_base + extra)
