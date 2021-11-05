import argparse as ap
import pyautogui as pg

parser = ap.ArgumentParser(description='Abrir pergaminos de Mision de Administracion')
parser.add_argument('-n', '--num', dest="num_pergaminos", default=1, type=int, help='Cantidad de pergaminos a abrir')
args = parser.parse_args()


# settings
num_pergaminos = args.num_pergaminos


sleep_time = 0.8


# coordenadas en la pantalla
xuso, yuso = 946, 905



# tiempo para correr el programa desde el terminal
pg.sleep(5)

for i in range(num_pergaminos):
    # tiempo de espera
    pg.sleep(sleep_time)

    pg.click(xuso, yuso)
    pg.sleep(sleep_time)
