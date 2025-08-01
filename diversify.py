"""
diversify.py
Construye una cartera diversificada según los activos seleccionados y el capital disponible.
"""

def build_portfolio(selected_assets, capital):
    """
    Construye la cartera con asignación de capital entre activos.

    Args:
        selected_assets (list): Activos seleccionados.
        capital (float): Capital disponible para invertir.

    Returns:
        dict: Cartera con asignación y activos.
    """
    n = len(selected_assets)
    if n == 0:
        return {}
    asignacion = capital / n
    cartera = {
        "activos": [
            {
                "nombre": a["nombre"],
                "sector": a.get("sector"),
                "tipo": a.get("tipo"),
                "riesgo": a.get("riesgo", "moderado"),
                "asignacion": asignacion,
                "rendimiento_simulado": a.get("rendimiento_simulado", 0),
                "probabilidad_ganancia": a.get("probabilidad_ganancia", 0)
            } for a in selected_assets
        ],
        "capital_total": capital
    }
    return cartera