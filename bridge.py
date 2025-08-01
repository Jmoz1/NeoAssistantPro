"""
bridge.py
Implementa el puente entre sistemas de inversión y gestión de resultados.
"""

from typing import Dict, Any, Optional, List, Union
import json
import time
from datetime import datetime

from logger import NeoproyecttoLogger
from error_handling import handle_error, InvestmentError

# Inicializar logger
logger = NeoproyecttoLogger("neoproyectto.bridge")

class InvestmentBridge:
    """
    Clase que proporciona funcionalidad de puente entre diferentes 
    sistemas de inversión y estrategias.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa el puente con la configuración proporcionada.
        
        Args:
            config: Configuración del puente.
        """
        self.config = config or {}
        self.connected_systems = []
        self.operation_history = []
        logger.info("Puente de inversión inicializado", {"config": self.config})
    
    def register_system(self, system_id: str, system_config: Dict[str, Any]) -> bool:
        """
        Registra un sistema de inversión con el puente.
        
        Args:
            system_id: Identificador único del sistema.
            system_config: Configuración del sistema.
            
        Returns:
            bool: True si el registro fue exitoso.
        """
        # Validar que no exista ya
        if any(s.get("id") == system_id for s in self.connected_systems):
            logger.warning(f"Sistema {system_id} ya está registrado")
            return False
        
        # Registrar sistema
        self.connected_systems.append({
            "id": system_id,
            "config": system_config,
            "registered_at": datetime.now().isoformat(),
            "status": "active"
        })
        
        logger.info(f"Sistema {system_id} registrado exitosamente", 
                  {"system_id": system_id, "config": system_config})
        return True
    
    def transfer_capital(
        self, 
        source_system_id: str, 
        target_system_id: str,
        amount: float,
        strategy_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Transfiere capital entre sistemas registrados.
        
        Args:
            source_system_id: Sistema de origen.
            target_system_id: Sistema de destino.
            amount: Cantidad a transferir.
            strategy_params: Parámetros de estrategia para la transferencia.
            
        Returns:
            Dict: Resultado de la transferencia.
        """
        operation_id = logger.start_operation(
            "transfer_capital",
            {
                "source": source_system_id,
                "target": target_system_id,
                "amount": amount,
                "strategy": strategy_params
            }
        )
        
        try:
            # Validar sistemas
            source = next((s for s in self.connected_systems if s["id"] == source_system_id), None)
            target = next((s for s in self.connected_systems if s["id"] == target_system_id), None)
            
            if not source or not target:
                missing = []
                if not source:
                    missing.append(source_system_id)
                if not target:
                    missing.append(target_system_id)
                raise InvestmentError(
                    f"Sistemas no registrados: {', '.join(missing)}",
                    {"missing_systems": missing}
                )
            
            # Validar cantidad
            if amount <= 0:
                raise InvestmentError(
                    "La cantidad de transferencia debe ser positiva",
                    {"amount": amount}
                )
            
            # Simular transferencia (aquí iría la lógica real)
            transfer_result = {
                "operation_id": operation_id,
                "status": "completed",
                "source_system": source_system_id,
                "target_system": target_system_id,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "strategy_applied": strategy_params or {}
            }
            
            # Registrar en historial
            self.operation_history.append(transfer_result)
            
            logger.end_operation(operation_id, "transfer_capital", {"status": "success"})
            return transfer_result
            
        except Exception as e:
            error_result = handle_error(e)
            logger.end_operation(
                operation_id, 
                "transfer_capital", 
                {"status": "error", "error": error_result}
            )
            return {"error": True, "details": error_result}

def bridge_function():
    """Función principal del puente de inversión (compatibilidad)."""
    print("Función del puente de inversión")
    return InvestmentBridge()

if __name__ == "__main__":
    bridge_function()