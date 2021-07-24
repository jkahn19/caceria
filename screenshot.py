import argparse as ap
import pyautogui as pg

parser = ap.ArgumentParser(description='Captura de pantallas de los regalos de lord mobile')

parser.add_argument('-n', '--num', dest="num_regalos", default=4, type=int, help='Cantidad de regalos por capturar')
args = parser.parse_args()

# settings
num_regalos = args.num_regalos
num_iteraciones = num_regalos // 4

sleep_time = 0.5
sleep_regalos = 2

# coordenadas en la pantalla
xscreen1, yscreen1 = 741, 1048
xscreen2, yscreen2 = 1516, 401

xguardar, yguardar = 1470, 380

xlordmobile, ylordmobile = 529, 1056

xregalo1, yregalo1 = 1666, 465
xregalo2, yregalo2 = 1666, 634
xregalo3, yregalo3 = 1666, 800
xregalo4, yregalo4 = 1666, 958

xborrar, yborrar = 1549, 229


# tiempo para correr el programa desde el terminal
pg.sleep(5)

for i in range(num_iteraciones):
    # tiempo de espera
    pg.sleep(sleep_time)


    # captura de pantalla
    pg.press('printscreen')
    pg.sleep(sleep_time)

    pg.moveTo(xscreen1, yscreen1)
    pg.sleep(sleep_time)
    
    pg.mouseDown()
    pg.sleep(sleep_time)
    
    pg.moveTo(xscreen2, yscreen2)
    pg.sleep(sleep_time)

    pg.mouseUp()
    pg.sleep(sleep_time)
    

    # guardar captura
    pg.click(xguardar, yguardar)
    pg.sleep(sleep_time)

    pg.press('enter')
    pg.sleep(sleep_time)

    # regresar a lord mobile
    pg.click(xlordmobile, ylordmobile)
    pg.sleep(sleep_time)


    # abrir regalos
    pg.click(xregalo1, yregalo1)
    pg.sleep(sleep_time)

    pg.click(xregalo2, yregalo2)
    pg.sleep(sleep_time)

    pg.click(xregalo3, yregalo3)
    pg.sleep(sleep_time)

    pg.click(xregalo4, yregalo4)
    pg.sleep(sleep_regalos)


    # borrar regalos abiertos
    pg.click(xborrar, yborrar)
    pg.sleep(sleep_regalos)