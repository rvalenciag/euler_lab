"""Tablas visuales para el resumen y las iteraciones de Heun."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QFrame, QHeaderView, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout


def mostrar_numero(valor, decimales, no_disponible="—", porcentaje=False):
    if valor is None:
        return no_disponible
    texto = f"{valor:.{decimales}f}"
    return texto + " %" if porcentaje else texto


def crear_tabla(encabezados, filas, altura=None):
    tabla = QTableWidget(filas, len(encabezados))
    tabla.setHorizontalHeaderLabels(encabezados)
    tabla.verticalHeader().setVisible(False)
    tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    tabla.setShowGrid(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.horizontalHeader().setMinimumSectionSize(74)
    if altura:
        tabla.setFixedHeight(altura)
        tabla.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    return tabla


class TablaResumen(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("resultsPanel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 12)
        layout.addWidget(QLabel("◎  Resumen de resultados", objectName="summaryTitle"))
        self.tabla = crear_tabla(("Método", "Valor final", "Error absoluto", "Error relativo"), 3, 146)
        self.tabla.setObjectName("summaryTable")
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        layout.addWidget(self.tabla)

    def actualizar(self, euler, heun, exacta_final, decimales):
        valor_euler = euler[-1]["y"]
        valor_heun = heun[-1]["corregido"]
        if exacta_final is None:
            error_euler = error_heun = relativo_euler = relativo_heun = None
        else:
            error_euler = abs(valor_euler - exacta_final)
            error_heun = abs(valor_heun - exacta_final)
            relativo_euler = error_euler / abs(exacta_final) * 100 if exacta_final != 0 else None
            relativo_heun = error_heun / abs(exacta_final) * 100 if exacta_final != 0 else None
        filas = (
            ("Euler simple", valor_euler, error_euler, relativo_euler),
            ("Euler mejorado", valor_heun, error_heun, relativo_heun),
            ("Solución exacta", exacta_final, None, None),
        )
        for fila, valores in enumerate(filas):
            textos = (valores[0], mostrar_numero(valores[1], decimales, "No disponible"), mostrar_numero(valores[2], decimales), mostrar_numero(valores[3], decimales, porcentaje=True))
            for columna, texto in enumerate(textos):
                item = QTableWidgetItem(texto)
                alineacion = Qt.AlignmentFlag.AlignLeft if columna == 0 else Qt.AlignmentFlag.AlignCenter
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | alineacion)
                self.tabla.setItem(fila, columna, item)
        self.tabla.resizeRowsToContents()

    def limpiar(self):
        self.tabla.clearContents()


class TablaIteraciones(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("tablePanel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 14)
        layout.setSpacing(8)
        layout.addWidget(QLabel("▦  Tabla de iteraciones (Euler Mejorado)", objectName="tableTitle"))
        self.tabla = crear_tabla(("n", "xₙ", "yₙ* (predictor)", "yₙ (corregido)", "y exacta", "Eₐ = |y - yᵣ|", "Eᵣ (%)"), 0)
        self.tabla.setMinimumHeight(250)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        layout.addWidget(self.tabla)

    def actualizar(self, iteraciones, decimales):
        self.tabla.setRowCount(len(iteraciones))
        for fila, dato in enumerate(iteraciones):
            valores = (
                str(dato["n"]), mostrar_numero(dato["x"], decimales),
                mostrar_numero(dato["predictor"], decimales), mostrar_numero(dato["corregido"], decimales),
                mostrar_numero(dato.get("exacta"), decimales), mostrar_numero(dato.get("error_absoluto"), decimales),
                mostrar_numero(dato.get("error_relativo"), decimales),
            )
            for columna, texto in enumerate(valores):
                item = QTableWidgetItem(texto)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla.setItem(fila, columna, item)
        self.tabla.resizeRowsToContents()

    def limpiar(self):
        self.tabla.setRowCount(0)
