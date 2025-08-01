"""
test_api.py
Pruebas de integración para la API REST.
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
import json

from api import app
from auth import create_access_token

client = TestClient(app)

# Token de prueba
test_token = create_access_token({"sub": "test_user"})
headers = {"Authorization": f"Bearer {test_token}"}

def test_root_endpoint():
    """Prueba el endpoint raíz de la API."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app" in data
    assert data["app"] == "Neoproyectto API"
    assert "status" in data
    assert data["status"] == "running"

@patch('main.gestionar_inversion_dividendos_mensuales')
def test_api_dividendos(mock_dividendos):
    """Prueba el endpoint de dividendos."""
    # Configurar el mock
    mock_dividendos.return_value = {
        "activos": [
            {"nombre": "AAPL", "asignacion": 5000},
            {"nombre": "MSFT", "asignacion": 5000}
        ],
        "capital_total": 10000,
        "moneda": "EUR"
    }
    
    # Datos de la solicitud
    data = {
        "capital": 10000,
        "moneda": "EUR",
        "preferencias": {"sector": "tecnología"}
    }
    
    # Realizar solicitud
    response = client.post("/api/dividendos", headers=headers, json=data)
    
    # Verificaciones
    assert response.status_code == 200
    result = response.json()
    assert "activos" in result
    assert len(result["activos"]) == 2
    assert result["capital_total"] == 10000
    
    # Verificar que se llamó a la función con los parámetros correctos
    mock_dividendos.assert_called_once_with(
        capital=10000, 
        moneda="EUR", 
        preferencias={"sector": "tecnología"}
    )

@patch('main.autoinversion_ia_global')
def test_api_autoinversion(mock_autoinversion):
    """Prueba el endpoint de autoinversión."""
    # Configurar el mock
    mock_autoinversion.return_value = {
        "cartera_inicial": {
            "activos": [
                {"nombre": "AAPL", "asignacion": 5000},
                {"nombre": "MSFT", "asignacion": 5000}
            ],
            "capital_total": 10000
        },
        "movimientos": []
    }
    
    # Datos de la solicitud
    data = {
        "capital": 10000,
        "moneda": "USD",
        "perfil_riesgo": "alto",
        "preferencias_avanzadas": {"sector": "tecnología"},
        "porcentaje_ganancia_reventa": 12,
        "tolerancia_perdida": 1.5
    }
    
    # Realizar solicitud
    response = client.post("/api/autoinversion", headers=headers, json=data)
    
    # Verificaciones
    assert response.status_code == 200
    result = response.json()
    assert "cartera_inicial" in result
    assert "movimientos" in result
    
    # Verificar que se llamó a la función con los parámetros correctos
    mock_autoinversion.assert_called_once()

def test_api_dividendos_invalid_data():
    """Prueba el endpoint de dividendos con datos inválidos."""
    # Datos inválidos
    data = {
        "capital": -1000,  # Capital negativo
        "moneda": "EUR"
    }
    
    # Realizar solicitud
    response = client.post("/api/dividendos", headers=headers, json=data)
    
    # Verificaciones
    assert response.status_code == 422  # Validation error

def test_api_unauthorized():
    """Prueba acceso no autorizado a endpoints protegidos."""
    # Sin token
    response = client.post("/api/dividendos", json={"capital": 10000, "moneda": "EUR"})
    assert response.status_code == 401
    
    # Token inválido
    response = client.post(
        "/api/dividendos", 
        headers={"Authorization": "Bearer invalid_token"},
        json={"capital": 10000, "moneda": "EUR"}
    )
    assert response.status_code == 401