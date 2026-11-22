# Cobertura cambiaria USD/COP para una importadora de Cartagena

Proyecto final de Toma de decisiones basadas en datos (UTB).
Integrantes: Angel Vega Rodríguez (T00068186), Germán De Armas (T00068765), María Valentina Serna (T00067756), Luis Mario Díaz (T00069220) y Daniel Castillo (T00091828).

La pregunta es si una importadora que paga en dólares a 3 o 6 meses debe fijar hoy la tasa con un forward y qué porcentaje del pago conviene cubrir.

Tablero publicado: https://01a2057d-f00e-0325-72e3-2329520e3b87.share.connect.posit.cloud/

## Estructura

```
datos/
  descargar_datos.py      descarga TRM, Yahoo Finance, BIS y FRED a CSV
  crudos/                 copias de las descargas
  limpios/                paneles diario y mensual después del ETL
notebook/
  analisis_cobertura.ipynb   ETL, EDA, regresión, GJR-GARCH, Monte Carlo, tornado, backtest y recomendación
resultados/
  resultados.json         todas las cifras que usan el documento y el tablero
documento/
  documento_tecnico.qmd   documento técnico (portada, índice y 4 páginas de contenido)
  estilo.typ, logos/      diseño del PDF y logos de la UTB y la Escuela
  documento_tecnico.pdf   versión compilada
  figuras/                gráficas exportadas por el notebook
dashboard/
  app.py, calculos.py     tablero en Dash (modo claro y oscuro)
  assets/estilos.css      estilo visual
  datos/                  archivos que exporta el notebook para el tablero
  requirements.txt        dependencias para Posit Connect Cloud
presentacion/             diapositivas (pendiente)
```

## Cómo reproducir todo

El entorno virtual está en `C:\Users\angel\venvs\cobertura` porque la ruta de OneDrive es demasiado larga para instalar Jupyter dentro del proyecto. Para crearlo en otro equipo:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements-notebook.txt
.\venv\Scripts\python.exe -m ipykernel install --user --name cobertura
```

Orden de ejecución:

1. `python datos\descargar_datos.py` (solo si se quieren datos nuevos; los CSV ya están guardados).
2. Ejecutar `notebook\analisis_cobertura.ipynb` de principio a fin. Escribe las figuras, `resultados.json` y los datos del tablero.
3. Compilar el documento con `quarto render documento\documento_tecnico.qmd` (con `QUARTO_PYTHON` apuntando al Python del entorno).
4. Abrir el tablero con `python dashboard\app.py` y entrar a http://localhost:8050.

La simulación usa 10.000 escenarios y semilla 42, así que los resultados son idénticos en cada ejecución.

## Despliegue en Posit Connect Cloud

1. Subir el proyecto a un repositorio de GitHub (la carpeta `dashboard/` debe incluir `datos/` y `assets/`).
2. En connect.posit.cloud elegir **Publish → Dash**, seleccionar el repositorio y la rama.
3. Archivo principal `app.py` (en la raíz, carga el tablero de `dashboard/`). Posit instala las librerías de `requirements.txt`.
4. Publicar y compartir el enlace.
