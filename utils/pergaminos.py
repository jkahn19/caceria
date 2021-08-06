import argparse as ap
import pyautogui as pg

parser = ap.ArgumentParser(description='Abrir pergaminos de Mision de Administracion')
parser.add_argument('-n', '--num', dest="num_pergaminos", default=1, type=int, help='Cantidad de pergaminos a abrir')
args = parser.parse_args()


# settings
num_pergaminos = args.num_pergaminos


sleep_time = 0.8


# coordenadas en la pantalla
xflecha, yflecha = 782, 327
xuso, yuso = 955, 654
xmisionAdm, ymisionAdm = 1619, 431



# tiempo para correr el programa desde el terminal
pg.sleep(5)

for i in range(num_pergaminos):
    # tiempo de espera
    pg.sleep(sleep_time)
    
    #abrir mision de admin
    pg.click(xflecha, yflecha)
    pg.sleep(sleep_time)

    #usar pergamino
    pg.click(xuso, yuso)
    pg.sleep(sleep_time)

    for j in range (9):

        # abrir pergaminos
        pg.click(xmisionAdm, ymisionAdm)
        pg.sleep(sleep_time)




# joseph@sophia MINGW64 ~/Desktop/lord_mobile_app (main)
# $ python pergaminos.py
# Point(x=782, y=327)
# Point(x=955, y=654)
# Point(x=1619, y=431)
