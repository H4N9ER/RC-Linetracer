# -*- coding: utf-8 -*-
import socket
import sys
import os
import numpy as np
import pdb

import cv2
import time

from Image import *
from Utils import *

font = cv2.FONT_HERSHEY_SIMPLEX
direction = 0

#N_SLICES만큼 이미지를 조각내서 Images[] 배열에 담는다
Images=[]
N_SLICES = 3

for q in range(N_SLICES):
    Images.append(Image())

img = cv2.imread('dave.jpg')

if img is not None:
    #이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
    Points = SlicePart(img, Images, N_SLICES)
    print('Points : ', Points)

    #N_SLICES 개의 무게중심 점을 x좌표, y좌표끼리 나눈다
    x = Points[::2]
    y = Points[1::2]

    #조각난 이미지를 한 개로 합친다
    fm = RepackImages(Images)
    
    #완성된 이미지를 표시한다
    cv2.imshow("Vision Race", fm)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
else:
    print('not even processed')

