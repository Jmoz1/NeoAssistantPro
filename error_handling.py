"""
error_handling.py
Sistema centralizado para manejo de errores.
"""
import logging
from typing import Dict, Any, Type, Optional
import traceback

# Configuración de logging específica para errores
error_logger = logging.getLogger("neoproyectto.errors")

class NeoproyecttoBaseError(Exception):
    """Clase base para errores del proyecto."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)

class ValidationError(NeoproyecttoBaseError):
    """Error de validación de datos de entrada."""
    pass

class InvestmentError(NeoproyecttoBaseError):
    """Error en la lógica de inversión."""
    pass

class ExternalServiceError(NeoproyecttoBaseError):
    """Error al interactuar con servicios externos."""
    pass

class ConfigurationError(NeoproyecttoBaseError):
    """Error en la configuración del sistema."""
    pass

def handle_error(error: Exception, log_traceback: bool = True) -> Dict[str, Any]:
    """
    Maneja un error y genera una respuesta estandarizada.
    
    Args:
        error: La excepción capturada.
        log_traceback: Si se debe registrar el traceback completo.
        
    Returns:
        Dict[str, Any]: Respuesta de error estandarizada.
    """
    if isinstance(error, NeoproyecttoBaseError):
        error_type = error.__class__.__name__
        message = error.message
        details = error.details
        status_code = 400  # Por defecto para errores de validación
        
        if isinstance(error, ExternalServiceError):
            status_code = 502  # Bad Gateway
        elif isinstance(error, ConfigurationError):
            status_code = 500  # Internal Server Error
    else:
        error_type = "UnexpectedError"
        message = str(error)
        details = {}
        status_code = 500
    
    if log_traceback:
        error_logger.error(
            f"Error {error_type}: {message}", 
            exc_info=True
        )
    else:
        error_logger.error(f"Error {error_type}: {message}")
    
    return {
        "error": True,
        "type": error_type,
        "message": message,
        "details": details,
        "status_code": status_code
    }