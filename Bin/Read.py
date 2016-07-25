import cv2
import os
import numpy as np
from PIL import Image

def rawRead(path):
    datosRaw = open(path, 'rb').read()
    imagenRaw = Image.fromstring('F', (1280, 960), datosRaw, 'raw', 'F;16')
    imagenRaw = np.asanyarray(imagenRaw, dtype='uint16')
    imagenRaw *= (2 ** 16) / imagenRaw.max()
    return imagenRaw

path1 = 'Data/008/3621/07032015/3621BRAZOIZQUIERDO/multi'
path2 = 'Data/B007/11022015/multi'
path3 = 'Data/018/3629/07072015/3629AXILAIZQUIERDA/multi'
path4 = 'Data/030/3639/07102015/ESCAPULARDERECHASUPERIOR/multi'


imagen = rawRead('3-997-900-258-SKIN.raw')


cv2.imshow('3', imagen)
cv2.waitKey()
