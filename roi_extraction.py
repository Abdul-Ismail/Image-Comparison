import cv2
import numpy as np

def splitYUV(img):
    YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(YUV)
    return v


def cropImage(img):
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
    return bottom, top, left, right


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


def scaleImage(img):
    image2 = cv2.imread('./assets/PCB 2.JPG')
    height = image2.shape[0]
    width = image2.shape[1]

    return cv2.resize(img, dsize=(width, height))


def crop_roi(img):
    img = img.copy()
    img = scaleImage(img)
    v = splitYUV(img.copy())
    V = removeFlash(v)
    bottom1, top1, left1, right1 = cropImage(v)
    image1_cropped = img[bottom1 - 50:top1 + 50, left1 - 50:right1 + 50]
    return image1_cropped


def crop_roi_flash_removed(img):
    img1 = img.copy()
    scaled = scaleImage(img1)
    v = splitYUV(scaled)
    cl = removeFlash(v)
    bottom1, top1, left1, right1 = cropImage(cl)
    cl_cropped = cl[bottom1 - 50:top1 + 50, left1 - 50:right1 + 50]
    return cl_cropped
