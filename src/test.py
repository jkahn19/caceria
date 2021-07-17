import pytesseract
import cv2
import time
import sys
import os
import numpy as np

name = 'prueba0'
filename = './img/%s.png'%name
kernel = np.ones((5,5),np.uint8)

figura0 = cv2.imread(filename)
figura1 = cv2.cvtColor(figura0, cv2.COLOR_BGR2GRAY)
figura2 = cv2.threshold(figura1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
figura3 = cv2.medianBlur(figura1, 5)
figura4 = cv2.dilate(figura1, kernel, iterations = 1)
figura5 = cv2.erode(figura1, kernel, iterations = 1)

custom_config = r'--oem 3 --psm 11'

texto0 = pytesseract.image_to_string(figura0, lang='spa', config=custom_config)
texto1 = pytesseract.image_to_string(figura1, lang='spa', config=custom_config)
texto2 = pytesseract.image_to_string(figura2, lang='spa', config=custom_config)
texto3 = pytesseract.image_to_string(figura3, lang='spa', config=custom_config)
texto4 = pytesseract.image_to_string(figura4, lang='spa', config=custom_config)
texto5 = pytesseract.image_to_string(figura5, lang='spa', config=custom_config)


print(texto0)
print('figura0')
print('==========')
print(texto1)
print('figura1')
print('==========')
print(texto2)
print('figura2')
print('==========')
print(texto3)
print('figura3')
print('==========')
print(texto4)
print('figura4')
print('==========')
print(texto5)
print('figura5')


cv2.imwrite('./img/%s_save0.png'%name, figura0)
cv2.imwrite('./img/%s_save1.png'%name, figura1)
cv2.imwrite('./img/%s_save2.png'%name, figura2)
cv2.imwrite('./img/%s_save3.png'%name, figura3)
cv2.imwrite('./img/%s_save4.png'%name, figura4)
cv2.imwrite('./img/%s_save5.png'%name, figura5)