# Dashboard de tasación de coches de segunda mano (TFM Proyecto 1)
# Arranque: streamlit run app/dashboard.py

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import TargetEncoder

# Carpeta raíz del proyecto (la que contiene app/, data/, models/ y outputs/)
RAIZ = Path(__file__).resolve().parent.parent

ISLAS = ['Las Palmas', 'Tenerife', 'Baleares']


def euros(valor):
    # Formato español: 12.345 €
    return f'{valor:,.0f}'.replace(',', '.') + ' €'


# --- Carga del modelo, los datos limpios y el preprocesado (solo una vez) ---

@st.cache_resource
def cargar_modelo():
    # Random Forest ya entrenado en 04_modelado. No se vuelve a entrenar.
    # Es una copia comprimida del mismo modelo (65 MB en vez de 284 MB),
    # para que quepa en GitHub y el dashboard funcione también en la web.
    return joblib.load(RAIZ / 'models' / 'random_forest_app.joblib')


@st.cache_data
def cargar_datos():
    return pd.read_csv(RAIZ / 'data' / 'processed' / 'coches_limpio.csv')


@st.cache_data
def cargar_mae():
    # MAE en test del Random Forest, guardado por 04_modelado
    metricas = pd.read_csv(RAIZ / 'outputs' / 'metricas_random_forest.csv')
    return metricas.loc[metricas['conjunto'] == 'test', 'MAE (€)'].iloc[0]


@st.cache_resource
def cargar_preprocesado():
    # El cuaderno 03 no guarda sus encoders, así que repetimos aquí los mismos
    # pasos sobre los datos limpios: mismo train/test (random_state=42), las 10
    # marcas más frecuentes en train y el TargetEncoder del modelo ajustado
    # solo con train. Esto no entrena el Random Forest.
    df = cargar_datos()
    X = df.drop(columns='price')
    y = np.log(df['price'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    top = list(X_train['make'].value_counts().head(10).index)

    te = TargetEncoder(smooth='auto', target_type='continuous')
    te.fit(X_train[['model']], y_train)

    modelos_train = set(X_train['model'])
    return top, te, modelos_train


@st.cache_resource
def cargar_explicador():
    # El mismo explicador de SHAP que en 06_explicabilidad_negocio
    return shap.TreeExplainer(cargar_modelo())


model = cargar_modelo()
explicador = cargar_explicador()
df = cargar_datos()
mae = cargar_mae()
top, te, modelos_train = cargar_preprocesado()

# Rango de los datos con los que se entrenó el modelo
edad_max = int(2021 - df['year'].min())
kms_max = int(df['kms'].max())
power_min = int(df['power'].min())
power_max = int(df['power'].max())


# --- Página ---

st.set_page_config(page_title='Tasador de coches de ocasión', page_icon='🚗')

st.title('🚗 Tasador de coches de ocasión')
st.caption('Concesionario Seat (ficticio) · Guía de tasación del TFM. '
           'Los precios son de anuncios de enero de 2021, no de ventas reales.')

# Parámetros de la oferta, en la barra lateral
st.sidebar.header('Parámetros de la oferta')
margen = st.sidebar.slider('Margen (%)', min_value=0.0, max_value=40.0, value=15.0, step=0.5)
costes = st.sidebar.number_input('Costes de preparación (€)', min_value=0, max_value=20000, value=0, step=50)
st.sidebar.markdown('**Fórmula:** oferta = precio estimado × (1 − margen) − costes de preparación')

# Datos del coche
st.subheader('Datos del coche')

col1, col2 = st.columns(2)

with col1:
    marcas = sorted(df['make'].unique())
    marca = st.selectbox('Marca', marcas, index=marcas.index('SEAT'))

    modelos = sorted(df.loc[df['make'] == marca, 'model'].unique())
    modelo = st.selectbox('Modelo', modelos)

    combustibles = list(df['fuel'].value_counts().index)
    combustible = st.selectbox('Combustible', combustibles)

    cambio = st.selectbox('Cambio', ['Manual', 'Automático'])

    vendedor = st.selectbox('Tipo de vendedor', ['Profesional', 'Particular'])

with col2:
    edad = st.number_input('Antigüedad (años)', min_value=0, max_value=40, value=5, step=1)

    kms = st.number_input('Kilómetros', min_value=0, max_value=2000000, value=80000, step=5000)

    # Potencia por defecto: la más frecuente de ese modelo en los datos
    potencia_frecuente = int(df.loc[(df['make'] == marca) & (df['model'] == modelo), 'power'].mode().iloc[0])
    potencia = st.number_input('Potencia (CV)', min_value=1, max_value=1500, value=potencia_frecuente, step=5)

    puertas = st.selectbox('Puertas', [2, 3, 4, 5], index=3)

    isla = st.checkbox('El coche está en Canarias o Baleares')

if st.button('Calcular tasación', type='primary'):

    # Construimos una fila con las mismas columnas que espera el modelo, todas a 0
    fila = pd.DataFrame(0.0, index=[0], columns=model.feature_names_in_)

    # Modelo: target encoding aprendido en train
    fila['model'] = te.transform(pd.DataFrame({'model': [modelo]}))[0][0]

    fila['kms'] = kms
    fila['power'] = potencia
    fila['doors'] = puertas
    fila['shift'] = 1 if cambio == 'Automático' else 0
    fila['is_professional'] = 1 if vendedor == 'Profesional' else 0
    fila['age'] = edad
    fila['isla'] = 1 if isla else 0

    # Combustible: one-hot
    fila['fuel_' + combustible] = 1

    # Marca: las 10 más frecuentes en train o Other, y one-hot
    marca_agrupada = marca if marca in top else 'Other'
    fila['make_' + marca_agrupada] = 1

    # El modelo predice el logaritmo del precio; lo deshacemos con np.exp
    precio = np.exp(model.predict(fila)[0])

    precio_min = max(precio - mae, 0)
    precio_max = precio + mae
    oferta = precio * (1 - margen / 100) - costes

    st.subheader('Resultado')

    c1, c2, c3 = st.columns([2, 3, 2])
    c1.metric('Precio estimado', euros(precio))
    c2.metric('Rango aproximado', euros(precio_min) + ' – ' + euros(precio_max))
    c3.metric('Oferta de compra', euros(max(oferta, 0)))

    st.write('El rango es el precio estimado ± el error medio del modelo en test '
             '(MAE de ' + euros(mae) + '). Es orientativo, no un intervalo de confianza.')
    st.write('Oferta = ' + euros(precio) + ' × (1 − ' + str(margen).replace('.', ',') + ' %) − '
             + euros(costes) + ' = ' + euros(oferta))

    if oferta <= 0:
        st.error('Con este margen y estos costes la oferta sale a cero o negativa: no compensa comprar el coche.')

    # Avisos: coche fuera del rango con el que se entrenó el modelo
    if edad > edad_max:
        st.warning('El coche tiene más de ' + str(edad_max) + ' años. El modelo se entrenó con coches de 0 a '
                   + str(edad_max) + ' años, así que esta tasación no es fiable.')
    if kms > kms_max:
        st.warning('Los kilómetros superan el máximo visto en los datos ('
                   + f'{kms_max:,}'.replace(',', '.') + ' km).')
    if potencia < power_min or potencia > power_max:
        st.warning('La potencia se sale del rango visto en los datos (de ' + str(power_min) + ' a '
                   + str(power_max) + ' CV).')
    if modelo not in modelos_train:
        st.warning('Este modelo no estaba en los datos de entrenamiento. '
                   'El modelo lo trata como un coche medio, así que la tasación es poco fiable.')

    # Revisión manual: donde el modelo falla más (05_evaluacion, pregunta 12)
    if precio < 5000 or edad > 12:
        st.info('Revisión manual recomendada: el modelo falla más (errores del 22-29 %) en coches de menos '
                'de 5.000 € y de más de 12 años, porque su precio depende mucho del estado del coche.')

    # --- Explicación de la tasación con SHAP ---
    st.subheader('¿Por qué este precio?')

    # Un valor SHAP por cada columna del modelo, en logaritmo del precio
    valores_shap = pd.Series(explicador.shap_values(fila)[0], index=fila.columns)

    # Punto de partida: lo que predice el modelo para un coche medio
    precio_medio = np.exp(np.ravel(explicador.expected_value)[0])

    # Las columnas one-hot de combustible y de marca se suman en una sola barra
    col_fuel = [c for c in fila.columns if c.startswith('fuel_')]
    col_make = [c for c in fila.columns if c.startswith('make_')]

    efectos = pd.Series({
        'Antigüedad: ' + str(edad) + ' años': valores_shap['age'],
        'Modelo: ' + modelo: valores_shap['model'],
        'Potencia: ' + str(potencia) + ' CV': valores_shap['power'],
        'Kilómetros: ' + f'{kms:,}'.replace(',', '.'): valores_shap['kms'],
        'Cambio: ' + cambio: valores_shap['shift'],
        'Combustible: ' + combustible: valores_shap[col_fuel].sum(),
        'Marca: ' + marca: valores_shap[col_make].sum(),
        'Vendedor: ' + vendedor: valores_shap['is_professional'],
        'Puertas: ' + str(puertas): valores_shap['doors'],
        'Islas: ' + ('sí' if isla else 'no'): valores_shap['isla'],
    })

    # Como el modelo trabaja con el logaritmo, cada efecto multiplica el precio.
    # Lo pasamos a porcentaje: exp(0,10) - 1 es un 10,5 % más de precio.
    efectos = ((np.exp(efectos) - 1) * 100).sort_values()

    colores = ['tab:green' if v > 0 else 'tab:red' for v in efectos]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(efectos.index, efectos.values, color=colores)
    ax.axvline(0, color='black', linewidth=0.8)
    for i, v in enumerate(efectos.values):
        etiqueta = f'{v:+.1f} %'.replace('.', ',')
        ax.text(v, i, ' ' + etiqueta + ' ', va='center', ha='left' if v > 0 else 'right')
    ax.margins(x=0.2)
    ax.set_xlabel('Efecto en el precio (%)')
    ax.set_title('Qué sube y qué baja el precio de este coche')
    st.pyplot(fig)

    st.write('El modelo parte del precio de un coche medio (' + euros(precio_medio) + ') y cada '
             'característica lo sube (verde) o lo baja (rojo) en ese porcentaje. Aplicando todos los '
             'efectos, uno detrás de otro, se llega al precio estimado de ' + euros(precio) + '.')
