import pytesseract
import cv2
import numpy as np

def extraer_texto_original(filename):
    '''
    Abre la imagen que vamos aprocesar y obtiene su escala en gris

    retorna la cadena de texto de la imagen por filtar
    '''
    img_input = cv2.imread(filename)
    figure = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.uint8)
    figure = cv2.dilate(figure, kernel, iterations = 1)
    custom_config = r'--oem 3 --psm 11'
    texto = pytesseract.image_to_string(figure, lang='spa', config=custom_config)
    texto = texto.lower()
    texto = texto.replace('ú','u')
    texto = texto.replace('í','i')
    texto = texto.replace('é','e')
    return texto

def extraer_texto(filename):
    '''
    Abre la imagen que vamos aprocesar y obtiene su escala en gris

    retorna la cadena de texto de la imagen por filtar
    '''
    img_input = cv2.imread(filename)
    figura = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
    figura = cv2.medianBlur(figura, 5)
    custom_config = r'--oem 3 --psm 11'
    texto = pytesseract.image_to_string(figura, lang='spa', config=custom_config)
    texto = texto.lower()
    texto = texto.replace('ú','u')
    texto = texto.replace('í','i')
    return texto