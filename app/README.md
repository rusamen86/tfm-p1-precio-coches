# 🚗 Tasador de coches de ocasión (dashboard)

Herramienta local en Streamlit para un concesionario ficticio (Seat). Usa el Random Forest entrenado en el TFM para tasar un coche y calcular la oferta de compra. Es una aportación adicional al proyecto: no forma parte de la hoja de ruta de cuadernos y no los modifica.

## Qué hay en esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `dashboard.py` | El dashboard: formulario, tasación, oferta, avisos y explicación con SHAP |
| `arrancar.command` | Lanzador para macOS: doble clic y se abre el dashboard en el navegador |
| `README.md` | Esta guía |

## Qué necesita

- El entorno virtual del proyecto con las dependencias instaladas (`pip install -r requirements.txt` desde la raíz).
- Tres archivos que generan los cuadernos (los dos primeros no se suben a GitHub):
  - `models/random_forest.joblib` (04_modelado)
  - `data/processed/coches_limpio.csv` (02_limpieza)
  - `outputs/metricas_random_forest.csv` (04_modelado)

Si faltan, hay que ejecutar antes los cuadernos en orden, como explica el README principal.

## Cómo arrancarlo

**Opción 1, doble clic (macOS):** abrir `arrancar.command` desde Finder.

**Opción 2, terminal**, desde la raíz del proyecto:

```bash
source .venv/bin/activate
streamlit run app/dashboard.py
```

Se abre en http://localhost:8501. Para pararlo, Ctrl + C en la terminal.

## Cómo se usa

1. En la barra lateral, ajustar el **margen** (15 % por defecto) y los **costes de preparación**.
2. Rellenar los datos del coche: marca, modelo, combustible, cambio, vendedor, antigüedad, kilómetros, potencia, puertas y si está en las islas.
3. Pulsar **Calcular tasación**.

## Qué muestra

- **Precio estimado:** la predicción del Random Forest.
- **Rango aproximado:** precio estimado ± el MAE de test (1.816 €). Es orientativo, no un intervalo de confianza.
- **Oferta de compra:** precio estimado × (1 − margen) − costes de preparación.
- **Avisos:** si el coche se sale de los datos de entrenamiento (más de 15 años, más de 940.000 km, potencia fuera de 37-620 CV o un modelo que no estaba en train) y cuándo conviene una revisión manual (más de 12 años o menos de 5.000 €).
- **¿Por qué este precio?:** un gráfico con SHAP que parte del precio de un coche medio y muestra cuánto sube (verde) o baja (rojo) el precio cada característica de ese coche, en porcentaje.

## Limitaciones

- Los precios son de **anuncios de enero de 2021**, no de ventas reales ni actuales.
- La antigüedad se introduce en años porque el modelo aprendió con la antigüedad a esa fecha.
- El preprocesado (las 10 marcas más frecuentes y el target encoding del modelo) no está guardado en disco: el dashboard lo reconstruye al arrancar repitiendo los pasos de 03_preprocesado sobre los datos limpios. El modelo no se reentrena.
