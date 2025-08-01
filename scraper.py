"""
scraper.py
Simula la obtención de datos de activos de todos los mercados y atributos para preferencias.
"""

import random

def fetch_all_market_data():
    """
    Simula la obtención de datos de activos de todos los mercados.

    Returns:
        list: Lista de activos simulados.
    """
    return [
        {
            "nombre": "Apple Inc.",
            "sector": "tecnología",
            "tipo": "acción",
            "riesgo": "moderado",
            "rendimiento_simulado": random.uniform(8, 15)
        },
        {
            "nombre": "Ethereum",
            "sector": "cripto",
            "tipo": "criptomoneda",
            "riesgo": "alto",
            "rendimiento_simulado": random.uniform(-2, 20)
        },
        {
            "nombre": "Vanguard REIT ETF",
            "sector": "inmobiliario",
            "tipo": "ETF",
            "riesgo": "bajo",
            "rendimiento_simulado": random.uniform(2, 6)
        },
        {
            "nombre": "Tesla Inc.",
            "sector": "tecnología",
            "tipo": "acción",
            "riesgo": "alto",
            "rendimiento_simulado": random.uniform(-5, 18)
        },
        {
            "nombre": "Bitcoin",
            "sector": "cripto",
            "tipo": "criptomoneda",
            "riesgo": "alto",
            "rendimiento_simulado": random.uniform(-8, 25)
        },
        {
            "nombre": "Johnson & Johnson",
            "sector": "salud",
            "tipo": "acción",
            "riesgo": "bajo",
            "rendimiento_simulado": random.uniform(1, 5)
        },
    ]

def fetch_dividend_data():
    """
    Simula la obtención de datos de activos con dividendos mensuales.

    Returns:
        list: Lista de activos simulados con dividendos mensuales.
    """
    return [
        {
            "nombre": "Realty Income Corp.",
            "sector": "inmobiliario",
            "tipo": "REIT",
            "riesgo": "bajo",
            "rendimiento_simulado": random.uniform(3, 7),
            "dividendos_mensuales": True
        },
        {
            "nombre": "STAG Industrial",
            "sector": "inmobiliario",
            "tipo": "REIT",
            "riesgo": "moderado",
            "rendimiento_simulado": random.uniform(4, 8),
            "dividendos_mensuales": True
        },
        {
            "nombre": "Apple Inc.",
            "sector": "tecnología",
            "tipo": "acción",
            "riesgo": "moderado",
            "rendimiento_simulado": random.uniform(8, 15),
            "dividendos_mensuales": False
        },
    ]