# EulerLab V2

Versión didáctica de EulerLab. Conserva la interfaz y las funciones de la aplicación original, pero usa funciones simples, diccionarios y comentarios en español para facilitar su estudio.

## Estructura

- `main.py`: inicia la aplicación.
- `logica/metodos.py`: Euler simple y Euler mejorado (Heun).
- `logica/expresiones.py`: convierte expresiones como `x + y` en funciones matemáticas seguras.
- `logica/errores.py`: añade solución exacta y errores cuando existe.
- `logica/casos.py`: contiene los casos predefinidos.
- `interfaz/ventana_principal.py`: formulario, botones y conexión con la lógica.
- `interfaz/grafica.py`: gráfica comparativa.
- `interfaz/tabla.py`: resumen y tabla de iteraciones.

## Ejecutar

### Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

### Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

## Heun

El código de `calcular_euler_mejorado()` sigue estos pasos:

```python
k1 = funcion(x_actual, y_actual)
y_predictor = y_actual + paso * k1
x_siguiente = x_actual + paso
k2 = funcion(x_siguiente, y_predictor)
y_corregido = y_actual + (paso / 2) * (k1 + k2)
```

El siguiente ciclo comienza usando `y_corregido`.

## Expresiones permitidas

Variables: `x` y `y` en la EDO; solo `x` en la solución exacta.

Funciones: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `exp`, `log`, `ln`, `sqrt`, `abs`.

Constantes: `pi`, `e`. Se puede escribir potencia con `^` o `**`.

## Pruebas

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```
