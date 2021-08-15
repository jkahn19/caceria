from src.abrir import *
from src.imagenes import *
import pandas as pd
import re
import os

#from difflib import SequenceMatcher as S
import difflib

import argparse as ap

parser = ap.ArgumentParser(description='Conteo de Imagenesde caceria de Lord Mobile')

parser.add_argument('-f', '--folder', dest="foldername", default='test', type=str, help='Nombre del folder')
parser.add_argument('-e', '--error', dest="falgerror", default=False, type=bool, action=ap.BooleanOptionalAction, help='Flag para agregar las imagenes no contabilizadas')
args = parser.parse_args()


palabras_claves = ['botin de', 'regalo de']
diccionario_nivel = {'comun': 1, 'poco comun': 2, 'raro': 3, 'epico': 4}
puntaje = {1:1, 2:4, 3:16}
lista_de_imagenes = []

filename_miembros = './data/miembros-D_S.csv'
df_D_S = pd.read_csv(filename_miembros)


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
        error = False
    return conteo, error

def contar(cadena_textos_original, cadena_textos):
    global lista_de_imagenes
    data = []
    img_error = []

    for i in range(len(cadena_textos)):
        #print('proceso %i/%i'%(i,len(cadena_textos)))
        data_img, agregar_bol = conteo_imagen(cadena_textos_original[i], cadena_textos[i])
        if agregar_bol:
            data += data_img
        else:
            img_error.append(lista_de_imagenes[i])
            print('>>> WARNNING : No se pudo reconocer el texto de %s\n'%lista_de_imagenes[i])

    data_frame = pd.DataFrame(data, columns = ['Nombre', 'Rareza'])

    return data_frame, img_error

def puntaje(data):
    dataframe = pd.DataFrame([], columns=['Nombre', 'N1', 'N2', 'N3', 'N4', 'Total', 'Puntaje'])
    dataframe['Nombre'] = data['Nombre'].unique()
    dataframe['Total'] = 0
    dataframe['Puntaje'] = 0


    for nombre in dataframe['Nombre']:
        numero_n1 = 0
        numero_n2 = 0
        numero_n3 = 0
        numero_n4 = 0
        total = 0
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
        total = numero_n1 + numero_n2 + numero_n3 + numero_n4

        dataframe.loc[dataframe['Nombre'] == nombre, 'N1'] = numero_n1
        dataframe.loc[dataframe['Nombre'] == nombre, 'N2'] = numero_n2
        dataframe.loc[dataframe['Nombre'] == nombre, 'N3'] = numero_n3
        dataframe.loc[dataframe['Nombre'] == nombre, 'N4'] = numero_n4
        dataframe.loc[dataframe['Nombre'] == nombre, 'Total'] = total
        dataframe.loc[dataframe['Nombre'] == nombre, 'Puntaje'] = valor_puntaje

    return dataframe

def depurar_nombre(name):
    newname = name.strip()
    newname = re.sub(r'[.%+-]+', '', newname)
    newname = newname.replace(' ','')
    newname = newname.lower()
    return newname

def depurar(data):
    global df_D_S
    miembros = [nombre.lower() for nombre in df_D_S['Nombre'].to_list()]
    lista_caceria = data['Nombre'].to_list()

    df_filter = pd.DataFrame([], columns=['Nombre', 'N1', 'N2', 'N3', 'N4','Total', 'Puntaje'])
    df_filter['Nombre'] = df_D_S['Nombre']
    df_filter['N1'] = 0
    df_filter['N2'] = 0
    df_filter['N3'] = 0
    df_filter['N4'] = 0
    df_filter['Total'] = 0
    df_filter['Puntaje'] = 0

    rango = ['N1', 'N2', 'N3', 'N4','Total', 'Puntaje']
    for name in lista_caceria:
        name_coincidencia = difflib.get_close_matches(depurar_nombre(name), possibilities = miembros, n=1, cutoff = 0.6)
        if len(name_coincidencia) == 0:
            print('>> WARNNING: nombre no encontrad%s'%name)
        else:
            name_coincidencia = name_coincidencia[0]
            filtro = df_filter['Nombre'].apply(lambda s: s.lower() if type(s) == str else s)==name_coincidencia
            valores = data.loc[data['Nombre']==name]
            df_filter.loc[filtro, 'N1'] += valores['N1'].values[0]
            df_filter.loc[filtro, 'N2'] += valores['N2'].values[0]
            df_filter.loc[filtro, 'N3'] += valores['N3'].values[0]
            df_filter.loc[filtro, 'N4'] += valores['N4'].values[0]
            df_filter.loc[filtro, 'Total'] += valores['Total'].values[0]
            df_filter.loc[filtro, 'Puntaje'] += valores['Puntaje'].values[0]

    return df_filter


def add_error(args):
    try:
        df = pd.read_csv('./output/output_%s.txt'%args.foldername)
    except FileNotFoundError as e:
        print(e)
        print('>>> Comenzando por el conteo de imagenes')
        main(args)
        df = pd.read_csv('./output/output_%s.txt'%args.foldername)
    
    try:
        df_error = pd.read_csv('./%s/error/error.txt'%args.foldername)

        for name in df_error['Nombre'].values:
            filtro = df['Nombre'] == name
            valores = df_error.loc[df_error['Nombre']==name]
            df.loc[filtro, 'N1'] += valores['N1'].values[0]
            df.loc[filtro, 'N2'] += valores['N2'].values[0]
            df.loc[filtro, 'N3'] += valores['N3'].values[0]
            df.loc[filtro, 'N4'] += valores['N4'].values[0]
            df.loc[filtro, 'Total'] += valores['Total'].values[0]
            df.loc[filtro, 'Puntaje'] += valores['Puntaje'].values[0]

        df.to_csv('./output/output_%s_error.txt'%args.foldername, index=False)
    except FileNotFoundError as e:
        print(e)
        return 0

def main(args):
    global lista_de_imagenes
    foldername = args.foldername
    print('>>> Exportando nombres de la carpeta %s'%foldername)
    lista_de_imagenes = directorio_img('./%s/'%foldername)
    print('>>> Reconociendo Texto de las Imagenes ...')
    cadena_textos_original, cadena_textos = generar_cadena_textos(lista_de_imagenes)
    print('>>> Procesando\n')
    data, img_error = contar(cadena_textos_original, cadena_textos)
    print('>>> Conteo de caceria')
    dataframe = puntaje(data)
    dataframe = depurar(dataframe)
    print('>>> Guardando Resultados')
    dataframe.to_csv('./output/output_%s.txt'%foldername, index=False)
    n_error = len(img_error)
    if n_error != 0:
        # create error folder and move the images to the error folder
        print('>>> Moviendo Imagenes que no se pueden reconocer a la carpeta error')
        try:
            os.mkdir('./%s/error'%foldername)
        except OSError as error:
            print(">>> La carpeta './%s/error' ya existe "%foldername)
        for i in range(n_error):
            try:
                os.rename(img_error[i], img_error[i].replace('%s'%foldername, '%s/error'%(foldername)))
            except OSError as error:
                print('>>> WARNNING: verificar %s'%img_error[i])
        print('>>> Imagenes que no se han contado han sido reubicada en ./%s/error'%(foldername))

if __name__ == '__main__':
    if not args.falgerror:
        main(args)
    else:
        add_error(args)
        