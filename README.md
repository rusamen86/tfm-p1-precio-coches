# 🚗 TFM Proyecto 1 · Estimador de precio de coches de segunda mano

Modelo predictivo (regresión) que estima el **precio de venta de un coche de segunda mano en España** a partir de los datos de su anuncio (marca, modelo, año, kilómetros, potencia, combustible, cambio, provincia...).

> **Uso previsto:** una **guía de tasación** para una empresa de compraventa de coches usados.

---

## 📑 Tabla de contenidos

1. [Objetivo de negocio](#-objetivo-de-negocio)
2. [Dataset](#-dataset)
3. [Hipótesis previas](#-hipótesis-previas)
4. [Preguntas a responder](#-preguntas-a-responder)
5. [Modelos](#-modelos)
6. [Métricas y KPIs](#-métricas-y-kpis)
7. [Estructura del repositorio](#-estructura-del-repositorio)
8. [Flujo de ramas](#-flujo-de-ramas)
9. [Cómo ejecutar](#️-cómo-ejecutar)
10. [Resultados](#-resultados)
11. [Explicabilidad](#-explicabilidad)
12. [Paso a producción](#-paso-a-producción)
13. [Conclusiones y mejoras](#-conclusiones-y-mejoras)

---

## 🎯 Objetivo de negocio

Una empresa de compraventa de coches usados quiere estimar **a qué precio podrá vender un coche**. Con ese precio y el margen que busca, calcula **cuánto ofrecer al cliente** que viene a venderlo:

```
oferta = precio_estimado × (1 − margen) − costes_de_preparación
```

**¿Qué hace el modelo?** Una regresión que predice `price` a partir de la marca, el modelo, el año, los km, la potencia, el combustible, el cambio y la provincia.

---

## 📊 Dataset

| Característica | Detalle |
|---|---|
| Origen | Muestra gratuita de **DataMarket**: anuncios de una plataforma española de coches de segunda mano (web de origen anonimizada) |
| Tamaño | **50.000** anuncios · **21** columnas |
| Fechas de publicación | Del 09-05-2017 al 15-01-2021 |
| Fecha de captura | 15-01-2021 |
| Variable objetivo | `price` (€) |
| Descarga (CSV) | https://raw.githubusercontent.com/Data-Market/vehiculos-de-segunda-mano/main/coches-de-segunda-mano-sample.csv |
| Repositorio y documentación | https://github.com/Data-Market/vehiculos-de-segunda-mano |
| Dataset completo (de pago) | https://datamarket.es/#coches-de-segunda-mano-dataset |
| Licencia | Muestra de evaluación y uso gratuito (el repositorio no incluye licencia formal) |

⚠️ **Limitación:** son **precios de anuncio**, no precios de venta real.

📁 El CSV (`data/raw/coches_segunda_mano.csv`) **no se sube al repositorio** (`data/raw/` está en `.gitignore`).

---

## 💡 Hipótesis previas

*Las validaremos o refutaremos con los datos.*

- **H1:** los coches de alta gama se deprecian más rápido.
- **H2:** hay marcas que se deprecian menos que la media y otras que se deprecian más.
- **H3:** a igualdad de año, el precio va de mayor a menor así: eléctrico > diésel > gasolina.

**Estado tras el EDA** (primera validación en 02b_preguntas_eda.ipynb; el EDA, preguntas 1-7, está terminado):

| Hipótesis | Resultado | Dónde |
|---|---|---|
| H1 | **Refutada:** Audi, BMW y Mercedes conservan su valor por encima de la media | Pregunta 4 |
| H2 | **Apoyada:** unas marcas conservan su valor por encima de la media y otras por debajo | Pregunta 4 |
| H3 | **Apoyada** con los coches de 2018-2020: eléctrico 28.500 € > diésel 23.890 € > gasolina 17.900 € | Pregunta 5 |

Se volverán a comprobar con el modelo (SHAP) en 06_explicabilidad_negocio.ipynb.

---

## ❓ Preguntas a responder

### 🔍 Análisis exploratorio (EDA)
1. ¿Cómo se distribuye el precio y qué valores atípicos hay?
2. ¿Cuánto se deprecia un coche por cada año de antigüedad?
3. ¿Cuánto baja el precio por cada 10.000 km?
4. ¿Qué marcas conservan mejor su valor frente a otras?
5. ¿Cómo influyen el combustible y el tipo de cambio?
6. ¿Influye la provincia?
7. ¿Hay diferencias entre vendedor profesional y particular?

### 🤖 Modelo
8. ¿Qué variables influyen más en el precio? (explicabilidad)
9. ¿Qué modelo tasa mejor?
10. ¿Cuál es el error medio en € y en %?

### 💼 Negocio
11. Con un margen fijo (p. ej., 15 %), ¿en qué % de coches no perderíamos dinero?
12. ¿En qué coches falla más el modelo y hace falta revisión humana?
13. ¿Qué margen mínimo hace la oferta segura en el 90 % de los casos sin espantar al cliente?

---

## 🧠 Modelos

| Modelo | Papel |
|---|---|
| Regresión lineal | Línea base |
| Random Forest | Modelo de árboles (ensemble) |
| XGBoost | Gradient boosting |

**Resultados** (pendiente de rellenar):

| Modelo | MAE (€) | MAPE (%) | RMSE (€) | % coches con error < margen |
|---|---|---|---|---|
| Regresión lineal | | | | |
| Random Forest | | | | |
| XGBoost | | | | |

---

## 📏 Métricas y KPIs

### Técnicas
| Métrica | Qué mide | Por qué la usamos |
|---|---|---|
| **MAE** | Error medio en € | Habla el lenguaje del negocio: «me equivoco de media en X €» |
| **MAPE** | Error medio en % | Permite comparar coches baratos y caros |
| **RMSE** | Error en €, penaliza los errores grandes | Detecta tasaciones muy desviadas |

### De negocio
- **% de coches tasados con un error menor que el margen** → en cuántos no perderíamos dinero.
- **Dinero arriesgado de media por coche.**

### ⚖️ El error no pesa igual en los dos sentidos
- **Sobrevalorar** → pagamos de más y **perdemos dinero**.
- **Infravalorar** → como mucho, **el cliente se va**.

👉 Así que nos interesa un **modelo prudente**.

---

## 🗂️ Estructura del repositorio

```
tfm-p1-precio-coches/
├── data/
│   ├── raw/          # Datos originales, sin tocar (no se suben)
│   └── processed/    # Datos limpios listos para modelar (no se suben)
├── notebooks/        # Un cuaderno por fase (ver hoja de ruta)
├── src/              # Código reutilizable (carga, preprocesado...)
├── scripts/          # Scripts ejecutables (pipeline completo)
├── models/           # Modelos entrenados (no se suben)
├── outputs/          # Gráficos, tablas e informes generados
├── requirements.txt  # Dependencias
├── DECISIONES.md     # Registro diario de decisiones
└── README.md
```

### 📓 Hoja de ruta de cuadernos

Cada cuaderno hace **solo su fase**: lee lo que deja el anterior y guarda lo que necesita el siguiente.

| # | Cuaderno | Qué hace | Lee | Guarda |
|---|---|---|---|---|
| 1 | `01_eda.ipynb` | Explora y anota decisiones (no modifica datos) | `data/raw/` | — |
| 2 | `02_limpieza.ipynb` | Aplica las decisiones del EDA (columnas, nulos, potencia) | `data/raw/` | `data/processed/coches_limpio.csv` |
| 2b | `02b_preguntas_eda.ipynb` | Preguntas 1-7 y primera validación de H1-H3 (no modifica datos) | `coches_limpio.csv` | figuras en `outputs/figures/` |
| 3 | `03_preprocesado.ipynb` | Atípicos, encoding, train/test, escalado (solo para la lineal) | `coches_limpio.csv` | train/test en `data/processed/` |
| 4 | `04_modelado.ipynb` | Entrena regresión lineal, Random Forest y XGBoost | train/test | `models/` |
| 5 | `05_evaluacion.ipynb` | Compara MAE, MAPE y RMSE y elige el mejor | `models/` + test | `outputs/` |
| 6 | `06_explicabilidad_negocio.ipynb` | SHAP, hipótesis, preguntas 11-13, paso a producción | mejor modelo + test | `outputs/` |

> No usamos PCA: hay pocas variables y queremos un modelo explicable. El escalado solo se aplica a la regresión lineal.

---

## 🌿 Flujo de ramas

- **`develop`** → rama de trabajo del día a día.
- **`main`** → solo lo terminado y revisado.
- **`experiment/...`** → pruebas (p. ej., `experiment/xgboost`), que se fusionan en `develop` si salen bien.

---

## ▶️ Cómo ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

*(Pendiente de completar con la ejecución del pipeline.)*

---

## 🖼️ Visualizaciones del EDA

Figuras generadas en notebooks/01_eda.ipynb y notebooks/02b_preguntas_eda.ipynb (se guardan con plt.savefig en outputs/figures/).

**Distribución de las variables numéricas:** histogramas de precio, kilómetros, potencia y fotos; todas con cola a la derecha.

![Distribución de las variables numéricas](outputs/figures/01_distribucion_variables_numericas.png)

**Diagramas de caja:** valores que se alejan del resto en precio, kilómetros, potencia y fotos.

![Diagramas de caja](outputs/figures/02_boxplot_variables_numericas.png)

**Logaritmo del precio:** en escala logarítmica el precio se parece mucho más a una campana.

![Distribución del logaritmo del precio](outputs/figures/03_distribucion_log_precio.png)

**Mediana del precio por año:** el precio baja de forma regular con la antigüedad (≈ 11-12 % por año).

![Mediana del precio por año de fabricación](outputs/figures/04_mediana_precio_por_anio.png)

**Mediana del precio por tramo de kilómetros (Pregunta 3):** el precio baja de forma regular con los kilómetros (≈ 657 € cada 10.000 km).

![Mediana del precio por tramo de 10.000 km](outputs/figures/05_mediana_precio_por_kms.png)

**Valor retenido por marca (Pregunta 4):** mediana de los coches de 2013-2015 frente a la de 2018-2020; Fiat, Audi y Volkswagen son las que mejor conservan su valor.

![Valor retenido por marca](outputs/figures/06_valor_retenido_por_marca.png)

**Mediana del precio por combustible (Pregunta 5):** con los coches de 2018-2020, eléctrico (28.500 €) > diésel (23.890 €) > gasolina (17.900 €).

![Mediana del precio por combustible](outputs/figures/07_mediana_precio_por_combustible.png)

**Mediana del precio por tipo de cambio (Pregunta 5):** con los coches de 2018-2020, un automático vale de mediana 30.800 € frente a 17.400 € de un manual.

![Mediana del precio por tipo de cambio](outputs/figures/08_mediana_precio_por_cambio.png)

**Mediana del precio por provincia (Pregunta 6):** en la península hay poca diferencia entre provincias; Canarias y Baleares salen más baratas.

![Mediana del precio por provincia](outputs/figures/09_mediana_precio_por_provincia.png)

**Mediana del precio por tipo de vendedor (Pregunta 7):** con todos los años, un profesional anuncia a 15.999 € y un particular a 7.800 €; con los coches de 2018-2020 la diferencia desaparece (20.900 € frente a 21.000 €).

![Mediana del precio por tipo de vendedor](outputs/figures/10_mediana_precio_por_vendedor.png)

---

## 📈 Resultados

*Pendiente.*

## 🔎 Explicabilidad

*Pendiente.*

## 🚀 Paso a producción

*Pendiente.*

## ✅ Conclusiones y mejoras

*Pendiente.*
