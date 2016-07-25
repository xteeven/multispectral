import cv2
import os
import numpy as np
from PIL import Image


def rawRead(path):
    """
    Leer Raw y Normalizar a 16b de profundidad
    """
    datosRaw = open(path, 'rb').read()
    imagenRaw = Image.fromstring('F', (1280, 960), datosRaw, 'raw', 'F;16')
    imagenRaw = np.asanyarray(imagenRaw, dtype='uint16')
    imagenRaw *= (2 ** 16) / imagenRaw.max()
    return imagenRaw



def createMatrix(path):
    """"
    Crear Matriz con primera coordenada polarizacion, segunda coordenada longitud de onda de forma ascendente
            |   0   |   1   |   2   |   3   |   4   |   5   |   6   |   7   |
        0   |0, 417 |0,447  |0,477  |0,525  |0,671  |0,736  |0,891  |0,997  |
        1   |45,417 |...
        2   |90,417 |...
    es decir: Matriz[Polarizacion,Wavelength]
    """
    filesbypol = []
    imagematrix = []
    files = os.listdir(path)
    filesbypol.append(files[0:8])
    filesbypol.append(files[8:16])
    filesbypol.append(files[16:24])
    for column in range(0,3):
        imagerows = []
        [imagerows.append(rawRead(path + '/' + row)) for row in filesbypol[column]]
        print column
        imagematrix.append(imagerows)
    return imagematrix

path = []

path.append('Data/008/3621/07032015/3621BRAZOIZQUIERDO/multi')
path.append('Data/B007/11022015/multi')
path.append('Data/018/3629/07072015/3629AXILAIZQUIERDA/multi')
path.append('Data/030/3639/07102015/ESCAPULARDERECHASUPERIOR/multi')
path.append('Data/029/3639/07102015/ESCAPULARDERECHAINFERIOR/multi')


#datosimg = files[i].split("-") # 0. ) 1.Longitud de Onda 2. ? 3. ?


imatrix = createMatrix(path[4])

cv2.imshow('2', imatrix[2][7])


cv2.waitKey()
