"""Punto de entrada para Posit Connect Cloud: carga el tablero de la carpeta dashboard."""

import importlib.util
import sys
from pathlib import Path

CARPETA = Path(__file__).resolve().parent / "dashboard"
sys.path.insert(0, str(CARPETA))

# Carga dashboard/app.py como módulo propio para que Dash encuentre sus estilos
especificacion = importlib.util.spec_from_file_location("tablero", CARPETA / "app.py")
tablero = importlib.util.module_from_spec(especificacion)
sys.modules["tablero"] = tablero
especificacion.loader.exec_module(tablero)

app = tablero.app
server = tablero.server

if __name__ == "__main__":
    app.run(debug=False, port=8050)
