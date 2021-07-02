import os

def directorio_img(directory_name):
    lista_imagenes = os.listdir(directory_name)

    lista_imagenes_filtrada = []
    for i_imagen in range(len(lista_imagenes)):
        if '.png' in lista_imagenes[i_imagen]:
            lista_imagenes_filtrada.append( directory_name + lista_imagenes[i_imagen])
    
    return lista_imagenes_filtrada