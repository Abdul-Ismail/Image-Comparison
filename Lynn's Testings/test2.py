import cv2
import numpy as np

image1 = cv2.imread('../assets/PCB 1.JPG')
image2 = cv2.imread('../assets/PCB 2.JPG')


def splitYUV(img):
    YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(YUV)
    return v


def cropImage(img , img2):
    height = img.shape[0]
    width = img.shape[1]

    bottom = height
    top = 0
    left = width
    right = 0

    for y in range(0, height):
        for x in range(0, width):
            if np.any(img[y, x] < 100):
                if y > top:
                    top = y

                if y < bottom:
                    bottom = y

                if x > right:
                    right = x

                if x < left:
                    left = x
    img2 = img[bottom - 50:top + 50, left - 50:right + 50]
    return cv2.resize(img2, dsize=(int(550), int(456)))


def removeFlash(img):
    # grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dilated_grayscaled = cv2.dilate(img, np.ones((7, 7), np.uint8))
    background_img = cv2.medianBlur(dilated_grayscaled, 21)
    difference = 255 - cv2.absdiff(img, background_img)

    norm_img = difference.copy()
    cv2.normalize(difference, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
    result2 = cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

    return clahe.apply(result2)

def makePixelsDarker(img):
    height = img.shape[0]
    width = img.shape[1]

    for y in range(0, height):
        for x in range(0, width):

            if np.any(img[y, x] < 100):
                img[y, x] = img[y, x] - 20

            # if np.any(img[y, x] > 230):
            #     img[y, x] = 255
    return img


def compare(img1, img2):
    height = img1.shape[0]
    width = img1.shape[1]

    for y in range(0, width, 30):
        for x in range(0, height, 30):
            if (img1[x:x+30, y:y+30].mean() > (img2[x:x+30, y:y+30].mean() + 30))or (img1[x:x+30, y:y+30].mean() < (img2[x:x+30, y:y+30].mean() - 30)):
                img1[x:x + 30, y:y + 30] = 0
    return img1


def scaleImage(img, img2):
    height = img.shape[0]
    width = img.shape[1]

    return cv2.resize(img2, dsize=(width, height))

v1 = splitYUV(image1)
v2 = splitYUV(image2)

crop1 = cropImage(v1, image1)
crop2 = cropImage(v2, image2)

cl1 = removeFlash(crop1)
cl2 = removeFlash(crop2)

cv2.imwrite('./saved/pic1.jpg', cl1)
cv2.imwrite('./saved/pic2.jpg', cl2)

# cv2.imshow('cl', cl1)
# cv2.imshow('cl2', cl2)

# og1 = scaleImage(cl1)
# cv2.imshow('scaled', og1)

#
# compared = compare(cl1, cl2)
# # compare(cl1, cl2)

# og2 = scaleImage(cl2)
# difference = scaleImage(compared)
#
# cv2.imshow('og1', og1)
# cv2.imshow('og2', og2)
# cv2.imshow('difference', difference)

cv2.imshow('cropped1', cl1)
cv2.imshow('cropped2', cl2)

# cv2.imshow('v', v2)
# cv2.imshow('u', u)

while True:
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyAllWindows()
        exit()