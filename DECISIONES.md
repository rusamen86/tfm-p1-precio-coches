# Registro de decisiones · TFM Proyecto 1

Diario de las decisiones tomadas en el proyecto. Cada entrada recoge **qué se decidió**, **por qué** y, si aplica, **la cifra** que lo apoya.

---

## 10-10-2026

- **Dos repositorios, uno por proyecto.** El repo existente se renombra a tfm-p1-precio-coches (Proyecto 1) y se crea tfm-p2 (Proyecto 2). Motivo: el TFM tiene dos proyectos independientes (60 % y 40 % de la nota).
- **Repos fuera de Google Drive** (en Documents/TFM). Motivo: Drive sincronizando la carpeta .git puede corromper el repositorio. La copia antigua se conserva renombrada como proyecto_data_OLD_movido_a_Documentos.
- **Ramas: develop para trabajar, main para lo terminado** (y experiment/... para pruebas). Motivo: main queda siempre estable y revisada.
- **Estructura base del repo:** data/raw, data/processed, notebooks, src, scripts, models, outputs. Motivo: es la estructura propuesta en la presentación del máster.
- **El CSV no se sube a GitHub** (data/raw, data/processed y models están en .gitignore). Motivo: los datos no se versionan.
- **Dataset del Proyecto 1:** anuncios de coches de segunda mano en España. Motivo: permite un modelo de regresión sencillo de explicar (año, km, potencia y marca mandan).

## 11-10-2026

- **Objetivo de negocio:** estimar el precio de venta de un coche usado para una empresa de compraventa y calcular la oferta al cliente con la fórmula *oferta = precio_estimado × (1 − margen) − costes de preparación*. Motivo: convierte el modelo en una guía de tasación útil.
- **Hipótesis previas** (escritas antes de explorar, para no ajustarlas a los datos):
  - H1: la alta gama se deprecia más rápido.
  - H2: Volkswagen se deprecia menos que la media.
  - H3: a igual año, eléctrico > diésel > gasolina en precio.
- **13 preguntas:** EDA (1-7), modelo (8-10) y negocio (11-13). Detalle en el README.
- **Modelos:** regresión lineal (línea base), Random Forest y XGBoost. Motivo: de lo más simple a lo más potente, todos vistos en el máster.
- **Métricas:**
  - MAE: error medio en euros, el lenguaje del negocio.
  - MAPE: error en %, permite comparar coches baratos y caros.
  - RMSE: penaliza los errores grandes.
  - El error es asimétrico: sobrevalorar hace perder dinero, infravalorar como mucho pierde al cliente. Buscamos un modelo prudente.
- **Fuente del dataset:** muestra gratuita de DataMarket (repo Data-Market/vehiculos-de-segunda-mano). Son 50.000 anuncios y 21 columnas, captura del 15-01-2021 y publicaciones del 09-05-2017 al 15-01-2021. La web de origen está anonimizada. Licencia: muestra de evaluación y uso gratuito. Limitación: son precios de anuncio, no de venta real.
- **Entorno:** venv propio (.venv) con kernel tfm-p1. Se añade xgboost a requirements. Motivo: el Python del sistema no deja instalar paquetes fuera de un entorno virtual.
- **Hoja de ruta de 6 cuadernos:** 01_eda, 02_limpieza, 03_preprocesado, 04_modelado, 05_evaluacion y 06_explicabilidad_negocio. **Cada cuaderno, solo su fase.** Motivo: el EDA solo explora y anota decisiones; los cambios se aplican donde toca y así cada paso es fácil de explicar.
- **Sin PCA.** Motivo: hay pocas variables y queremos que el modelo se pueda explicar.
- **Escalado solo para la regresión lineal.** Motivo: los modelos de árboles no lo necesitan.
- **Sin warnings** (no se usa warnings.filterwarnings). Motivo: los avisos se leen y se entienden, no se esconden.
- **Eliminar price_financed.** Motivo: falta en más de la mitad de los anuncios (26.437 nulos) y va casi a la par que price (correlación 0,997), así que no aporta información nueva.
- **Quitar url, company y country.** Motivo: no describen el coche. url es un identificador único, company tiene un solo valor y country siempre es "Spain".
- **Marca de los D2S = INVICTA ELECTRIC.** Motivo: los 2 anuncios sin marca son del modelo D2S y no hay otro anuncio del que copiarla. Fuente externa: invictaelectric.es.
- **Pasar year a entero (int16) tras tratar sus 2 nulos.** Motivo: el año no tiene decimales; int16 basta y reduce memoria (int64 ocupa lo mismo que float64).
- **Mantener power aunque tenga nulos.** Motivo: 8.528 nulos (17 %), pero es una variable clave para el precio.
- **Filas con 3 nulos a la vez:** como mucho se eliminan (son 3 filas). Motivo: es preferible descartarlas antes que completar tantos datos.

## 12-10-2026

- **Corte de precio: de 1.000 € a 100.000 €.** Motivo de negocio: por debajo de 1.000 € la empresa no compra (coches demasiado antiguos o en mal estado) y por encima de 100.000 € son casos aislados. Cifras: 1.012 coches por debajo de 1.000 € y 195 por encima de 100.000 €.
- **Kilómetros hasta 1.000.000.** Motivo: por encima no es un kilometraje creíble. Cifra: 21 anuncios.
- **Potencia hasta 700 CV** (los nulos no entran en este corte). Cifra: 6 anuncios.
- **Fotos sin recortar.** Motivo: el máximo es 54, el tope del portal; no son casos aislados.
- **Los 99.999 km exactos se anotan como limitación.** Motivo: pueden ser un relleno, pero no se puede reconstruir el dato. Cifra: 19 anuncios.
- **Los cortes se aplican en 03_preprocesado, no en la limpieza.** Motivo: no corrigen errores; definen a qué coches se aplica el modelo.
- **Probar a predecir log(price).** Motivo: el precio tiene mucha cola a la derecha; la asimetría pasa de 6,6 a −0,5 con el logaritmo. Además, la depreciación es exponencial y en log baja casi en línea recta.
- **Depreciación de referencia: 11-12 % por año de antigüedad** (media 11,3 %, mediana 12,4 %). Es la "media" contra la que se comparan H1 y H2.
- **Sesgo de supervivencia en coches de más de 20 años.** Con esa edad solo siguen a la venta los bien conservados o apreciados, y hay menos anuncios. Por eso de 2001 a 2000 el precio sube un 8,1 % y la depreciación deja de ser fiable.
- **Antigüedad hasta 15 años (year de 2006 en adelante).** Decisión de negocio: la empresa se centra en coches de 0 a 15 años, donde la caída es clara y predecible. Cifra: se pierden 7.979 anuncios (16,4 % del rango 1.000-100.000 €).
- **Figuras del EDA en outputs/figures** (con plt.savefig) y enlazadas en el README.
- **Nulos de power tras los cortes: 3.842 (9,4 %)** de 40.801 anuncios.
- **Imputar power SOLO con la moda de marca + modelo.** Motivo: la mediana podría dar potencias que no existen en ese modelo; la moda es un motor real y frecuente.
  - Se descartó buscar un gemelo exacto (marca + modelo + versión): solo 88 casos y añade complejidad.
  - Se descartó extraer los CV del texto de version: solo recupera 15 nulos y añade complejidad.
- **Markdown de los cuadernos sin backticks ni resaltados.** Motivo: preferencia de estilo de Rubén.

## 13-10-2026

- **Eliminar los coches sin potencia y sin ningún coche de la misma marca y modelo** (unos 108 antes de los cortes, ≈ 0,2 %), en lugar de rellenarlos con la media. Motivo: la media daría potencias que no existen y mezclaría segmentos distintos. El número real se contará tras aplicar los cortes.

- **Nuevo cuaderno 01b_preguntas_eda.** Las preguntas e hipótesis salen de 01_eda a un cuaderno propio. Motivo: 01_eda se queda con la revisión de los datos y 01b con las preguntas 1-7 y la primera validación de H1-H3, así cada cuaderno es más corto y fácil de seguir.
- **La comprobación de gemelos de potencia pasa a 02_limpieza.** Motivo: es la base del tratamiento de los nulos de power (moda de marca + modelo y eliminar los que no tienen gemelo), que se aplica en la limpieza.
- **Kilómetros (Pregunta 3): cada 10.000 km restan unos 656 € de mediana** (≈ 2,7 % del precio del primer tramo), con la bajada más fuerte en los primeros 10.000 km. Kilómetros y año están muy relacionados (correlación −0,77), así que parte de la bajada es por edad.

---

## Pendiente

- Revisar el resto de nulos pequeños: model (5), fuel (46), shift (111), color (594) y province (6).
- Valorar si se quita dealer.
- Unificar colores.
- Actualizar las "Conclusiones del EDA" del cuaderno: siguen citando el corte antiguo de 350.000 € y no recogen los cortes de 1.000-100.000 €, de antigüedad, el log del precio ni la imputación por moda.
- Responder a las preguntas 3 a 7 del EDA y hacer una primera validación de H1, H2 y H3.
