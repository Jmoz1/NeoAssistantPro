"""
logger.py
Sistema avanzado de logging para Neoproyectto.
"""
import logging
import json
import time
import uuid
from typing import Dict, Any, Optional, Union

class NeoproyecttoLogger:
    """
    Logger personalizado para el proyecto Neoproyectto.
    Provee logging estructurado y capacidades avanzadas.
    """
    
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.request_id = str(uuid.uuid4())
        
        # Configuración para asegurar que solo hay un handler
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log(self, level: int, message: str, data: Optional[Dict[str, Any]] = None, 
             exception: Optional[Exception] = None, request_id: Optional[str] = None):
        """
        Método interno para manejar los logs con formato estructurado.
        """
        log_data = {
            "message": message,
            "timestamp": time.time(),
            "request_id": request_id or self.request_id
        }
        
        if data:
            log_data["data"] = data
            
        if exception:
            log_data["exception"] = str(exception)
            log_data["exception_type"] = exception.__class__.__name__
        
        # Convertir a JSON para logging estructurado
        log_message = f"{message} - {json.dumps(log_data)}"
        self.logger.log(level, log_message)
    
    def info(self, message: str, data: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None):
        """Log a nivel INFO."""
        self._log(logging.INFO, message, data, request_id=request_id)
    
    def warning(self, message: str, data: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None):
        """Log a nivel WARNING."""
        self._log(logging.WARNING, message, data, request_id=request_id)
    
    def error(self, message: str, data: Optional[Dict[str, Any]] = None, 
              exception: Optional[Exception] = None, request_id: Optional[str] = None):
        """Log a nivel ERROR."""
        self._log(logging.ERROR, message, data, exception, request_id=request_id)
    
    def critical(self, message: str, data: Optional[Dict[str, Any]] = None, 
                exception: Optional[Exception] = None, request_id: Optional[str] = None):
        """Log a nivel CRITICAL."""
        self._log(logging.CRITICAL, message, data, exception, request_id=request_id)
    
    def start_operation(self, operation_name: str, data: Optional[Dict[str, Any]] = None) -> str:
        """Inicia el registro de una operación y devuelve un ID de operación."""
        operation_id = str(uuid.uuid4())
        self.info(
            f"Iniciando operación: {operation_name}",
            data={"operation_id": operation_id, "operation": operation_name, **data} if data else {"operation_id": operation_id, "operation": operation_name}
        )
        return operation_id
    
    def end_operation(self, operation_id: str, operation_name: str, result: Optional[Union[Dict[str, Any], str]] = None):
        """Registra la finalización de una operación."""
        self.info(
            f"Finalizando operación: {operation_name}",
            data={"operation_id": operation_id, "operation": operation_name, "result": result} if result else {"operation_id": operation_id, "operation": operation_name}
        )