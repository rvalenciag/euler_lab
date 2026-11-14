"""Gráfica de Matplotlib para comparar los resultados."""

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QFrame, QVBoxLayout


class Grafica(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("chartPanel")
        self.figura = Figure(facecolor="white", layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figura)
        self.ejes = self.figura.add_subplot(111)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 14)
        layout.addWidget(self.canvas)
        self.limpiar()

    def limpiar(self):
        self.ejes.clear()
        self.ejes.text(0.5, 0.5, "Introduce los parámetros y pulsa Calcular", ha="center", va="center", color="#60758f")
        self.ejes.set_axis_off()
        self.canvas.draw_idle()

    def actualizar(self, euler, heun, funcion_exacta, datos):
        self.ejes.clear()
        self.ejes.plot([fila["x"] for fila in euler], [fila["y"] for fila in euler], "o--", color="#1473e6", label="Euler simple", linewidth=1.8, markersize=4)
        self.ejes.plot([fila["x"] for fila in heun], [fila["corregido"] for fila in heun], "s-", color="#f08c1a", label="Euler mejorado", linewidth=2, markersize=4)
        if funcion_exacta:
            valores_x = np.linspace(datos["x0"], datos["xf"], 300)
            valores_y = [funcion_exacta(float(x)) for x in valores_x]
            self.ejes.plot(valores_x, valores_y, color="#0cab72", label="Solución exacta", linewidth=2)
        self.ejes.set_xlabel("x", fontweight="bold")
        self.ejes.set_ylabel("y", fontweight="bold", rotation=0, labelpad=10)
        self.ejes.set_title(f"Solución de la EDO:  y' = {datos['ecuacion']}  ·  [{datos['x0']:g}, {datos['xf']:g}]  ·  h = {datos['h']:g}", color="#4c6384", fontsize=10, pad=14)
        self.ejes.grid(True, color="#dce7f4", linewidth=0.7)
        self.ejes.set_facecolor("#fbfdff")
        self.ejes.spines[["top", "right"]].set_visible(False)
        self.ejes.spines[["bottom", "left"]].set_color("#6583a6")
        self.ejes.tick_params(colors="#476588", labelsize=8)
        self.ejes.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#b7c9e2", fontsize=8)
        self.canvas.draw_idle()
