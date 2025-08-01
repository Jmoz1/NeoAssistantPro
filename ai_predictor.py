"""
ai_predictor.py
Simula una función de IA para calcular la probabilidad de ganancia de un activo.
"""

import random

def calcular_probabilidad_ganancia(activo, perfil_riesgo, preferencias):
    """
    Calcula (simula) la probabilidad de ganancia de un activo usando IA.

    Args:
        activo (dict): Información del activo.
        perfil_riesgo (str): Perfil de riesgo.
        preferencias (dict): Preferencias extra.

    Returns:
        float: Probabilidad de ganancia (0-1).
    """
    base = random.uniform(0.3, 0.9)
    if perfil_riesgo == "alto":
        base += 0.1
    if preferencias and activo.get("sector") == preferencias.get("sector"):
        base += 0.05
    return min(base, 1.0)