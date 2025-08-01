"""
asset_selector.py
Selecciona activos de todos los mercados según perfil de riesgo y preferencias.
"""

def select_all_assets(assets, perfil_riesgo="moderado", preferencias=None):
    """
    Selecciona activos de todos los mercados según perfil de riesgo y preferencias.

    Args:
        assets (list): Lista de activos.
        perfil_riesgo (str): Perfil de riesgo.
        preferencias (dict, opcional): Preferencias para filtrar activos.

    Returns:
        list: Activos seleccionados.
    """
    activos_filtrados = assets
    # Filtrar por preferencias (sector, tipo, etc.)
    if preferencias:
        for clave, valor in preferencias.items():
            activos_filtrados = [
                a for a in activos_filtrados if a.get(clave) == valor
            ]
    # Filtrar por perfil de riesgo (simulado)
    if perfil_riesgo == "bajo":
        activos_filtrados = [a for a in activos_filtrados if a.get("riesgo", "moderado") != "alto"]
    elif perfil_riesgo == "alto":
        activos_filtrados = [a for a in activos_filtrados if a.get("riesgo", "moderado") != "bajo"]
    return activos_filtrados

def select_dividend_assets(assets, preferencias=None):
    """
    Selecciona activos enfocados en dividendos mensuales según preferencias.

    Args:
        assets (list): Lista de activos con datos de dividendos.
        preferencias (dict, opcional): Preferencias para filtrar activos.

    Returns:
        list: Activos seleccionados (simulados).
    """
    activos_filtrados = assets
    if preferencias:
        for clave, valor in preferencias.items():
            activos_filtrados = [
                a for a in activos_filtrados if a.get(clave) == valor
            ]
    # Simula selección de activos con dividendos mensuales
    return [a for a in activos_filtrados if a.get("dividendos_mensuales", False)]