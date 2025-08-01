"""
ai_predictor.py
Implementación de algoritmos de predicción financiera avanzados.
"""
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import logging

from logger import NeoproyecttoLogger
from error_handling import InvestmentError

# Inicializar logger
logger = NeoproyecttoLogger("neoproyectto.ai_predictor")

class FinancialPredictor:
    """
    Clase para realizar predicciones financieras basadas en modelos de ML.
    """
    
    def __init__(self, historical_data: Optional[pd.DataFrame] = None):
        """
        Inicializa el predictor financiero.
        
        Args:
            historical_data: Datos históricos para entrenar los modelos.
        """
        self.historical_data = historical_data
        self.models = {}
        self.scaler = StandardScaler()
        
        # Verificar si tenemos datos históricos para entrenar
        if historical_data is not None and not historical_data.empty:
            self._train_models()
    
    def _train_models(self):
        """
        Entrena modelos de predicción con datos históricos.
        """
        logger.info("Entrenando modelos de predicción financiera")
        
        try:
            # Preparar datos
            X = self.historical_data.drop(['rendimiento'], axis=1)
            y = self.historical_data['rendimiento']
            
            # Escalar características
            X_scaled = self.scaler.fit_transform(X)
            
            # Entrenar modelos
            # 1. Regresión lineal
            lr_model = LinearRegression()
            lr_model.fit(X_scaled, y)
            self.models['linear'] = lr_model
            
            # 2. Random Forest
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X_scaled, y)
            self.models['random_forest'] = rf_model
            
            logger.info("Modelos entrenados correctamente")
            
        except Exception as e:
            logger.error("Error entrenando modelos de predicción", exception=e)
            raise InvestmentError("No se pudieron entrenar los modelos de predicción", 
                                {"error": str(e)})
    
    def predict_return(self, asset: Dict[str, Any], timeframe: str = '1m') -> float:
        """
        Predice el retorno esperado para un activo.
        
        Args:
            asset: Datos del activo.
            timeframe: Marco temporal para la predicción ('1m', '3m', '6m', '1y').
            
        Returns:
            float: Retorno esperado en porcentaje.
        """
        # Si no tenemos modelos entrenados, usar simulación básica
        if not self.models:
            logger.warning("Usando simulación básica por falta de modelos entrenados")
            return self._simulate_basic_return(asset, timeframe)
            
        try:
            # Preparar datos del activo para predicción
            asset_features = self._extract_features(asset)
            
            # Escalar características
            asset_scaled = self.scaler.transform([asset_features])
            
            # Realizar predicción con ambos modelos
            lr_pred = self.models['linear'].predict(asset_scaled)[0]
            rf_pred = self.models['random_forest'].predict(asset_scaled)[0]
            
            # Promedio ponderado (dando más peso al Random Forest)
            prediction = 0.3 * lr_pred + 0.7 * rf_pred
            
            # Ajustar predicción según timeframe
            timeframe_factor = self._get_timeframe_factor(timeframe)
            adjusted_prediction = prediction * timeframe_factor
            
            logger.info(f"Predicción para activo {asset.get('nombre', 'desconocido')}: {adjusted_prediction}%",
                      {"asset": asset.get('nombre'), "prediction": adjusted_prediction})
                      
            return adjusted_prediction
            
        except Exception as e:
            logger.error(f"Error prediciendo retorno para {asset.get('nombre', 'desconocido')}", 
                       exception=e)
            # Fallback a simulación básica
            return self._simulate_basic_return(asset, timeframe)
    
    def _extract_features(self, asset: Dict[str, Any]) -> List[float]:
        """
        Extrae características numéricas de un activo para predicción.
        """
        # Mapeo de sectores a valores numéricos
        sector_mapping = {
            "tecnología": 1.0,
            "finanzas": 2.0,
            "salud": 3.0,
            "consumo": 4.0,
            "energía": 5.0,
            "industrial": 6.0,
            "otros": 7.0
        }
        
        # Mapeo de tipos a valores numéricos
        tipo_mapping = {
            "acción": 1.0,
            "bono": 2.0,
            "fondo": 3.0,
            "etf": 4.0,
            "cripto": 5.0,
            "otros": 6.0
        }
        
        # Mapeo de riesgo a valores numéricos
        riesgo_mapping = {
            "bajo": 1.0,
            "moderado": 2.0,
            "alto": 3.0
        }
        
        # Extraer características
        sector = sector_mapping.get(asset.get('sector', '').lower(), 7.0)
        tipo = tipo_mapping.get(asset.get('tipo', '').lower(), 6.0)
        riesgo = riesgo_mapping.get(asset.get('riesgo', '').lower(), 2.0)
        
        # Obtener otras características numéricas
        price = asset.get('precio', 50.0)  # Precio por defecto si no está disponible
        volatility = asset.get('volatilidad', 0.1)  # Volatilidad por defecto
        
        # Vector de características
        features = [sector, tipo, riesgo, price, volatility]
        return features
    
    def _get_timeframe_factor(self, timeframe: str) -> float:
        """
        Obtiene un factor multiplicador basado en el marco temporal.
        """
        mapping = {
            '1m': 1.0,    # 1 mes
            '3m': 2.5,    # 3 meses
            '6m': 4.5,    # 6 meses
            '1y': 8.0     # 1 año
        }
        return mapping.get(timeframe, 1.0)
    
    def _simulate_basic_return(self, asset: Dict[str, Any], timeframe: str) -> float:
        """
        Simula un retorno básico basado en características del activo.
        Usado como fallback cuando no hay modelos entrenados.
        """
        # Obtener factores base según tipo y sector
        base_factor = 0.0
        
        # Factor por sector
        sector = asset.get('sector', '').lower()
        if sector == 'tecnología':
            base_factor += 0.8
        elif sector == 'finanzas':
            base_factor += 0.6
        elif sector == 'salud':
            base_factor += 0.7
        elif sector == 'energía':
            base_factor += 0.5
        elif sector == 'industrial':
            base_factor += 0.6
        else:
            base_factor += 0.4
        
        # Factor por tipo
        tipo = asset.get('tipo', '').lower()
        if tipo == 'acción':
            base_factor += 0.7
        elif tipo == 'bono':
            base_factor += 0.3
        elif tipo == 'fondo':
            base_factor += 0.5
        elif tipo == 'etf':
            base_factor += 0.6
        elif tipo == 'cripto':
            base_factor += 1.2
        else:
            base_factor += 0.4
        
        # Factor por riesgo
        riesgo = asset.get('riesgo', '').lower()
        if riesgo == 'bajo':
            base_factor *= 0.7
        elif riesgo == 'alto':
            base_factor *= 1.4
        
        # Añadir componente aleatorio
        random_component = np.random.normal(0, 0.2)
        
        # Calcular retorno simulado
        timeframe_factor = self._get_timeframe_factor(timeframe)
        return (base_factor + random_component) * timeframe_factor

# Función compatible con versiones anteriores
def calcular_probabilidad_ganancia(activo, perfil_riesgo='moderado', preferencias=None):
    """
    Calcula la probabilidad de ganancia de un activo (función legacy).
    """
    predictor = FinancialPredictor()
    expected_return = predictor.predict_return(activo)
    
    # Convertir retorno esperado a probabilidad (0-1)
    if expected_return <= -10:
        probability = 0.1
    elif expected_return >= 10:
        probability = 0.9
    else:
        probability = 0.5 + (expected_return / 20)
    
    # Ajustar según perfil de riesgo
    if perfil_riesgo == 'bajo':
        # Penalizar activos más volátiles
        if activo.get('riesgo') == 'alto':
            probability *= 0.8
    elif perfil_riesgo == 'alto':
        # Favorecer activos más volátiles
        if activo.get('riesgo') == 'alto':
            probability *= 1.2
            probability = min(probability, 0.95)  # Limitar a 0.95
    
    return probability