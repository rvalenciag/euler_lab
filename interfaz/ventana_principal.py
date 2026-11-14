"""Ventana única de EulerLab. Aquí se conectan los botones con la lógica."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSpinBox, QSplitter, QVBoxLayout, QWidget

from interfaz.grafica import Grafica
from interfaz.tabla import TablaIteraciones, TablaResumen
from logica.casos import CASOS
from logica.errores import agregar_errores
from logica.expresiones import crear_funcion_edo, crear_funcion_exacta
from logica.metodos import calcular_euler_mejorado, calcular_euler_simple


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EulerLab — Métodos Numéricos para EDO")
        self.setMinimumSize(1050, 720)
        self.resize(1500, 900)
        self.crear_interfaz()
        self.cargar_estilos()
        self.calcular()  # Muestra un ejemplo útil al abrir, sin marcar ningún caso.

    def crear_interfaz(self):
        raiz = QWidget()
        raiz.setObjectName("root")
        self.setCentralWidget(raiz)
        layout_raiz = QVBoxLayout(raiz)
        layout_raiz.setContentsMargins(16, 10, 16, 16)
        layout_raiz.setSpacing(10)

        encabezado = QHBoxLayout()
        encabezado.addWidget(QLabel("▣  EulerLab — Métodos Numéricos para EDO", objectName="appTitle"))
        encabezado.addStretch()
        encabezado.addWidget(QLabel("Euler simple · Euler mejorado (Heun)", objectName="appSubtitle"))
        layout_raiz.addLayout(encabezado)

        divisor = QSplitter(Qt.Orientation.Horizontal)
        divisor.setChildrenCollapsible(False)
        layout_raiz.addWidget(divisor, 1)

        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout(panel_izquierdo)
        layout_izquierdo.setContentsMargins(0, 0, 0, 0)
        layout_izquierdo.setSpacing(14)
        layout_izquierdo.addWidget(self.crear_panel_parametros())
        layout_izquierdo.addWidget(self.crear_panel_casos(), 1)
        divisor.addWidget(panel_izquierdo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout(panel_derecho)
        layout_derecho.setContentsMargins(0, 0, 0, 0)
        layout_derecho.setSpacing(12)
        self.grafica = Grafica()
        self.grafica.setMinimumHeight(360)
        self.resumen = TablaResumen()
        self.iteraciones = TablaIteraciones()
        layout_derecho.addWidget(self.grafica, 3)
        layout_derecho.addWidget(self.resumen)
        layout_derecho.addWidget(self.iteraciones, 2)
        scroll.setWidget(panel_derecho)
        divisor.addWidget(scroll)
        divisor.setSizes([405, 1000])
        divisor.setStretchFactor(1, 1)

    def crear_panel_parametros(self):
        panel = QFrame()
        panel.setObjectName("parametersPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(QLabel("⚙  Parámetros del problema", objectName="panelTitle"))

        formulario = QFormLayout()
        formulario.setSpacing(9)
        self.entrada_ecuacion = self.crear_entrada("x + y", "Ej.: x + y, sin(x), -15*y")
        self.entrada_x0 = self.crear_entrada("0")
        self.entrada_y0 = self.crear_entrada("0")
        self.entrada_h = self.crear_entrada("0.2")
        self.entrada_xf = self.crear_entrada("2")
        self.entrada_exacta = self.crear_entrada("exp(x) - x - 1", "Opcional")
        self.entrada_decimales = QSpinBox()
        self.entrada_decimales.setRange(0, 15)
        self.entrada_decimales.setValue(6)
        self.entrada_decimales.setToolTip("Solo cambia cómo se muestran los números.")
        formulario.addRow("f(x,y) =", self.entrada_ecuacion)
        formulario.addRow("x₀ =", self.entrada_x0)
        formulario.addRow("y₀ =", self.entrada_y0)
        formulario.addRow("h =", self.entrada_h)
        formulario.addRow("x_f =", self.entrada_xf)
        formulario.addRow("Solución exacta\n(opcional)", self.entrada_exacta)
        formulario.addRow("Decimales =", self.entrada_decimales)
        layout.addLayout(formulario)

        botones = QHBoxLayout()
        calcular = QPushButton("▷  Calcular")
        calcular.setObjectName("calculateButton")
        calcular.clicked.connect(self.calcular)
        limpiar = QPushButton("↻  Limpiar")
        limpiar.setObjectName("clearButton")
        limpiar.clicked.connect(self.limpiar)
        botones.addWidget(calcular, 3)
        botones.addWidget(limpiar, 2)
        layout.addLayout(botones)
        return panel

    def crear_entrada(self, texto, sugerencia=""):
        entrada = QLineEdit(texto)
        entrada.setPlaceholderText(sugerencia)
        return entrada

    def crear_panel_casos(self):
        panel = QFrame()
        panel.setObjectName("casesPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(QLabel("⚗  Casos de estudio", objectName="panelTitle"))
        texto = QLabel("Explora ejemplos predefinidos para estudiar el comportamiento y la precisión del método.")
        texto.setObjectName("mutedText")
        texto.setWordWrap(True)
        layout.addWidget(texto)
        for nombre, caso in CASOS.items():
            boton = QPushButton(f"{caso['titulo']}\n{caso['descripcion']}")
            boton.setObjectName("caseButton")
            boton.setMinimumHeight(70)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.clicked.connect(lambda _=False, nombre_caso=nombre: self.cargar_caso(nombre_caso))
            layout.addWidget(boton)
        layout.addStretch()
        return panel

    def obtener_datos(self):
        """Lee los QLineEdit y los devuelve en un diccionario sencillo."""
        try:
            return {
                "ecuacion": self.entrada_ecuacion.text().strip(),
                "x0": float(self.entrada_x0.text()),
                "y0": float(self.entrada_y0.text()),
                "h": float(self.entrada_h.text()),
                "xf": float(self.entrada_xf.text()),
                "exacta": self.entrada_exacta.text().strip(),
                "decimales": self.entrada_decimales.value(),
            }
        except ValueError as error:
            raise ValueError("x₀, y₀, h y x_f deben ser números válidos.") from error

    def cargar_caso(self, nombre):
        """Rellena los campos; el botón no queda marcado después del clic."""
        caso = CASOS[nombre]
        self.entrada_ecuacion.setText(caso["ecuacion"])
        self.entrada_x0.setText(str(caso["x0"]))
        self.entrada_y0.setText(str(caso["y0"]))
        self.entrada_h.setText(str(caso["h"]))
        self.entrada_xf.setText(str(caso["xf"]))
        self.entrada_exacta.setText(caso["exacta"])
        self.calcular()

    def calcular(self):
        try:
            datos = self.obtener_datos()
            funcion_edo = crear_funcion_edo(datos["ecuacion"])
            funcion_exacta = crear_funcion_exacta(datos["exacta"]) if datos["exacta"] else None
            euler = calcular_euler_simple(funcion_edo, datos["x0"], datos["y0"], datos["h"], datos["xf"])
            heun = calcular_euler_mejorado(funcion_edo, datos["x0"], datos["y0"], datos["h"], datos["xf"])
            agregar_errores(heun, funcion_exacta)
            exacta_final = funcion_exacta(datos["xf"]) if funcion_exacta else None
        except (ValueError, ArithmeticError) as error:
            QMessageBox.warning(self, "No se pudo calcular", str(error))
            return

        self.grafica.actualizar(euler, heun, funcion_exacta, datos)
        self.resumen.actualizar(euler, heun, exacta_final, datos["decimales"])
        self.iteraciones.actualizar(heun, datos["decimales"])

    def limpiar(self):
        for entrada in (self.entrada_ecuacion, self.entrada_x0, self.entrada_y0, self.entrada_h, self.entrada_xf, self.entrada_exacta):
            entrada.clear()
        self.entrada_decimales.setValue(6)
        self.grafica.limpiar()
        self.resumen.limpiar()
        self.iteraciones.limpiar()
        self.entrada_ecuacion.setFocus()

    def cargar_estilos(self):
        archivo = Path(__file__).with_name("estilos.qss")
        QApplication.instance().setStyleSheet(archivo.read_text(encoding="utf-8"))
