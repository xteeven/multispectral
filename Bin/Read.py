"""
Conjunto de funciones Aplicadas para Leer Organizar y buscar Carpetas Y Directorios
Contiene:
Lectura Raw
Busqueda En Directorios
Crear Matrices
"""


import os
import numpy as np
from PIL import Image


def rawRead(path):
    """
    Leer Raw y Normalizar a 16b de profundidad
    """
    datosRaw = open(path, 'rb').read()
    imagenRaw = Image.frombytes('F', (1280, 960), datosRaw, 'raw', 'F;16')
    imagenRaw = np.asanyarray(imagenRaw, dtype='uint16')
    imagenRaw *= (2 ** 16) / imagenRaw.max()
    return imagenRaw

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

class imageMatrix:
    def __init__(self, path):
        self.image = self.createMatrix(path)
        self.name = [["0, 417", "0, 447", "0, 477", "0, 525", "0, 671", "0, 736", "0, 891", "0, 997"],
              ["45, 417", "45, 447", "45, 477", "45, 525", "45, 671", "45, 736", "45, 891", "45, 997"],
              ["90, 417", "90, 447", "90, 477", "90, 525", "90, 671", "90, 736", "90, 891", "90, 997"]]

    def createMatrix(self, path):
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


