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
from scipy.interpolate import interp1d
"""Carpetas 008, B007, 018, 030, 029"""
start_time = time.time()


path = search('Data/030', 'multi')[0] #Buscar Path donde se encuentran las imagenes RAW
imatrix = imageMatrix(path)
p = 0
i = 2
ang = 0
img = np.copy(imatrix.image[p][i])
img = rotate(img,ang)
img, contours = cont(img, t=2,screenpercent=0.6)
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
cut, normcontor = cutt(rotate(imatrix.image[p][i],ang), contours, True)
centrado = normcontor-normcontor.mean(axis=0)


r = (centrado[:, 1]**2 + centrado[:, 0]**2)**0.5
theta = np.arctan2(centrado[:, 1], centrado[:, 0])-np.pi/2
#
print("--- %s seconds ---" % (time.time() - start_time))

# Plots
f = plt.figure('Segmentacion')
f1 = f.add_subplot(223)
f1.plot(theta, r)
f2 = f.add_subplot(224, polar=True)
f2.plot(theta, r)
f3 = f.add_subplot(221)
f3.imshow(imatrix.image[p][i], cmap='gray', interpolation='none')
f3.plot(contours[:, 1], contours[:, 0], linewidth=2)
f4 = f.add_subplot(222)
f4.imshow(cut, cmap='gray', interpolation='none')
f4.plot(normcontor[:, 1], normcontor[:, 0], linewidth=2)

m = plt.figure('Multiespectral')
sub = m.add_subplot(3, 7, 1)

start_time = time.time()
polardev = [[], [], []]
polarmean = [[], [], []]
for nimg in range(0, 24):
    sub = m.add_subplot(3, 8, 1+nimg)
    sub.set_xticks([])
    sub.set_yticks([])
    pol = nimg/8
    wave = nimg-(nimg/8)*8
    window = int(np.mean(r)/1.5)
    centerx, centery = int(contours.mean(axis=0)[0]), int(contours.mean(axis=0)[1])
    texture = imatrix.image[pol][wave][centerx-window:centerx+window, centery-window:centery+window]
    polardev[nimg/8].append(np.std(texture))
    polarmean[nimg/8].append(np.mean(texture))
    sub.imshow(texture, cmap='gray', interpolation='none')
    #sub.plot(contours[:, 1], contours[:, 0], linewidth=2)
    #print nimg/8, nimg-(nimg/8)*8, nimg+1, np.mean(texture)
print("--- %s seconds ---" % (time.time() - start_time))
polarmeant = plt.figure('Mean')
po = polarmeant.add_subplot(121)
plotfun1 = []
for ploter in range(3):
    plotfun1.append(interp1d(range(0, 8), polarmean[ploter], kind='cubic')(np.linspace(0, 7, num=80, endpoint=True)))
plotfun2 = []
for ploter in range(3):
    plotfun2.append(interp1d(range(0, 8), polardev[ploter], kind='cubic')(np.linspace(0, 7, num=80, endpoint=True)))

p1, = po.plot(plotfun1[0], label='Polarizacion 0 mean')
p2, = po.plot(plotfun1[1], label='Polarizacion 45 mean')
p3, = po.plot(plotfun1[2], label='Polarizacion 90 mean')
po.legend(handles=[p1, p2, p3], loc=4)
pob = polarmeant.add_subplot(122)
p1b, = pob.plot(plotfun2[0], label='Polarizacion 0 dev')
p2b, = pob.plot(plotfun2[1], label='Polarizacion 45 dev')
p3b, = pob.plot(plotfun2[2], label='Polarizacion 90 dev')
pob.legend(handles=[p1b, p2b, p3b], loc=2)
ticks = np.linspace(417, 997, len(pob.get_xticks().tolist()), dtype=int).tolist()
pob.set_xticklabels(ticks)
po.set_xticklabels(ticks)

print np.mean(r)/np.median(r), np.mean(r), np.std(r), (np.sum(r))/(1280*960)
plt.show()
