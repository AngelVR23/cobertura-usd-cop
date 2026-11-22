"""Descarga de las series del proyecto y copia en CSV dentro de datos/crudos."""

import io
import subprocess
import time
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

CARPETA = Path(__file__).resolve().parent / "crudos"
CARPETA.mkdir(parents=True, exist_ok=True)
INICIO = "2015-01-01"

# Tickers de Yahoo Finance y nombre de columna en español
TICKERS = {
    "COP=X": "usdcop_yahoo",
    "BZ=F": "brent",
    "CL=F": "wti",
    "EC": "ecopetrol_adr",
    "DX-Y.NYB": "indice_dolar",
    "^GSPC": "sp500",
    "GC=F": "oro",
}

# Series del BIS (tasas de política e inflación anual)
SERIES_BIS = {
    "tasa_banrep": "WS_CBPOL/M.CO",
    "tasa_fed": "WS_CBPOL/M.US",
    "inflacion_col": "WS_LONG_CPI/M.CO.771",
    "inflacion_eeuu": "WS_LONG_CPI/M.US.771",
}

# Series opcionales de FRED
SERIES_FRED = {"fedfunds": "FEDFUNDS", "tbill_3m": "DTB3"}


def descargar_yahoo():
    """Precios de cierre diarios de Yahoo Finance."""
    datos = yf.download(list(TICKERS), start=INICIO, progress=False, auto_adjust=False)
    cierre = datos["Close"].rename(columns=TICKERS)
    cierre.index.name = "fecha"
    cierre.to_csv(CARPETA / "yahoo_cierres.csv")
    return cierre


def descargar_trm():
    """TRM oficial histórica de datos.gov.co (Superfinanciera)."""
    url = "https://www.datos.gov.co/resource/32sa-8pi3.csv"
    params = {"$limit": 50000, "$order": "vigenciadesde ASC"}
    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    trm = pd.read_csv(io.StringIO(r.text))
    trm.to_csv(CARPETA / "trm_datosgov.csv", index=False)
    return trm


def leer_url_curl(url):
    """Lee un CSV con curl, que responde mejor que requests en estos servidores."""
    salida = subprocess.run(["curl", "-s", "-m", "120", "-A", "Mozilla/5.0", url],
                            capture_output=True, text=True, encoding="utf-8")
    return salida.stdout


def descargar_bis():
    """Tasas de política monetaria e inflación anual del BIS."""
    tablas = []
    for nombre, clave in SERIES_BIS.items():
        texto = leer_url_curl(f"https://stats.bis.org/api/v1/data/{clave}?format=csv&startPeriod=2014-01")
        df = pd.read_csv(io.StringIO(texto))[["TIME_PERIOD", "OBS_VALUE"]]
        df.columns = ["mes", nombre]
        tablas.append(df.set_index("mes"))
        time.sleep(1)
    bis = pd.concat(tablas, axis=1).sort_index()
    bis.to_csv(CARPETA / "bis_tasas_inflacion.csv")
    return bis


def descargar_fred():
    """Series opcionales de FRED; si el servidor bloquea se deja constancia."""
    tablas = []
    for nombre, clave in SERIES_FRED.items():
        texto = leer_url_curl(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={clave}")
        if not texto.startswith("observation_date"):
            print(f"  FRED no respondió para {clave}")
            continue
        df = pd.read_csv(io.StringIO(texto))
        df.columns = ["fecha", nombre]
        tablas.append(df.set_index("fecha"))
        time.sleep(5)
    if tablas:
        fred = pd.concat(tablas, axis=1)
        fred = fred[fred.index >= "2014-01-01"]
        fred.to_csv(CARPETA / "fred_tasas_eeuu.csv")
        return fred
    return None


def resumir(nombre, df):
    """Imprime rango de fechas, nulos y últimas filas."""
    print(f"\n=== {nombre} ===")
    print(f"Filas: {len(df):,}  Desde: {df.index.min()}  Hasta: {df.index.max()}")
    print("Nulos por columna:", df.isna().sum().to_dict())
    print(df.tail(3).to_string())


if __name__ == "__main__":
    resumir("Yahoo Finance", descargar_yahoo())
    trm = descargar_trm()
    resumir("TRM datos.gov.co", trm.set_index("vigenciadesde")[["valor"]])
    resumir("BIS", descargar_bis())
    fred = descargar_fred()
    if fred is not None:
        resumir("FRED", fred)
