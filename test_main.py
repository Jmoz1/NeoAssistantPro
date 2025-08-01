import pytest
from main import (
    gestionar_inversion_dividendos_mensuales,
    autoinversion_ia_global,
    puente_autoinversion_a_dividendos
)

def test_gestionar_inversion_dividendos_mensuales():
    result = gestionar_inversion_dividendos_mensuales(
        capital=10000,
        moneda='EUR',
        preferencias={"sector": "tecnología"}
    )
    assert "activos" in result

def test_autoinversion_ia_global():
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