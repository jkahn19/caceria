import datetime as dt
import numpy as np
import pandas as pd

seconds2hours = 3600

listaRecursos = ['Comida','Piedra','Madera','Mineral','Oro','Anima']

# Produccion
df_produccion = pd.DataFrame([],
                            index=listaRecursos,
                            columns=['Por Hora'])

#produccion_comida = 0
df_produccion.loc[listaRecursos[0]] = 0
#produccion_piedra = 201982#216307
df_produccion.loc[listaRecursos[1]] = 205895
# produccion_madera = 257368#283981
df_produccion.loc[listaRecursos[2]] = 257368
# produccion_mineral = 173401#196140
df_produccion.loc[listaRecursos[3]] = 173401
# produccion_oro = 57350#64331
df_produccion.loc[listaRecursos[4]] = 57350
# produccion_anima = 22636
df_produccion.loc[listaRecursos[5]] = 22636

print(df_produccion)


# Caballeria -> dataframe
tipos = ['Inf', 'Art', 'Cab', 'Pac']

df_tipo = pd.DataFrame([],
                        index=tipos,
                        columns=['Cantidad'] + listaRecursos + ['Tiempo'])


velocidad_T4 = dt.timedelta(hours=9,minutes=14,seconds=1)
velocidad_Pactos = dt.timedelta(hours=18,minutes=17,seconds=34)
df_tipo.loc[tipos[0]] = [1e3, 1e6, 0, 1e6, 1e6, 5*1e5, 0, velocidad_T4]
df_tipo.loc[tipos[1]] = [1e3, 1e6, 1e6, 1e6, 0, 5*1e5, 0, velocidad_T4]
df_tipo.loc[tipos[2]] = [1e3, 1e6, 1e6, 0, 1e6, 5*1e5, 0, velocidad_T4]
df_tipo.loc[tipos[3]] = [9, 4.5*1e5, 4.5*1e5, 4.5*1e5, 4.5*1e5, 4.5*1e4, 4.5*1e5, velocidad_Pactos]
[9,450,450,450,450,450,45,450]
# cantidad_T4 = 1e3
# costo_T4_comida = 1e6
# costo_T4_piedra = 1e6
# costo_T4_madera = 0
# costo_T4_mineral = 1e6
# costo_T4_oro = 5*1e5



print(df_tipo)
# print('Produccion de piedra por el tiempo que le toma entrenar 1k de T4\n%.2f'%(df_produccion.loc[listaRecursos[1],'Por Hora']*velocidad_T4.total_seconds() / seconds2hours))


# print('''
# Cantidad T4 = %i

# Costo
# - comida = %i
# - piedra = %i
# - madera = %i
# - mineral = %i
# - oro = %i

# Tiempo = %s
# '''%(cantidad_T4,costo_T4_comida,costo_T4_piedra,costo_T4_madera,costo_T4_mineral, costo_T4_oro,velocidad_T4))
