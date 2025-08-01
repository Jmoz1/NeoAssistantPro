"""
api.py
Implementación de API REST para Neoproyectto.
"""
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union
import uvicorn
import json
import time
from datetime import datetime

from logger import NeoproyecttoLogger
from security import authenticate_request
from error_handling import handle_error, ValidationError, NeoproyecttoBaseError
from main import (
    gestionar_inversion_dividendos_mensuales,
    autoinversion_ia_global,
    puente_autoinversion_a_dividendos
)

app = FastAPI(
    title="Neoproyectto API",
    description="API para el centro de gestión de inversiones inteligentes",
    version="1.0.0",
)

# Inicializar logger
logger = NeoproyecttoLogger("neoproyectto.api")

# Modelos para API
class InversionDividendosRequest(BaseModel):
    capital: float = Field(..., gt=0, description="Capital disponible para invertir")
    moneda: str = Field("EUR", description="Moneda del capital")
    preferencias: Optional[Dict[str, Any]] = Field(None, description="Preferencias de inversión")

class AutoinversionRequest(BaseModel):
    capital: float = Field(..., gt=0, description="Capital disponible para invertir")
    moneda: str = Field("EUR", description="Moneda del capital")
    perfil_riesgo: str = Field("moderado", description="Perfil de riesgo (bajo, moderado, alto)")
    preferencias_avanzadas: Optional[Dict[str, Any]] = Field(None, description="Preferencias avanzadas")
    porcentaje_ganancia_reventa: float = Field(10.0, gt=0, description="Porcentaje para reventa")
    tolerancia_perdida: float = Field(1.5, gt=0, description="Tolerancia a pérdidas")

class PuenteRequest(BaseModel):
    capital_minimo_activacion: float = Field(..., gt=0, description="Capital mínimo para activación")
    capital_objetivo: float = Field(..., gt=0, description="Capital objetivo")
    args_autoinversion: Dict[str, Any] = Field(..., description="Argumentos para autoinversión")
    args_dividendos: Dict[str, Any] = Field(..., description="Argumentos para dividendos")

# Middleware para logging de solicitudes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de solicitudes HTTP entrantes y sus respuestas."""
    start_time = time.time()
    
    # Generar ID de solicitud
    request_id = f"req_{int(time.time() * 1000)}"
    
    # Log de solicitud entrante
    logger.info(
        f"Solicitud recibida {request.method} {request.url.path}",
        {"request_id": request_id, "method": request.method, "path": request.url.path}
    )
    
    # Procesar la solicitud
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = time.time() - start_time
    
    # Log de respuesta
    logger.info(
        f"Respuesta enviada {response.status_code}",
        {
            "request_id": request_id,
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2)
        }
    )
    
    return response

async def verify_token(authorization: Optional[str] = Header(None)):
    """Verifica el token de autorización."""
    if not authorization:
        raise HTTPException(status_code=401, detail="No se proporcionó token de autorización")
    
    # Formato esperado: "Bearer {token}"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema de autorización inválido")
    except ValueError:
        raise HTTPException(status_code=401, detail="Formato de autorización inválido")
    
    is_valid, user_info = authenticate_request(token)
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    return user_info

@app.get("/")
async def root():
    """Endpoint raíz de la API."""
    return {
        "app": "Neoproyectto API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/dividendos")
async def api_dividendos(
    request: InversionDividendosRequest, 
    user_info: Dict[str, Any] = Depends(verify_token)
):
    """Endpoint para gestionar inversión en dividendos."""
    operation_id = logger.start_operation(
        "api_dividendos", 
        {"user": user_info["id"], "request": request.dict()}
    )
    
    try:
        result = gestionar_inversion_dividendos_mensuales(
            capital=request.capital,
            moneda=request.moneda,
            preferencias=request.preferencias
        )
        
        if "error" in result:
            logger.error("Error en gestión de dividendos", {"error": result["error"]})
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.end_operation(operation_id, "api_dividendos", {"status": "success"})
        return result
        
    except NeoproyecttoBaseError as e:
        error_response = handle_error(e)
        logger.end_operation(
            operation_id, 
            "api_dividendos", 
            {"status": "error", "error": error_response}
        )
        raise HTTPException(
            status_code=error_response["status_code"], 
            detail=error_response
        )
    except Exception as e:
        error_response = handle_error(e)
        logger.end_operation(
            operation_id, 
            "api_dividendos", 
            {"status": "error", "error": error_response}
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/autoinversion")
async def api_autoinversion(
    request: AutoinversionRequest, 
    user_info: Dict[str, Any] = Depends(verify_token)
):
    """Endpoint para autoinversión con IA."""
    operation_id = logger.start_operation(
        "api_autoinversion", 
        {"user": user_info["id"], "request": request.dict()}
    )
    
    try:
        result = autoinversion_ia_global(
            capital=request.capital,
            moneda=request.moneda,
            perfil_riesgo=request.perfil_riesgo,
            preferencias_avanzadas=request.preferencias_avanzadas,
            porcentaje_ganancia_reventa=request.porcentaje_ganancia_reventa,
            tolerancia_perdida=request.tolerancia_perdida
        )
        
        if "error" in result:
            logger.error("Error en autoinversión", {"error": result["error"]})
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.end_operation(operation_id, "api_autoinversion", {"status": "success"})
        return result
        
    except NeoproyecttoBaseError as e:
        error_response = handle_error(e)
        logger.end_operation(
            operation_id, 
            "api_autoinversion", 
            {"status": "error", "error": error_response}
        )
        raise HTTPException(
            status_code=error_response["status_code"], 
            detail=error_response
        )
    except Exception as e:
        error_response = handle_error(e)
        logger.end_operation(
            operation_id, 
            "api_autoinversion", 
            {"status": "error", "error": error_response}
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/puente")
async def api_puente(
    request: PuenteRequest, 
    user_info: Dict[str, Any] = Depends(verify_token)
):
    """Endpoint para el puente entre autoinversión y dividendos."""
    operation_id = logger.start_operation(
        "api_puente", 
        {"user": user_info["id"], "request": request.dict()}
    )
    
    try:
        result = puente_autoinversion_a_dividendos(
            capital_minimo_activacion=request.capital_minimo_activacion,
            capital_objetivo=request.capital_objetivo,
            args_autoinversion=request.args_autoinversion,
            args_dividendos=request.args_dividendos
        )
        
        if "error" in result:
            logger.error("Error en puente", {"error": result["error"]})
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.end_operation(operation_id, "api_puente", {"status": "success"})
        return result
        
    except NeoproyecttoBaseError as e:
        error_response = handle_error(e)
        logger.end_operation(
            operation_id, 
            "api_puente", 
            {"status": "error", "error": error_response}
        )
        raise HTTPException(
            status_code=error_response["status_code"], 
            detail=error_response
        )
    except Exception as e:
        error_response = handle_error(e)
        logger.end_operation(
            operation_id, 
            "api_puente", 
            {"status": "error", "error": error_response}
        )
        raise HTTPException(status_code=500, detail=str(e))

def api_endpoint():
    """Función de compatibilidad (para scripts antiguos)."""
    print("Endpoint de API")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)