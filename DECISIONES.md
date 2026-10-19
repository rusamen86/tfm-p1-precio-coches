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
- **Los cortes se aplican en 02_limpieza, al principio.** Motivo: no corrigen errores; definen a qué coches se aplica el modelo, y aplicarlos primero evita limpiar o rellenar coches que luego se van a quitar. (Al principio se pensaron para 03_preprocesado.)
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

- **Nuevo cuaderno 02b_preguntas_eda** (se creó como 01b y después se renombró a 02b, porque trabaja con el dataset limpio de 02_limpieza). Las preguntas e hipótesis salen de 01_eda a un cuaderno propio. Motivo: 01_eda se queda con la revisión de los datos y 02b con las preguntas 1-7 y la primera validación de H1-H3, así cada cuaderno es más corto y fácil de seguir.
- **La comprobación de gemelos de potencia pasa a 02_limpieza.** Motivo: es la base del tratamiento de los nulos de power (moda de marca + modelo y eliminar los que no tienen gemelo), que se aplica en la limpieza.
- **Kilómetros (Pregunta 3): cada 10.000 km restan unos 656 € de mediana** (≈ 2,7 % del precio del primer tramo), con la bajada más fuerte en los primeros 10.000 km. Kilómetros y año están muy relacionados (correlación −0,77), así que parte de la bajada es por edad.

## 16-10-2026

- **Quitar publish_date y photos.** Motivo: todos los anuncios se capturaron casi a la vez, así que la fecha no ayuda a estimar el precio, y el número de fotos no es una característica del coche.
- **Antigüedad (age) en lugar del año: 2021 menos year.** Motivo: es más fácil de interpretar. Los datos se capturaron en enero de 2021.
- **is_professional y shift como 0/1 (profesional = 1, automático = 1).** Motivo: solo tienen dos valores, así que basta una columna.
- **La provincia se sustituye por una sola columna, isla** (Las Palmas, Tenerife y Baleares = 1). Motivo: en la Pregunta 6 la provincia apenas cambia el precio en la península y en las islas los coches son más baratos. Una columna en vez de 52.
- **Variable objetivo: el logaritmo del precio.** Motivo: la distribución es más simétrica y el error se mide en proporción al precio.
- **Train y test 80/20:** 32.491 y 8.123 coches.
- **Todo lo que se aprende de los datos se ajusta solo con train** (marca, target encoding y escalado). Motivo: que test no influya en el preprocesado. El one-hot del combustible se hace antes de separar porque no aprende nada de los datos.
- **Marca: las 10 más frecuentes en train y el resto en Other, con one-hot.** Motivo: hay muchas marcas y algunas tienen muy pocos coches.
- **Modelo con target encoding (smooth='auto').** Motivo: hay 690 modelos distintos en train, demasiados para una columna por cada uno. Con smooth, los modelos con pocos coches se acercan a la media general.
- Quedan 26 columnas numéricas y sin nulos.

## 17-10-2026

- **Los tres modelos (regresión lineal, Random Forest y XGBoost) en un solo cuaderno, 04_modelado.** Motivo: se entrenan con los mismos datos y se miden con las mismas métricas, así la comparación queda en un solo sitio.
- **Ajuste de hiperparámetros con RandomizedSearchCV (n_iter=10, cv=3, MAE como medida), no con GridSearch.** Motivo: prueba 10 combinaciones al azar en lugar de todas, así la búsqueda es más corta. Se hace solo con train, test no se toca.
- **El ajuste mejora poco.** Cifras: el Random Forest pasa de 1.849 € a 1.816 € de MAE en test (unos 30 €) y de 12,9 % a 12,6 % de MAPE. El XGBoost pasa de 1.918 € a 1.854 €.
- **Métricas: MAE, MAPE, RMSE y R2 en train y en test, más el % de coches con error menor del 15 %.** No se añaden más. Motivo: comparar train y test muestra el sobreajuste, y el 15 % es el margen de la empresa.
- **Los modelos se guardan con joblib en models/.** Motivo: los cuadernos siguientes los cargan sin volver a entrenar, y es la base para usar el modelo fuera del proyecto. joblib no se vio en el máster: es investigación propia y una aportación del TFM.

## 18-10-2026

- **Descartar la regresión lineal.** Motivo: queda claramente por detrás en todas las métricas (MAE de 2.664 € y solo un 58,7 % de coches con error menor del 15 %).
- **Modelo elegido: Random Forest ajustado, con criterio de negocio.** Motivo: en las métricas generales está muy igualado con XGBoost (Random Forest gana en MAE y MAPE, XGBoost en RMSE), pero pone menos dinero en riesgo. Cifras: el Random Forest sobrevalora el 49,9 % de los coches, de media 1.537 €, 6,23 millones de euros en total; el XGBoost el 50,1 %, de media 1.624 €, 6,61 millones (unos 380.000 € más). Además, el Random Forest acierta más en los coches de 10.000 a 40.000 € y en los de hasta 3 años, que son el grueso del negocio.
- **XGBoost queda como alternativa.** Motivo: resultados muy cercanos y más estable entre train y test (unos 350 € de diferencia de MAE frente a unos 1.150 € del Random Forest).
- **Sin cuaderno 04b ni reentrenar los modelos para que infravaloren.** Motivo: la protección frente a la sobrevaloración la da el margen. En la otra mitad de los coches el modelo infravalora (unos 2.100 € de media) y ahí el beneficio es mayor o, como mucho, se pierde la compra.
- **Pregunta 12 con tramos de pd.cut, incluido uno de 40.000 a 60.000 €.** Motivo: que 60.000-100.000 € quede como alta gama aparte. Resultado: el error pasa del 28-29 % en los coches de menos de 5.000 € al 9-10 % entre 10.000 y 40.000 €, y crece con la antigüedad (8-9 % hasta 3 años, más de un 22 % con más de 12). Los coches baratos y viejos son los más difíciles porque su precio depende del estado, que no está en los datos.
- **SHAP con TreeExplainer sobre una muestra de 500 coches de test.** Motivo: en un Random Forest de 100 árboles sin límite de profundidad el cálculo es lento, y 500 coches bastan para ver el comportamiento general. Resultado: age, model, power y kms, en ese orden; el cambio automático sube el precio alrededor de un 10 %.
- **Hipótesis validadas con el modelo mediante simulación:** los mismos coches de test con 2 y con 8 años, y cambiando solo el combustible. Motivo: así se comparan coches idénticos en todo lo demás, algo que con los datos en bruto no se puede hacer.
  - H1 refutada: alta gama (Audi, BMW y Mercedes-Benz) retiene un 71,2 % de su valor de 2 a 8 años y el resto un 70,8 %.
  - H2 apoyada: el valor retenido va del 64 % de Peugeot al 74 % de Mercedes-Benz.
  - H3 apoyada solo en parte: diésel (17.288 €) > eléctrico (16.646 €) > gasolina (16.265 €). El combustible pesa poco, gran parte de su efecto ya lo recoge model y hay muy pocos eléctricos.
- **Figura 20 por marca** (20_valor_retenido_marca.png): valor retenido de 2 a 8 años según marca, que es lo que miden H1 y H2.
- **Los costes de preparación se dejan fuera de la oferta.** Motivo: no hay datos. Se considera que no se pierde dinero si la oferta es igual o menor que el precio real.
- **Margen.** Pregunta 11: con un 15 %, no se pierde dinero en el 88,3 % de los coches (80,1 % con un 10 % y 93 % con un 20 %). Pregunta 13: el margen mínimo para no perder en el 90 % de los coches es del 16,5 %, con una oferta mediana del 83,4 % del precio real. El 10 % restante conviene que lo revise una persona antes de hacer la oferta.
- **Presentación de negocio en PDF, en docs/presentacion_negocio.pdf.** Motivo: el enunciado no la pide, pero valora las aportaciones adicionales y el enfoque de negocio.
- **Etiquetas del eje de la figura 16 inclinadas** (rotation=30, ha='right'). Motivo: los nombres de los tramos de precio se solapaban.
- **Borrar las carpetas src/ y scripts/.** Motivo: solo tenían archivos de plantilla sin código; todo el flujo está en los cuadernos.

---

## Pendiente

- Sección de producción en el README, tras las clases del 23-10.
- "Cómo ejecutar" y sección de dificultades en el README.
- Repaso final del README y del esquema del flujo.
