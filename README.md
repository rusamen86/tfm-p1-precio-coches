# TFM Proyecto 1 - Predicción del precio de coches de segunda mano

Modelo predictivo (regresión) del precio de coches de segunda mano en España a partir de anuncios (año, kilómetros, potencia, marca, etc.).

El dataset (`data/raw/coches_segunda_mano.csv`) no se sube al repositorio.
Enlace de descarga del dataset: https://raw.githubusercontent.com/Data-Market/vehiculos-de-segunda-mano/main/coches-de-segunda-mano-sample.csv

## Objetivo de negocio: 
	una empresa de compraventa de coches usados quiere estimar a qué precio podrá vender un coche. Con ese precio y el margen que busca, calcula cuánto ofrecer al cliente que viene a venderlo.

## oferta=
	precio estimado ×(1−margen)−costes de preparacion
	oferta=precio estimado×(1−margen)−costes de preparacion

## Qué haría el modelo: 
	una regresión que predice price a partir de la marca, el modelo, el año, los km, la potencia, el combustible, el cambio y la provincia.

## KPIs (indicadores de éxito):

### Técnicos: el MAE, que es el error medio en euros ("me equivoco de media en X €"), y el MAPE, ese mismo error en porcentaje.
### De negocio: qué porcentaje de coches tasamos con un error menor que el margen, es decir, en cuántos no perderíamos dinero. Y cuánto dinero arriesgamos de media por coche.

el error no pesa igual en los dos sentidos. Si sobrevaloramos un coche pagamos de más y perdemos dinero. Si lo infravaloramos, como mucho el cliente se va. Así que nos interesa un modelo prudente

