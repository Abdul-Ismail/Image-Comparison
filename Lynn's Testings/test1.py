import cv2
import numpy as np

# img1 = cv2.imread('./assets/PCB 1.JPG')
# img2 = cv2.imread('./assets/PCB 2.JPG')
#
# # if images are the same then variable will be all 0s else not be all 0
# difference = cv2.subtract(img1, img2)
#
# # if difference returns all zeroes then this will return false
# # therefore we inverse it so that if it is the same then it will return true
# result = not np.any(difference)
#
# if result is True:
#     print("The images are the same")
# else:
#     cv2.imwrite("./assets/differences.jpg", difference)
#     print("The images are different")
#
# cv2.imshow('image1', img1)
# cv2.imshow('image2', img2)

# ########################## Part 2 #########################################

# image1 = cv2.imread('./assets/differences.jpg')
# grayscaled = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
# gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 155, 1)
#
# # img2gray = cv2.cvtColor(gaus, cv2.COLOR_BGR2GRAY)
#
# cv2.imshow('gaus', gaus)
# cv2.imwrite('./assets/gaus.jpg', gaus)

# ########################## Part 3 #########################################

image1 = cv2.imread('./assets/differences.jpg')

img2gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 50, 255, cv2.THRESH_BINARY_INV)


cv2.imshow('img2gray', img2gray)
cv2.imshow('mask', mask)

# cv2.imwrite('./assets/changes.jpg', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()