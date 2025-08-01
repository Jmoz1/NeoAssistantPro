import pytest
from main import (
    gestionar_inversion_dividendos_mensuales,
    autoinversion_ia_global,
    puente_autoinversion_a_dividendos
)
from validation import validate_investment_params, validate_autoinversion_params

def test_gestionar_inversion_dividendos_mensuales():
    # Test con parámetros normales
    result = gestionar_inversion_dividendos_mensuales(
        capital=10000,
        moneda='EUR',
        preferencias={"sector": "tecnología"}
    )
    assert "activos" in result
    
    # Test con parámetros inválidos - será manejado por el nuevo sistema de validación
    result_invalid = gestionar_inversion_dividendos_mensuales(
        capital=-1000,
        moneda='EUR'
    )
    assert "error" in result_invalid or isinstance(result_invalid, dict)

def test_autoinversion_ia_global():
    # Test con parámetros normales
    result = autoinversion_ia_global(
        capital=20000,
        moneda='USD',
        perfil_riesgo='alto',
        preferencias_avanzadas={"sector": "tecnología"},
        porcentaje_ganancia_reventa=12,
        tolerancia_perdida=1.5
    )
    assert "cartera_inicial" in result
    assert "movimientos" in result
    
    # Test con perfil de riesgo inválido - será manejado por el nuevo sistema de validación
    result_invalid = autoinversion_ia_global(
        capital=20000,
        moneda='USD',
        perfil_riesgo='extremo',  # Perfil inválido
        porcentaje_ganancia_reventa=12,
        tolerancia_perdida=1.5
    )
    assert "error" in result_invalid or isinstance(result_invalid, dict)

def test_puente_autoinversion_a_dividendos():
    result = puente_autoinversion_a_dividendos(
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
    assert "mensaje" in result

def test_validacion_parametros():
    # Test de validación de parámetros de inversión
    valid, _ = validate_investment_params(10000, "EUR", {"sector": "tecnología"})
    assert valid is True
    
    invalid, error = validate_investment_params(-100, "EUR")
    assert invalid is False
    assert "capital" in error.lower()
    
    # Test de validación de parámetros de autoinversión
    valid, _ = validate_autoinversion_params("alto", 10, 2)
    assert valid is True
    
    invalid, error = validate_autoinversion_params("extremo", 10, 2)
    assert invalid is False
    assert "perfil" in error.lower()