""""
Programa de Extraccion de caracteristicas
Contiene
"""
import cv2 #Opencv 3.000 a 32bits
import numpy as np
from Read import search, imageMatrix
import time
from matplotlib import pyplot as plt
from Segment import cont, cutt
from skimage.transform import rotate
"""Carpetas 008, B007, 018, 030, 029"""
start_time = time.time()


path = search('Data/003', 'multi')[0] #Buscar Path donde se encuentran las imagenes RAW
imatrix = imageMatrix(path)
p = 0
i = 2
ang = 0
img = np.copy(imatrix.image[p][i])
img = rotate(img,ang)
img, contours = cont(img, t=2,screenpercent=0.6)
print("--- %s seconds ---" % (time.time() - start_time))
cut, normcontor = cutt(rotate(imatrix.image[p][i],ang), contours, True)
centrado = normcontor-normcontor.mean(axis=0)


r = (centrado[:, 1]**2 + centrado[:, 0]**2)**0.5
theta = np.arctan2(centrado[:, 1], centrado[:, 0])-np.pi/2
#
# r = r.tolist()
# theta = theta.tolist()
# r.sort(key=dict(zip(r, theta)).get)
# theta.sort()

# Plots
f = plt.figure()

f1 = f.add_subplot(223)
f1.plot(theta, r)


f2 = f.add_subplot(224, polar=True)
f2.plot(theta, r)


f3 = f.add_subplot(221)
f3.imshow(rotate(imatrix.image[p][i],ang), cmap='gray', interpolation='none')

f3.plot(contours[:, 1], contours[:, 0], linewidth=2)

f4 = f.add_subplot(222)
f4.imshow(cut, cmap='gray', interpolation='none')
f4.plot(normcontor[:, 1], normcontor[:, 0], linewidth=2)

print np.mean(r)/np.median(r), np.mean(r), np.std(r), (np.sum(r))/(1280*960)
plt.show()
