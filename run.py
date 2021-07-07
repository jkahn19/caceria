from src.abrir import *
from src.imagenes import *
import pandas as pd
import re

palabras_claves = ['botin de', 'regalo de']
diccionario_nivel = {'comun': 1, 'poco comun': 2, 'raro': 3, 'epico': 4}
puntaje = {1:1, 2:4, 3:16}
lista_de_imagenes = []

def generar_cadena_textos(list_img):    
    candenas_texto_original = []
    candenas_texto = []

    for imagen in list_img:
        candenas_texto_original.append(extraer_texto_original(imagen))
        candenas_texto.append(extraer_texto(imagen))

    return candenas_texto_original, candenas_texto

def conteo_imagen(string_imagen_original, string_imagen):
    error = False
    conteo = [] # @TODO verificar si usar pandas

    botin_original = []
    regalo_original = []
    botin_gris = []
    regalo_gris = []

    string_imagen = string_imagen.split('\n')
    string_imagen_original = string_imagen_original.split('\n')

    for linea in string_imagen_original:
        if palabras_claves[0] in linea:
            botin_original.append(linea.strip())
        if palabras_claves[1] in linea:
            regalo_original.append(linea.strip())

    for linea in string_imagen:
        if palabras_claves[0] in linea:
            botin_gris.append(linea.strip())
        if palabras_claves[1] in linea:
            regalo_gris.append(linea.strip())
    
    n_max = max(len(botin_gris),len(regalo_gris), len(botin_original), len(regalo_original))
    botin = botin_gris
    regalo = regalo_gris
    if len(botin_gris) == n_max and len(regalo_gris) == n_max:
        botin = botin_gris
        regalo = regalo_gris
    elif len(botin_original) == n_max and len(regalo_original) == n_max:
        botin = botin_original
        regalo = regalo_original
    elif len(botin_gris) == n_max and len(regalo_original) == n_max:
        botin = botin_gris
        regalo = regalo_original
    elif len(botin_original) == n_max and len(regalo_gris) == n_max:
        botin = botin_original
        regalo = regalo_gris

    rareza_botin = ''
    nombre_jugador = ''
    try:
        for i in range(n_max):
            if not palabras_claves[0] in botin[i]:
                print('warning: no tiene la palabra clave "botin de"')
            if not palabras_claves[1] in regalo[i]:
                print('warning: no tiene la palabra clave "regalo de"')

            # nivel del monstruo
            if '[' in botin[i] and ']' in botin[i]:
                rareza_botin = botin[i].split('[')[1].split(']')[0]
            elif '(' in botin[i] and ')' in botin[i]:
                rareza_botin = botin[i].split('(')[1].split(')')[0]
            
            if not rareza_botin in diccionario_nivel.keys():
                print('rareza de botin no encontrado')
                if '[' in botin_original[i] and ']' in botin_original[i]:
                    rareza_botin = botin_original[i].split('[')[1].split(']')[0]
                elif '(' in botin_original[i] and ')' in botin_original[i]:
                    rareza_botin = botin_original[i].split('(')[1].split(')')[0]
                print(rareza_botin)
            
            nivel_botin = diccionario_nivel[rareza_botin]

            # nombre del jugador
            nombre_jugador = regalo[i].split(palabras_claves[1])[1]
            conteo.append([nombre_jugador,nivel_botin])
        error = True
    except:
        print('********** error **********')
    return conteo, error

def contar(cadena_textos_original, cadena_textos):
    global lista_de_imagenes
    data = []

    for i in range(len(cadena_textos)):
        #print('proceso %i/%i'%(i,len(cadena_textos)))
        data_img, agregar_bol = conteo_imagen(cadena_textos_original[i], cadena_textos[i])
        if agregar_bol:
            data += data_img
        else:
            print(lista_de_imagenes[i])
            print('********** error **********')

    data_frame = pd.DataFrame(data, columns = ['Nombre', 'Rareza'])

    return data_frame

def puntaje(data):
    dataframe = pd.DataFrame([], columns=['Nombre', 'N1', 'N2', 'N3', 'N4', 'Puntaje'])
    dataframe['Nombre'] = data['Nombre'].unique()
    dataframe['Puntaje'] = 0

    for nombre in dataframe['Nombre']:
        numero_n1 = 0
        numero_n2 = 0
        numero_n3 = 0
        numero_n4 = 0
        valor_puntaje = 0

        for valor in data[data['Nombre'] == nombre]['Rareza']:
            if valor == 1:
                numero_n1 += 1
                valor_puntaje += 1
            elif valor == 2:
                numero_n2 += 1
                valor_puntaje += 2
            elif valor == 3:
                numero_n3 += 1
                valor_puntaje += 16
            elif valor == 4:
                numero_n4 += 1
                valor_puntaje += 64
        
        dataframe.loc[dataframe['Nombre'] == nombre, 'N1'] = numero_n1
        dataframe.loc[dataframe['Nombre'] == nombre, 'N2'] = numero_n2
        dataframe.loc[dataframe['Nombre'] == nombre, 'N3'] = numero_n3
        dataframe.loc[dataframe['Nombre'] == nombre, 'N4'] = numero_n4
        dataframe.loc[dataframe['Nombre'] == nombre, 'Puntaje'] = valor_puntaje

    return dataframe

def depurar_nombre(name):
    newname = name.strip()
    newname = re.sub(r'[0-9]+', '', newname)
    newname = newname.replace(' ','')
    return newname

def depurar(df):
    list_name = df['Nombre'].to_list()
    list_filtername = []

    for i in range(len(list_name)):
        newname = depurar_nombre(list_name[i])
        if not newname in list_filtername:
            list_filtername.append(newname)
    
    df_filter = pd.DataFrame([], columns=['Nombre', 'N1', 'N2', 'N3', 'N4', 'Puntaje'])
    df_filter['Nombre'] = list_filtername
    df_filter['N1'] = 0
    df_filter['N2'] = 0
    df_filter['N3'] = 0
    df_filter['N4'] = 0
    df_filter['Puntaje'] = 0

    for name in list_name:
        df_filter.loc[df_filter['Nombre']==depurar_nombre(name),['N1', 'N2', 'N3', 'N4', 'Puntaje']] += np.sum(df.loc[df['Nombre']==name,['N1', 'N2', 'N3', 'N4', 'Puntaje']].values.tolist(), axis=0)

    return df_filter


def main():
    global lista_de_imagenes
    foldername = 'cap_jul7'
    print('>>> Exportando nombres de la carpeta %s'%foldername)
    lista_de_imagenes = directorio_img('./%s/'%foldername)
    print('>>> Reconociendo Texto de las Imagenes ...')
    cadena_textos_original, cadena_textos = generar_cadena_textos(lista_de_imagenes)
    print('>>> Procesando')
    data = contar(cadena_textos_original, cadena_textos)
    dataframe = puntaje(data)
    dataframe = depurar(dataframe)
    dataframe.to_csv('./output/output_%s.txt'%foldername,index=False)
    print(dataframe)

if __name__ == '__main__':
    main()