import pytest

from logica.metodos import calcular_euler_mejorado, calcular_euler_simple


def test_heun_sigue_el_predictor_y_corrector_esperados():
    funcion = lambda x, y: 0.4 * x * y
    resultados = calcular_euler_mejorado(funcion, 1, 1, 0.1, 2)

    primera_iteracion = resultados[1]
    assert primera_iteracion["x"] == pytest.approx(1.1)
    assert primera_iteracion["predictor"] == pytest.approx(1.04)
    assert primera_iteracion["corregido"] == pytest.approx(1.04288)
    assert resultados[-1]["corregido"] == pytest.approx(1.821392, abs=1e-6)


def test_el_ultimo_paso_se_ajusta_a_xf():
    resultados = calcular_euler_mejorado(lambda x, y: x + y, 0, 0, 0.3, 1)
    assert [fila["x"] for fila in resultados] == pytest.approx([0, 0.3, 0.6, 0.9, 1])


def test_euler_simple_y_heun_guardan_valores_finales_distintos():
    funcion = lambda x, y: y
    euler = calcular_euler_simple(funcion, 0, 1, 0.5, 1)
    heun = calcular_euler_mejorado(funcion, 0, 1, 0.5, 1)
    assert euler[-1]["y"] == pytest.approx(2.25)
    assert heun[-1]["corregido"] == pytest.approx(2.640625)
