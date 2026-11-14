"""Métodos numéricos escritos de forma directa para fines didácticos."""

import math


MAX_ITERACIONES = 100_000


def validar_parametros(x0, y0, h, xf):
    """Comprueba que el intervalo y el tamaño de paso sean utilizables."""
    if not all(math.isfinite(valor) for valor in (x0, y0, h, xf)):
        raise ValueError("x₀, y₀, h y x_f deben ser números finitos.")
    if h == 0:
        raise ValueError("El tamaño de paso h debe ser distinto de cero.")
    if x0 != xf and (xf - x0) * h < 0:
        raise ValueError("El signo de h debe avanzar desde x₀ hasta x_f.")
    pasos_estimados = math.ceil(abs((xf - x0) / h))
    if pasos_estimados > MAX_ITERACIONES:
        raise ValueError(f"El cálculo superaría {MAX_ITERACIONES:,} iteraciones.")


def siguiente_paso(x_actual, h, xf):
    """Devuelve h, excepto en el último tramo, donde evita pasar x_f."""
    distancia_restante = xf - x_actual
    direccion = 1 if h > 0 else -1
    return direccion * min(abs(h), abs(distancia_restante))


def calcular_euler_simple(funcion, x0, y0, h, xf):
    """Calcula Euler simple y devuelve una lista de filas para la interfaz."""
    validar_parametros(x0, y0, h, xf)
    resultados = [{"n": 0, "x": x0, "y": y0}]
    x_actual = x0
    y_actual = y0
    numero = 0
    direccion = 1 if xf >= x0 else -1

    while direccion * (xf - x_actual) > 1e-12 * max(1, abs(xf)):
        paso = siguiente_paso(x_actual, h, xf)
        pendiente = funcion(x_actual, y_actual)
        y_actual = y_actual + paso * pendiente
        x_actual = x_actual + paso
        numero += 1
        if not math.isfinite(y_actual):
            raise ValueError("Euler simple produjo un valor no finito.")
        resultados.append({"n": numero, "x": x_actual, "y": y_actual})

    # Evita que el redondeo binario muestre 1.999999999999 en lugar de 2.
    resultados[-1]["x"] = xf
    return resultados


def calcular_euler_mejorado(funcion, x0, y0, h, xf):
    """Calcula Heun: predictor de Euler y corrector con promedio de pendientes."""
    validar_parametros(x0, y0, h, xf)
    resultados = [{"n": 0, "x": x0, "predictor": None, "corregido": y0}]
    x_actual = x0
    y_actual = y0
    numero = 0
    direccion = 1 if xf >= x0 else -1

    while direccion * (xf - x_actual) > 1e-12 * max(1, abs(xf)):
        paso = siguiente_paso(x_actual, h, xf)

        # 1. Pendiente en el punto actual: k₁ = f(xₙ, yₙ)
        k1 = funcion(x_actual, y_actual)

        # 2. Predictor  y* = yₙ + h·k₁
        y_predictor = y_actual + paso * k1

        #3. Calcular sgte x
        x_siguiente = x_actual + paso

        # 4. Pendiente usando el predictor: k₂ = f(xₙ₊₁, y*)
        k2 = funcion(x_siguiente, y_predictor)

        # 5. Corrector de Heun: promedio de k₁ y k₂
        y_corregido = y_actual + (paso / 2) * (k1 + k2)
        if not math.isfinite(y_predictor) or not math.isfinite(y_corregido):
            raise ValueError("Euler mejorado produjo un valor no finito.")

        # La siguiente vuelta se parte del valor corregido, nunca del predictor.
        x_actual = x_siguiente
        y_actual = y_corregido
        numero += 1
        resultados.append({
            "n": numero,
            "x": x_actual,
            "predictor": y_predictor,
            "corregido": y_corregido,
        })

    resultados[-1]["x"] = xf
    return resultados
