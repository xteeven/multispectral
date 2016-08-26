import cv2
import os
import numpy as np
from PIL import Image
import time
start_time = time.time()



def rawRead(path):
    """
    Leer Raw y Normalizar a 16b de profundidad
    """
    datosRaw = open(path, 'rb').read()
    imagenRaw = Image.frombytes('F', (1280, 960), datosRaw, 'raw', 'F;16')
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
        imagematrix.append(imagerows)
    return imagematrix

def avgPol(matrix, polarizacion):
    """
    :param matrix: Matriz generada con el metodo createMatrix
    :param polarizacion: [0-2] tipo de polarizacion
    :return:
    Devuelve la intensidad promedio para una polarizacion especifica
    """
    if polarizacion<3:
        outprom = matrix[0][0] * 0
        for i in range(0, 8):
            outprom += matrix[polarizacion][i] / 8
        return outprom
    else:
        avgotsu = uint16to8(matrix[0][0] * 0)
        for i in range(0, 3):
            outsu = avgPol(matrix, i)
            outsu = uint16to8(outsu)
            a, outsu = cv2.threshold(outsu, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            avgotsu += outsu / 3
        return avgotsu

def uint16to8(inputt): return np.asanyarray(inputt/250, dtype="uint8")

def search(pathe, folder):
    """
    Busqueda De carpetas al interior de los directorios que contienen las imagenes
    :pathe: Directorio en el cual se desea buscar
    :folder: Nombre de la carpeta que se desea encontrar
    Devuelve array con la totalidad de coincidencias encontradas
    """

    directorios = [x[0] if x[0].split('\\')[-1] == folder else '' for x in os.walk(pathe)]
    while '' in directorios:
        directorios.remove('')
    return directorios


"""Carpetas 008, B007, 018, 030, 029"""


path = search('Data/022', 'multi')[0]

imatrix = createMatrix(path)
avgotsu = avgPol(imatrix,8)
cv2.imshow('1', imatrix[2][2])
#cv2.imshow('2', avgotsu)

print("--- %s seconds ---" % (time.time() - start_time))
cv2.waitKey()
