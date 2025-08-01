"""
validation.py
Funciones para validar entradas en las operaciones principales.
"""

def validate_investment_params(capital, moneda=None, preferencias=None):
    """
    Valida parámetros comunes de inversión.
    
    Args:
        capital (float): Capital a invertir.
        moneda (str, opcional): Moneda del capital.
        preferencias (dict, opcional): Preferencias de inversión.
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not isinstance(capital, (int, float)):
        return False, "El capital debe ser un número"
        
    if capital <= 0:
        return False, "El capital debe ser positivo"
        
    if moneda and not isinstance(moneda, str):
        return False, "La moneda debe ser una cadena de texto"
        
    if preferencias and not isinstance(preferencias, dict):
        return False, "Las preferencias deben ser un diccionario"
        
    return True, ""
    
def validate_autoinversion_params(perfil_riesgo, porcentaje_ganancia_reventa, tolerancia_perdida):
    """
    Valida parámetros específicos de autoinversión.
    
    Args:
        perfil_riesgo (str): Perfil de riesgo.
        porcentaje_ganancia_reventa (float): Porcentaje para reventa.
        tolerancia_perdida (float): Tolerancia a pérdidas.
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    perfiles_validos = ["bajo", "moderado", "alto"]
    if perfil_riesgo not in perfiles_validos:
        return False, f"Perfil de riesgo debe ser uno de: {', '.join(perfiles_validos)}"
        
    if not isinstance(porcentaje_ganancia_reventa, (int, float)) or porcentaje_ganancia_reventa <= 0:
        return False, "El porcentaje de ganancia debe ser un número positivo"
        
    if not isinstance(tolerancia_perdida, (int, float)) or tolerancia_perdida <= 0:
        return False, "La tolerancia a pérdidas debe ser un número positivo"
        
    return True, ""