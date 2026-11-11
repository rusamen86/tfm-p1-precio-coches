#!/bin/bash
# Lanzador del dashboard para macOS: doble clic desde Finder.
# Va a la raíz del proyecto, activa el entorno virtual y arranca Streamlit.

cd "$(dirname "$0")/.."
source .venv/bin/activate
streamlit run app/dashboard.py
