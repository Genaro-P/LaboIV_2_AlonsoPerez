import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#URL del repositorio publico de github: https://github.com/Genaro-P/Labo2Info2AlonsoGenaro

#Esto es el inciso 1
telemetria = pd.read_csv('telemetria_nodo_iot.csv', parse_dates=['timestamp'])
telemetria = telemetria.set_index('timestamp')
print(telemetria, "\n\n")

#Esto es el inciso 2
print("Estadisticas:")
print("count: Cantidad de elementos en la columna.")
print("mean: Valor promedio aritmetico de cierta colmna.")
print("std: Desviacion estandar de la columna, separacion promedio del valor promedio.")
print("min: Valor minimo de la columna.")
print("25%, 50%, 75%: Cuartiles de la columna.")
print("max: Valor maximo de la columna.\n")
print(telemetria.describe())



#Hay que crear un arreglo separado de numpy, el cual contiene valores booleanos.
#Hacer maindataframe[filtro] te tira un nuevo dataframe, el cual te da solo las filas
#que coincidan con los valores True de 'filtro', por ejemplo



#Definimos 3 criterios de alerta
print("\n\n")
print("Criterios de alerta:")
print(" - Registros de voltaje mayor a 4 V")
print(" - Registros de temperatura mayor a 20 C")
print(" - Registors de porcentaje de humedad menor o igual a 50%")

#Filtro de filas con voltaje menor o igual a 4 V
filtro_V = np.less_equal(telemetria['voltaje_bateria_V'], 4)
filtro_T = np.less_equal(telemetria['temperatura_C'], 20)
filtro_H = np.greater(telemetria['humedad_pct'], 50)

cumple_V = len(telemetria[filtro_V])
cumple_T = len(telemetria[filtro_T])
cumple_H = len(telemetria[filtro_H])

#Para contar cuales presentan al menos 1 alerta, hay que contar el total que cumple
#con todo, y restarlo a la cantidad total de filas

#Para hacerlo, hay que aplicar todos los filtros en el dataframe. Hay que aplicar
#cada filtro uno por uno y cada uno te retornara un dataframe de menor tamanio. Habra que
#hacer filtros del mismo tamanio que estos nuevos dataframes para que las funciones 
#hagan los calculos que queremos

telemetria_filtro_V = telemetria[filtro_V]
filtro_V_T = np.less_equal(telemetria_filtro_V['temperatura_C'], 20)
telemetria_filtro_V_T = telemetria_filtro_V[filtro_V_T]
filtro_V_T_H = np.greater(telemetria_filtro_V_T['humedad_pct'], 50)

cumple_todo = len(telemetria_filtro_V_T[filtro_V_T_H])
una_alerta = len(telemetria) - cumple_todo

print("Cantidad de entradas que cumplen con el voltaje:", cumple_V)
print("Cantidad de entradas que cumplen con la temperatura:", cumple_T)
print("Cantidad de entradas que cumplen con el porcentaje de humedad:", cumple_H)
print("Cantidad de entradas que poseen al menos una alerta:", una_alerta, "\n\n")


