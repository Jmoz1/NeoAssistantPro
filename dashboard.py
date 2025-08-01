"""
dashboard.py
Funciones para la visualización y análisis de carteras de inversión.
"""

from typing import Dict, List, Any, Optional

def mostrar_dashboard(cartera: Dict[str, Any], periodo: str = "mensual") -> Dict[str, Any]:
    """
    Genera datos para mostrar en el dashboard principal.
    
    Args:
        cartera (dict): Cartera de inversión actual.
        periodo (str): Periodo de análisis (diario, semanal, mensual, anual).
        
    Returns:
        dict: Datos procesados para visualización.
    """
    # Simulación de generación de datos para dashboard
    total_activos = len(cartera.get("activos", []))
    rendimiento_total = sum(
        activo.get("rendimiento_simulado", 0) * activo.get("asignacion", 0) 
        for activo in cartera.get("activos", [])
    ) / cartera.get("capital_total", 1)
    
    return {
        "resumen": {
            "capital_total": cartera.get("capital_total", 0),
            "moneda": cartera.get("moneda", "EUR"),
            "rendimiento_total": rendimiento_total,
            "total_activos": total_activos
        },
        "distribucion_sectores": _calcular_distribucion_sectores(cartera),
        "distribucion_riesgo": _calcular_distribucion_riesgo(cartera),
        "periodo_analisis": periodo
    }

def _calcular_distribucion_sectores(cartera: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Calcula la distribución de la cartera por sectores.
    """
    sectores = {}
    for activo in cartera.get("activos", []):
        sector = activo.get("sector", "otros")
        if sector not in sectores:
            sectores[sector] = 0
        sectores[sector] += activo.get("asignacion", 0)
    
    return [{"sector": k, "valor": v} for k, v in sectores.items()]

def _calcular_distribucion_riesgo(cartera: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Calcula la distribución de la cartera por nivel de riesgo.
    """
    riesgos = {"bajo": 0, "moderado": 0, "alto": 0}
    for activo in cartera.get("activos", []):
        riesgo = activo.get("riesgo", "moderado")
        riesgos[riesgo] = riesgos.get(riesgo, 0) + activo.get("asignacion", 0)
    
    return [{"riesgo": k, "valor": v} for k, v in riesgos.items() if v > 0]

def generar_informe_rendimiento(cartera: Dict[str, Any], periodo: str = "mensual") -> Dict[str, Any]:
    """
    Genera un informe detallado de rendimiento de la cartera.
    
    Args:
        cartera (dict): Cartera de inversión.
        periodo (str): Periodo del informe.
        
    Returns:
        dict: Informe de rendimiento.
    """
    # Implementación básica
    rendimientos = {
        "global": sum(
            activo.get("rendimiento_simulado", 0) * activo.get("asignacion", 0) 
            for activo in cartera.get("activos", [])
        ) / cartera.get("capital_total", 1),
        "por_activo": [
            {
                "nombre": activo.get("nombre", ""),
                "rendimiento": activo.get("rendimiento_simulado", 0),
                "contribucion": activo.get("rendimiento_simulado", 0) * activo.get("asignacion", 0) / cartera.get("capital_total", 1)
            }
            for activo in cartera.get("activos", [])
        ]
    }
    
    return {
        "periodo": periodo,
        "rendimientos": rendimientos,
        "fecha_informe": "2023-08-01"
    }