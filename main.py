"""Inicia EulerLab V2."""

import sys

from PySide6.QtWidgets import QApplication

from interfaz.ventana_principal import VentanaPrincipal


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("EulerLab")
    ventana = VentanaPrincipal()
    ventana.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
