"""
Programa de Segmentacion
Contiene
"""
import cv2 #Opencv 3.000 a 32bits
import numpy as np
from Read import search, imageMatrix
import time
from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu
from scipy.ndimage import gaussian_filter
from skimage import measure
from skimage import filters
import math


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

def binarizar(imagen, valor):
    imagen[imagen > valor] = 2**16-1
    imagen[imagen < valor] = 0
    return imagen

def cont(imagen, depth=2**16, gaussian=3, screenpercent=0.7,t=0):

    imagen = gaussian_filter(imagen, gaussian)

    if t==0:
        otsu = threshold_otsu(imagen, depth)
    elif t==1:
        otsu = filters.threshold_isodata(imagen, depth)
    else:
        otsu = filters.threshold_li(imagen)
    imagen = binarizar(imagen, otsu)
    imagen = gaussian_filter(imagen, gaussian)

    contours = measure.find_contours(imagen, 1)
    centro = np.asanyarray([1280*0.5, 960*0.5])
    while len(contours) > 1:
        if sum(np.abs(centro - contours[1].mean(axis=0)) < [1280*screenpercent*0.5, 960*screenpercent*0.5]) != 2:
            del contours[1]
        elif sum(np.abs(centro - contours[0].mean(axis=0)) < [1280*screenpercent*0.5, 960*screenpercent*0.5]) != 2:
            del contours[0]
        else:
            if contours[1].size < contours[0].size:
                del contours[1]
            else:
                del contours[0]
    return imagen, contours[0]

def cutt(image, contorno, newcontour = False):
    corte = image[int(min(contorno[:, 0])):int(max(contorno[:, 0])),int(min(contorno[:, 1])):int(max(contorno[:, 1]))]
    newcont = contorno - (min(contorno[:, 0]), min(contorno[:, 1]))
    if newcontour:
        return corte, np.asarray(newcont)
    else:
        return corte

def polar(x,y):
  return math.hypot(x,y),math.degrees(math.atan2(y,x))

