
"""
Programa de Segmentacion
Contiene
"""
import cv2 #Opencv 3.000 a 32bits
import numpy as np
from Read import search, imageMatrix
import time
from matplotlib import pyplot as plt
from Segment import cont, cutt

"""Carpetas 008, B007, 018, 030, 029"""
start_time = time.time()


path = search('Data/025', 'multi')[0] #Buscar Path donde se encuentran las imagenes RAW
imatrix = imageMatrix(path)
p = 0
i = 2
img = np.copy(imatrix.image[p][i])
img, contours = cont(img, t=2)
# hist1, bins = np.histogram(imatrix.image[p][i].ravel(), 65536, [0, 65536])
print("--- %s seconds ---" % (time.time() - start_time))


cut, normcontor = cutt(imatrix.image[p][i], contours, True)
centrado = normcontor-normcontor.mean(axis=0)
r = (centrado[:, 1]**2 + centrado[:, 0]**2)**0.5
theta = np.arctan2(centrado[:, 1],centrado[:, 0])


# Plots
f = plt.figure()

f1 = f.add_subplot(223)
f1.plot(theta+180, r)

f2 = f.add_subplot(224, polar=True)
# f2.plot(centrado[:, 1], centrado[:, 0])
f2.plot(theta+180, r)




f3 = f.add_subplot(221)
f3.imshow(imatrix.image[p][i], cmap='gray', interpolation='none')

f3.plot(contours[:, 1], contours[:, 0], linewidth=2)

f4 = f.add_subplot(222)
f4.imshow(cut, cmap='gray', interpolation='none')
f4.plot(normcontor[:, 1], normcontor[:, 0], linewidth=2)


plt.show()
