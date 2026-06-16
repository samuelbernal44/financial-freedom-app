# backend/app/services/debt_optimizer.py
from typing import List, Dict, Any
from backend.app.services.finance_core import FinanceCoreService


class DebtOptimizerService:

    @staticmethod
    def ordenar_deudas(deudas: List[Dict[str, Any]], estrategia: str) -> List[Dict[str, Any]]:
        """
        Ordena las deudas según la estrategia seleccionada:
        - 'bola_de_nieve': De menor a mayor saldo (motivación rápida).
        - 'avalancha': De mayor a menor tasa de interés (optimización matemática de intereses).
        """
        if estrategia == "bola_de_nieve":
            return sorted(deudas, key=lambda x: x["total_amount"])
        elif estrategia == "avalancha":
            return sorted(deudas, key=lambda x: x["interest_rate"], reverse=True)
        return deudas

    @classmethod
    def simular_liquidacion_total(
        cls,
        lista_deudas: List[Dict[str, Any]],
        ingreso_fijo: float,
        gasto_fijo: float,
        ingresos_eventuales: Dict[int, float],
        estrategia: str = "avalancha"
    ) -> Dict[str, Any]:
        """
        Simula la vida financiera del usuario mes a mes hasta que TODAS las deudas queden en cero.
        Calcula el impacto de aplicar el excedente disponible como abono extraordinario a capital.
        """
        # 1. Ordenar deudas según la estrategia
        deudas_activas = cls.ordenar_deudas(lista_deudas, estrategia)

        cronograma_global = []
        mes_simulacion = 1
        total_intereses_pagados = 0.0

        # Clonar el saldo actual para manipularlo en la simulación temporal
        for d in deudas_activas:
            d["saldo_temporal"] = d["total_amount"]
            # Calcular la tasa mensual vencida
            d["tasa_mensual"] = (1 + d["interest_rate"] / 100) ** (1 / 12) - 1
            # Calcular la cuota mínima base aproximada pactada
            d["cuota_minima"] = (d["total_amount"] * (d["tasa_mensual"] * (1 + d["tasa_mensual"]) ** d["pacted_months"]) /
                                 (((1 + d["tasa_mensual"]) ** d["pacted_months"]) - 1)) if d["tasa_mensual"] > 0 else d["total_amount"] / d["pacted_months"]

        # Bucle de simulación mes a mes hasta liquidar todo
        # Límite 30 años por seguridad
        while any(d["saldo_temporal"] > 0 for d in deudas_activas) and mes_simulacion <= 360:

            # Calcular el excedente disponible para este mes específico (incluye eventuales)
            excedente_mes = FinanceCoreService.calcular_excedente_mensual(
                ingreso_fijo, gasto_fijo, ingresos_eventuales, mes_simulacion
            )

            registro_mes = {
                "mes": mes_simulacion,
                "estado_deudas": [],
                "excedente_aplicado": 0.0,
                "interes_total_mes": 0.0
            }

            # Fase A: Aplicar los intereses del mes y calcular cuotas mínimas obligatorias
            for d in deudas_activas:
                if d["saldo_temporal"] > 0:
                    interes_del_mes = d["saldo_temporal"] * d["tasa_mensual"]
                    d["saldo_temporal"] += interes_del_mes
                    total_intereses_pagados += interes_del_mes
                    registro_mes["interes_total_mes"] += interes_del_mes

                    # Pago de la cuota mínima obligatoria
                    pago = min(d["cuota_minima"], d["saldo_temporal"])
                    d["saldo_temporal"] -= pago

            # Fase B: Inyectar el Excedente Extraordinario a Capital (Abono Dirigido)
            # Se aplica exclusivamente a la primera de la lista que aún tenga saldo (según la estrategia)
            for d in deudas_activas:
                if d["saldo_temporal"] > 0 and excedente_mes > 0:
                    abono_extra = min(excedente_mes, d["saldo_temporal"])
                    d["saldo_temporal"] -= abono_extra
                    excedente_mes -= abono_extra
                    registro_mes["excedente_aplicado"] += abono_extra

            # Guardar el estado de cada deuda al finalizar el mes para que la UI pueda graficarlo
            for d in deudas_activas:
                registro_mes["estado_deudas"].append({
                    "nombre": d["name"],
                    "saldo_restante": round(d["saldo_temporal"], 2)
                })

            registro_mes["interes_total_mes"] = round(
                registro_mes["interes_total_mes"], 2)
            cronograma_global.append(registro_mes)
            mes_simulacion += 1

        return {
            "estrategia_aplicada": estrategia,
            "meses_hasta_libertad": mes_simulacion - 1,
            "total_intereses_pagados": round(total_intereses_pagados, 2),
            "cronograma_mes_a_mes": cronograma_global
        }
