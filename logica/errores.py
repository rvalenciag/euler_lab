"""Funciones pequeñas para comparar con una solución analítica."""

import math


def error_absoluto(aproximado, exacto):
    return abs(aproximado - exacto)


def error_relativo(aproximado, exacto):
    """Devuelve porcentaje; no existe si el valor exacto es cero."""
    if math.isclose(exacto, 0.0, abs_tol=1e-15):
        return None
    return error_absoluto(aproximado, exacto) / abs(exacto) * 100


def agregar_errores(iteraciones, funcion_exacta):
    """Añade exacta, error absoluto y relativo a cada fila de Heun."""
    if funcion_exacta is None:
        return
    for fila in iteraciones:
        exacta = funcion_exacta(fila["x"])
        fila["exacta"] = exacta
        fila["error_absoluto"] = error_absoluto(fila["corregido"], exacta)
        fila["error_relativo"] = error_relativo(fila["corregido"], exacta)
