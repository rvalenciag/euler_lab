"""Ejemplos que rellenan el formulario al presionarlos."""

CASOS = {
    "convergencia": {
        "titulo": "Convergencia",
        "descripcion": "y' = x + y · crecimiento suave",
        "ecuacion": "x + y", "x0": 0, "y0": 0, "h": 0.2, "xf": 2,
        "exacta": "exp(x) - x - 1",
    },
    "oscilatorio": {
        "titulo": "Oscilatorio",
        "descripcion": "y' = cos(x) · solución senoidal",
        "ecuacion": "cos(x)", "x0": 0, "y0": 0, "h": 0.2,
        "xf": 6.283185307179586, "exacta": "sin(x)",
    },
    "estabilidad": {
        "titulo": "Estabilidad",
        "descripcion": "y' = -15y · paso grande",
        "ecuacion": "-15*y", "x0": 0, "y0": 1, "h": 0.15, "xf": 1.5,
        "exacta": "exp(-15*x)",
    },
}
