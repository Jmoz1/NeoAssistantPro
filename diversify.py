"""
diversify.py
Construye y optimiza portfolios de inversión basados en activos seleccionados.
"""

def build_portfolio(assets, capital):
    """
    Construye un portfolio diversificado basado en activos seleccionados.
    
    Args:
        assets (list): Lista de activos seleccionados.
        capital (float): Capital disponible para inversión.
        
    Returns:
        dict: Portfolio construido con asignaciones de capital.
    """
    if not assets:
        return {"activos": [], "capital_total": capital, "moneda": "EUR"}
        
    # Cálculo simple de pesos basado en probabilidad de ganancia
    total_prob = sum(asset.get("probabilidad_ganancia", 1) for asset in assets)
    
    cartera = {
        "activos": [],
        "capital_total": capital,
        "moneda": "EUR",
        "fecha_creacion": "2023-08-01"
    }
    
    capital_restante = capital
    
    for i, asset in enumerate(assets):
        # Último activo recibe el capital restante para evitar problemas de redondeo
        if i == len(assets) - 1:
            asignacion = capital_restante
        else:
            peso = asset.get("probabilidad_ganancia", 1) / total_prob
            asignacion = round(capital * peso, 2)
            capital_restante -= asignacion
            
        activo_cartera = {
            "nombre": asset.get("nombre", f"Activo {i}"),
            "sector": asset.get("sector", "general"),
            "tipo": asset.get("tipo", "activo"),
            "asignacion": asignacion,
            "porcentaje": round(asignacion / capital * 100, 2),
            "rendimiento_simulado": asset.get("rendimiento_simulado", 0)
        }
        cartera["activos"].append(activo_cartera)
        
    return cartera

def rebalance_portfolio(portfolio, market_changes):
    """
    Rebalancea un portfolio existente basado en cambios del mercado.
    
    Args:
        portfolio (dict): Portfolio existente.
        market_changes (dict): Cambios en el mercado por activo.
        
    Returns:
        dict: Portfolio rebalanceado.
    """
    # Esta función se implementará en la siguiente fase
    return portfolio