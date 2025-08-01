"""
currency.py
Convierte los valores de una cartera entre monedas simulando tasas de cambio.
"""

def convert_currency(portfolio, origen, destino):
    """
    Convierte la moneda de la cartera.

    Args:
        portfolio (dict): Cartera a convertir.
        origen (str): Moneda original.
        destino (str): Moneda destino.

    Returns:
        dict: Cartera con montos convertidos.
    """
    tasa_cambio = 1.1 if destino == "USD" and origen == "EUR" else 1
    cartera_convertida = portfolio.copy()
    for activo in cartera_convertida.get("activos", []):
        activo["asignacion"] *= tasa_cambio
    cartera_convertida["capital_total"] *= tasa_cambio
    cartera_convertida["moneda"] = destino
    return cartera_convertida