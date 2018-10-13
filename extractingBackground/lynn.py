import cv2
import numpy as np
import matplotlib.pyplot as plt

# img = cv2.imread('./assets/PCB 1.JPG')
# img2 = cv2.imread('./assets/PCB 2.JPG')

img2 = cv2.imread('./assets/4.png')
height, width, d = img2.shape

# mask = np.zeros(img.shape[:2], np.uint8)
mask = np.zeros(img2.shape[:2], np.uint8)

# outputs an array with one line and 65 columns, filled with zeros. np.float means the zeros have a decimal point.﻿
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# rect = (175, 110, 650, 465)
# rect2 = (170, 40, 490, 410)
rect2 = (0, 0, height, width)

# bgdModel - Temporary array for background, 5 - Number of iterations,GC_INIT_WITH_RECT - Initiative using our rectangle
# cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
cv2.grabCut(img2, mask, rect2, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')

# img = img*mask2[:, :, np.newaxis]
img2 = img2*mask2[:, :, np.newaxis]

# plt.imshow(img, 'gray')
plt.imshow(img2, 'gray')
# plt.colorbar()
plt.show()

# cv2.imwrite('./assets/PCB2.jpg', img2)
# cv2.imshow('img', img)
# cv2.imshow('img2', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()