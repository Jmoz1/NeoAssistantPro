"""
test_portfolio.py
Pruebas unitarias para la funcionalidad de portfolio.
"""
import unittest
import pytest
from unittest.mock import patch, MagicMock
import json

from diversify import build_portfolio
from main import gestionar_inversion_dividendos_mensuales
from ai_predictor import FinancialPredictor, calcular_probabilidad_ganancia
from validation import validate_investment_params

# Datos para pruebas
test_assets = [
    {
        "nombre": "AAPL", 
        "sector": "tecnología", 
        "tipo": "acción", 
        "rendimiento_simulado": 7.5,
        "probabilidad_ganancia": 0.8,
        "riesgo": "moderado"
    },
    {
        "nombre": "MSFT", 
        "sector": "tecnología", 
        "tipo": "acción", 
        "rendimiento_simulado": 6.2,
        "probabilidad_ganancia": 0.75,
        "riesgo": "bajo"
    },
    {
        "nombre": "AMZN", 
        "sector": "consumo", 
        "tipo": "acción", 
        "rendimiento_simulado": 8.1,
        "probabilidad_ganancia": 0.65,
        "riesgo": "alto"
    }
]

class TestDiversify(unittest.TestCase):
    """Pruebas para el módulo de diversificación."""
    
    def test_build_portfolio_empty_assets(self):
        """Prueba la construcción de portfolio con lista de activos vacía."""
        result = build_portfolio([], 10000)
        self.assertEqual(result["capital_total"], 10000)
        self.assertEqual(len(result["activos"]), 0)
    
    def test_build_portfolio_with_assets(self):
        """Prueba la construcción de portfolio con activos válidos."""
        result = build_portfolio(test_assets, 10000)
        self.assertEqual(result["capital_total"], 10000)
        self.assertEqual(len(result["activos"]), len(test_assets))
        self.assertEqual(result["moneda"], "EUR")
        
        # Verificar asignación de capital
        total_assigned = sum(asset["asignacion"] for asset in result["activos"])
        self.assertAlmostEqual(total_assigned, 10000, places=1)
        
    def test_build_portfolio_preserves_asset_info(self):
        """Verifica que la información importante de los activos se preserva."""
        result = build_portfolio(test_assets, 10000)
        for i, original_asset in enumerate(test_assets):
            portfolio_asset = result["activos"][i]
            self.assertEqual(portfolio_asset["nombre"], original_asset["nombre"])
            self.assertEqual(portfolio_asset["sector"], original_asset["sector"])
            self.assertEqual(portfolio_asset["tipo"], original_asset["tipo"])
            
class TestAiPredictor(unittest.TestCase):
    """Pruebas para el predictor de IA."""
    
    def test_calcular_probabilidad_ganancia(self):
        """Prueba el cálculo de probabilidad de ganancia."""
        asset = test_assets[0]
        probability = calcular_probabilidad_ganancia(asset, "moderado")
        self.assertGreaterEqual(probability, 0.0)
        self.assertLessEqual(probability, 1.0)
        
    def test_financial_predictor_basic_simulation(self):
        """Prueba la simulación básica del predictor financiero."""
        predictor = FinancialPredictor()
        asset = test_assets[0]
        result = predictor.predict_return(asset, "1m")
        self.assertIsInstance(result, float)
        
class TestValidation(unittest.TestCase):
    """Pruebas para el sistema de validación."""
    
    def test_validate_investment_params_valid(self):
        """Prueba la validación con parámetros válidos."""
        valid, _ = validate_investment_params(10000, "EUR", {"sector": "tecnología"})
        self.assertTrue(valid)
        
    def test_validate_investment_params_invalid_capital(self):
        """Prueba la validación con capital inválido."""
        valid, error = validate_investment_params(-1000, "EUR")
        self.assertFalse(valid)
        self.assertIn("capital", error.lower())
        
    def test_validate_investment_params_invalid_moneda(self):
        """Prueba la validación con moneda inválida."""
        valid, error = validate_investment_params(10000, 123)
        self.assertFalse(valid)
        self.assertIn("moneda", error.lower())

@pytest.mark.parametrize("capital,moneda,expected", [
    (10000, "EUR", True),
    (-1000, "EUR", False),
    (10000, 123, False),
    (0, "USD", False)
])
def test_validate_investment_params_parametrized(capital, moneda, expected):
    """Prueba parametrizada para validate_investment_params."""
    valid, _ = validate_investment_params(capital, moneda)
    assert valid == expected

@patch('scraper.fetch_dividend_data')
@patch('asset_selector.select_dividend_assets')
def test_gestionar_inversion_dividendos_mensuales(mock_select, mock_fetch):
    """Prueba la gestión de inversión con dependencias simuladas."""
    # Configurar mocks
    mock_fetch.return_value = test_assets
    mock_select.return_value = test_assets
    
    # Ejecutar función
    result = gestionar_inversion_dividendos_mensuales(10000, "EUR", {"sector": "tecnología"})
    
    # Verificaciones
    assert "activos" in result
    assert len(result["activos"]) == len(test_assets)
    mock_fetch.assert_called_once()
    mock_select.assert_called_once()

if __name__ == "__main__":
    unittest.main()