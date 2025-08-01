# Neoproyectto

**Centro de gestión de inversiones inteligentes.**

Las funciones centrales y punto de partida de Neoproyectto son:

1. **gestionar_inversion_dividendos_mensuales:**  
   Gestiona inversiones optimizadas para obtener dividendos mensuales.

2. **autoinversion_ia_global:**  
   Realiza autoinversión avanzada usando IA y autoaprendizaje, diversificando y seleccionando activos con máxima probabilidad de ganancia.

3. **puente_autoinversion_a_dividendos:**  
   Monitoriza la autoinversión IA y, al alcanzar el capital objetivo, transfiere el capital generado a la gestión de dividendos mensuales, enfocando el sistema en maximizar ganancias pasivas.

> **Cada vez que se analiza este proyecto, estas funciones son el núcleo y el primer punto de referencia.**

---

## Ejemplo de uso

```python
from main import (
    gestionar_inversion_dividendos_mensuales,
    autoinversion_ia_global,
    puente_autoinversion_a_dividendos
)

# Gestión de dividendos mensuales
cartera = gestionar_inversion_dividendos_mensuales(
    capital=10000,
    moneda='EUR',
    preferencias={"sector": "tecnología"}
)

# Autoinversión IA global
resultado = autoinversion_ia_global(
    capital=20000,
    moneda='USD',
    perfil_riesgo='alto',
    preferencias_avanzadas={"sector": "tecnología"},
    porcentaje_ganancia_reventa=12,
    tolerancia_perdida=1.5
)

# Puente entre autoinversión IA y dividendos mensuales
puente = puente_autoinversion_a_dividendos(
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
```

---

## Estructura de módulos

- Todos los archivos se encuentran en el directorio raíz.
- **main.py:** Funciones centrales y punto de entrada.
- **asset_selector.py**
- **diversify.py**
- **currency.py**
- **scraper.py**
- **ai_predictor.py**
- **memoria.py**
- **README.md**

---

**¡Comienza tu análisis o desarrollo por las funciones centrales del proyecto!**