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
- **H2:** Volkswagen se deprecia menos que la media.
- **H3:** a igualdad de año, el precio va de mayor a menor así: eléctrico > diésel > gasolina.

---

## ❓ Preguntas a responder

### 🔍 Análisis exploratorio (EDA)
1. ¿Cómo se distribuye el precio y qué valores atípicos hay?
2. ¿Cuánto se deprecia un coche por cada año de antigüedad?
3. ¿Cuánto baja el precio por cada 10.000 km?
4. ¿Qué marcas mantienen mejor su valor?
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
├── notebooks/        # Notebooks de trabajo: 01_eda, 02_modelo...
├── src/              # Código reutilizable (carga, preprocesado...)
├── scripts/          # Scripts ejecutables (pipeline completo)
├── models/           # Modelos entrenados (no se suben)
├── outputs/          # Gráficos, tablas e informes generados
├── requirements.txt  # Dependencias
└── README.md
```

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

## 📈 Resultados

*Pendiente.*

## 🔎 Explicabilidad

*Pendiente.*

## 🚀 Paso a producción

*Pendiente.*

## ✅ Conclusiones y mejoras

*Pendiente.*
