import json
import logging
from typing import Dict, Any, Optional

from asset_selector import select_dividend_assets, select_all_assets
from diversify import build_portfolio
from currency import convert_currency
from scraper import fetch_dividend_data, fetch_all_market_data
from ai_predictor import calcular_probabilidad_ganancia

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def gestionar_inversion_dividendos_mensuales(
    capital: float,
    moneda: str = 'EUR',
    preferencias: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Gestiona una inversión enfocada en dividendos mensuales.
    """
    logging.info(f"Gestionando inversión de {capital} {moneda} con enfoque en dividendos mensuales...")
    try:
        activos = fetch_dividend_data()
        if preferencias:
            activos = [a for a in activos if all(
                preferencias.get(k, True) == a.get(k, True) for k in preferencias
            )]
        activos_seleccionados = select_dividend_assets(activos, preferencias)
        cartera = build_portfolio(activos_seleccionados, capital)
        if moneda != 'EUR':
            cartera = convert_currency(cartera, 'EUR', moneda)
        return cartera
    except Exception as e:
        logging.error(f"Error en la gestión de inversión: {e}")
        return {}

def autoinversion_ia_global(
    capital: float,
    moneda: str = 'EUR',
    perfil_riesgo: str = 'moderado',
    preferencias_avanzadas: Optional[Dict[str, Any]] = None,
    porcentaje_ganancia_reventa: float = 10.0,
    tolerancia_perdida: float = 1.5
) -> Dict[str, Any]:
    """
    Autoinversión con IA avanzada.
    """
    logging.info(f"IA avanzada gestionando autoinversión en todos los mercados...")
    try:
        activos = fetch_all_market_data()
        for activo in activos:
            activo["probabilidad_ganancia"] = calcular_probabilidad_ganancia(
                activo, perfil_riesgo, preferencias_avanzadas
            )
        activos_seleccionados = select_all_assets(activos, perfil_riesgo, preferencias_avanzadas)
        activos_seleccionados = sorted(activos_seleccionados, key=lambda x: x["probabilidad_ganancia"], reverse=True)
        activos_top = activos_seleccionados[:5]
        cartera = build_portfolio(activos_top, capital)
        if moneda != 'EUR':
            cartera = convert_currency(cartera, 'EUR', moneda)
        movimientos = []
        for activo in cartera.get("activos", []):
            rendimiento = activo.get("rendimiento_simulado", 0)
            if rendimiento >= porcentaje_ganancia_reventa:
                movimientos.append({
                    "accion": "reventa_ganancia",
                    "activo": activo["nombre"],
                    "ganancia": rendimiento
                })
            elif rendimiento <= -tolerancia_perdida:
                movimientos.append({
                    "accion": "reventa_perdida",
                    "activo": activo["nombre"],
                    "perdida": rendimiento
                })
        resultado = {
            "cartera_inicial": cartera,
            "movimientos": movimientos,
            "parametros": {
                "porcentaje_ganancia_reventa": porcentaje_ganancia_reventa,
                "tolerancia_perdida": tolerancia_perdida
            }
        }
        return resultado
    except Exception as e:
        logging.error(f"Error en autoinversión IA: {e}")
        return {}

def puente_autoinversion_a_dividendos(
    capital_minimo_activacion: float,
    capital_objetivo: float,
    args_autoinversion: Dict[str, Any],
    args_dividendos: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Puente entre autoinversión IA y gestión de dividendos mensuales.
    """
    logging.info("Monitorizando autoinversión IA para puente a dividendos mensuales...")
    resultado_ia = autoinversion_ia_global(**args_autoinversion)
    capital_generado = sum(
        mov.get("ganancia", 0)
        for mov in resultado_ia.get("movimientos", [])
        if mov["accion"] == "reventa_ganancia"
    )
    logging.info(f"Capital generado por IA: {capital_generado}")
    if capital_generado >= capital_minimo_activacion and capital_generado >= capital_objetivo:
        logging.info("Capital objetivo alcanzado. Moviendo a gestión de dividendos mensuales...")
        args_dividendos_actualizado = args_dividendos.copy()
        args_dividendos_actualizado["capital"] = capital_generado
        resultado_dividendos = gestionar_inversion_dividendos_mensuales(**args_dividendos_actualizado)
        return {
            "capital_movilizado": capital_generado,
            "resultado_dividendos": resultado_dividendos,
            "mensaje": "Capital transferido y reinvertido en dividendos mensuales."
        }
    else:
        return {
            "capital_movilizado": 0,
            "resultado_dividendos": None,
            "mensaje": "Capital generado insuficiente para transferencia."
        }

if __name__ == "__main__":
    logging.info("Neoproyectto: Centro de gestión de inversiones inteligentes")
    cartera = gestionar_inversion_dividendos_mensuales(
        capital=10000,
        moneda='EUR',
        preferencias={"sector": "tecnología"}
    )
    logging.info("Propuesta de gestión de dividendos mensuales:")
    print(json.dumps(cartera, indent=2))

    resultado = autoinversion_ia_global(
        capital=20000,
        moneda='USD',
        perfil_riesgo='alto',
        preferencias_avanzadas={"sector": "tecnología"},
        porcentaje_ganancia_reventa=12,
        tolerancia_perdida=1.5
    )
    logging.info("Propuesta de autoinversión IA global:")
    print(json.dumps(resultado, indent=2))

    puente = puente_autoinversion_a_dividendos(
        capital_minimo_activacion=500,
        capital_objetivo=1000,
        args_autoinversion={
            "capital": 20000,
            "moneda": "USD",
            "perfil_riesgo": "alto",
            "preferencias_avanzadas": {"sector": "tecnología"},
            "porcentaje_ganancia_reventa": 12,
            "tolerancia_perdida": 1.5
        },
        args_dividendos={
            "moneda": "EUR",
            "preferencias": {"sector": "tecnología"}
        }
    )
    logging.info("Resultado del puente autoinversión a dividendos:")
    print(json.dumps(puente, indent=2))