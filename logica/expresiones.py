"""Convierte texto matemático limitado en funciones de Python seguras."""

import math
import re

import sympy as sp


FUNCIONES_PERMITIDAS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "exp": sp.exp, "log": sp.log, "ln": sp.log,
    "sqrt": sp.sqrt, "abs": sp.Abs, "pi": sp.pi, "e": sp.E,
}


def crear_funcion(texto, usa_y):
    """Acepta solo fórmulas conocidas, como x+y o exp(x)-x-1."""
    texto = texto.strip().replace("^", "**")
    if not texto:
        raise ValueError("La expresión no puede estar vacía.")
    if len(texto) > 300 or not re.fullmatch(r"[0-9A-Za-z+\-*/^().,\s]+", texto):
        raise ValueError("La expresión contiene caracteres no permitidos.")

    variables = {"x"}
    if usa_y:
        variables.add("y")
    nombres_en_texto = set(re.findall(r"[A-Za-z]+", texto))
    nombres_permitidos = variables | set(FUNCIONES_PERMITIDAS)
    desconocidos = nombres_en_texto - nombres_permitidos
    if desconocidos:
        raise ValueError(f"Símbolo o función no admitida: {', '.join(sorted(desconocidos))}.")

    simbolos = {nombre: sp.Symbol(nombre, real=True) for nombre in variables}
    try:
        expresion = sp.sympify(texto, locals={**FUNCIONES_PERMITIDAS, **simbolos})
        funcion_sympy = sp.lambdify(tuple(simbolos[nombre] for nombre in sorted(variables)), expresion, modules=["math"])
    except (sp.SympifyError, SyntaxError, TypeError, ValueError) as error:
        raise ValueError("No se pudo interpretar la expresión matemática.") from error

    def evaluar(x, y=None):
        try:
            if usa_y:
                valor = float(funcion_sympy(x, y))
            else:
                valor = float(funcion_sympy(x))
        except (ValueError, ZeroDivisionError, OverflowError, TypeError) as error:
            raise ValueError("La expresión no está definida para uno de los valores calculados.") from error
        if not math.isfinite(valor):
            raise ValueError("La expresión produjo un valor no finito.")
        return valor

    return evaluar


def crear_funcion_edo(texto):
    return crear_funcion(texto, usa_y=True)


def crear_funcion_exacta(texto):
    return crear_funcion(texto, usa_y=False)
