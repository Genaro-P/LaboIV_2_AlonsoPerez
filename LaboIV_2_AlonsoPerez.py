import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#URL del repositorio publico de github: https://github.com/Genaro-P/Labo2Info2AlonsoGenaro

#Esto es el inciso 1
telemetria = pd.read_csv('telemetria_nodo_iot.csv', parse_dates=['timestamp'])
telemetria = telemetria.set_index('timestamp')
print("Telemetria:\n")
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
print(" - Registros de voltaje menor a 3.5 V")
print(" - Registros de temperatura mayor a 45 C") 
#principalmente por las baterias, los circuitos suelen soportar hasta 70 C o mas
#...El maximo de T registrado en la telemetria es 24 C

print(" - Registors de porcentaje de humedad mayor o igual a 70%") 
#mas de 70% en muchos dispositivos favorece la condensacion de agua en los circuitos

#Filtro de filas con voltaje menor o igual a 3.5 V
filtro_V = np.less_equal(telemetria['voltaje_bateria_V'], 3.5)
#Filtro de filas con temperatura menor o igual a 50 C
filtro_T = np.greater_equal(telemetria['temperatura_C'], 45)
#Filtro de filas con porcentaje de humedad mayor a 70%
filtro_H = np.greater(telemetria['humedad_pct'], 70)

cumple_V = len(telemetria[filtro_V])
cumple_T = len(telemetria[filtro_T])
cumple_H = len(telemetria[filtro_H])

#Para contar cuales presentan al menos 1 alerta, hay que contar el total que cumple
#con todo, y restarlo a la cantidad total de filas

alertas = telemetria[filtro_V & filtro_T & filtro_H]

cumple_todo = len(alertas)
una_alerta = len(telemetria) - cumple_todo

print("Cantidad de entradas que cumplen con el voltaje:", cumple_V)
print("Cantidad de entradas que cumplen con la temperatura:", cumple_T)
print("Cantidad de entradas que cumplen con el porcentaje de humedad:", cumple_H)
print("Cantidad de entradas que poseen al menos una alerta:", una_alerta, "\n\n")

#El grafico elegido sera el del voltaje y la humedad a lo largo del tiempo

figure = plt.gcf()
figure.set_size_inches(14, 7)

plt.subplot(121)
plt.plot(telemetria.index, telemetria['voltaje_bateria_V'],label='Voltaje', color= "g")
plt.plot(telemetria.index[-filtro_V], telemetria[-filtro_V]['voltaje_bateria_V'], 'or',
         label= 'Alerta')#Plot para marcar las alertas con puntos
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.title('Voltaje en el tiempo')
plt.legend() 

plt.subplot(122)
plt.plot(telemetria.index, telemetria['humedad_pct'], label='Humedad')
plt.plot(telemetria.index[-filtro_H], telemetria[-filtro_H]['humedad_pct'], 'or',
         label= 'Alerta') #Plot para marcar las alertas con puntos
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.title('Humedad en el tiempo')
plt.legend() 

plt.show()

#Establece el dataframe con periodo diario e ingresa ciertos datos estadisticos
resumen_diario = telemetria.resample('D').agg(
    promedio_Temp = ('temperatura_C', 'mean'),
    min_Temp = ('temperatura_C', 'min'),
    max_Temp = ('temperatura_C', 'max'),
    promedio_Voltaje = ('voltaje_bateria_V', 'mean'),
    min_Voltaje = ('voltaje_bateria_V', 'min'),
    max_Voltaje = ('voltaje_bateria_V', 'max'),
    promedio_pct_Humedad = ('humedad_pct', 'mean')
    ).round(2)

#Inicializa una serie con la cantidad de alertas por dia y lo inserta en el resumen
alertas = telemetria[-filtro_V].resample('D')['voltaje_bateria_V'].count()
alertas += telemetria[-filtro_T].resample('D')['temperatura_C'].count()
alertas += telemetria[-filtro_H].resample('D')['humedad_pct'].count()
resumen_diario['cantidad_de_alertas'] = alertas
print(resumen_diario)


