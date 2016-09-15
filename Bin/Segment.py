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

def binarizar(imagen, valor):
    imagen[img > valor] = 2**16-1
    imagen[img < valor] = 0
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
    # print contours[0].mean(axis=0), [1280*screenpercent, 960*screenpercent], np.abs(centro - contours[0].mean(axis=0))
    return imagen, contours

"""Carpetas 008, B007, 018, 030, 029"""


path = search('Data/025', 'multi')[0] #Buscar Path donde se encuentran las imagenes RAW


imatrix = imageMatrix(path)
p = 0
i = 2
img = np.copy(imatrix.image[p][i])
img, contours = cont(img, t=0)
# print contour.mean(axis=0)
# print contour2.mean(axis=0)
hist1, bins = np.histogram(imatrix.image[p][i].ravel(), 65536, [0, 65536])
hist2, bins1 = np.histogram(img.ravel(), 65536, [0, 65536])
print("--- %s seconds ---" % (time.time() - start_time))







# Plots
f = plt.figure()

f1 = f.add_subplot(223)
f1.plot(hist1)

f2 = f.add_subplot(224)
f2.plot(hist2)

f3 = f.add_subplot(221)
f3.imshow(imatrix.image[p][i], cmap='gray', interpolation='none')

# f3.imshow(img2, cmap='gray', interpolation='none')
for n, contour in enumerate(contours):
    f3.plot(contour[:, 1], contour[:, 0], linewidth=2)

f4 = f.add_subplot(222)
# f4.imshow(img, cmap='gray', interpolation='none')
f4.imshow(img, cmap='gray', interpolation='none')
# f3.imshow(img2, cmap='gray', interpolation='none')

plt.show()
