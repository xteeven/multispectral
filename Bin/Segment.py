"""
Programa de Segmentacion
Contiene
"""
import cv2 #Opencv 3.000 a 32bits
import numpy as np
from Read import search, imageMatrix, Matrixnames
import time

start_time = time.time()

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

"""Carpetas 008, B007, 018, 030, 029"""


path = search('Data/022', 'multi')[0] #Buscar Path donde se encuentran las imagenes RAW

#imatrix = createMatrix(path) #Generar matriz de imagen. Formato de salida descrito en el Source (Read.py)
imatrix = imageMatrix(path)

print("--- %s seconds ---" % (time.time() - start_time))
cv2.putText(imatrix.image[0][2], "Image: " + imatrix.name[0][2], (100, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, 255, 2)
cv2.imshow('1', imatrix.image[0][2])


cv2.waitKey()