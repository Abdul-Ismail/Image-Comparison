import roi_extraction
import differences
import cv2
import numpy as np
import removeFlash
import removeBackground

image1 = cv2.imread('./assets/rubrik1.jpg')
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

# image1 = removeBackground.removedBasedOnPixels(image1)


'''
grab coords for top section, left section, right section and bottom section by a given width
pixel values of these coordinates will be put into an array and it will be used it to remove the background
we will loop through the pixels and remove any pixel that has a color value which is present in the array
'''

def get_medium_pixel_value_for_background(img, sampleSize):
    height= img.shape[0]
    width = img.shape[1]
    pixelColors = []

    # loop over the image, pixel by pixel
    for y in range(0, height):
        for x in range(0, sampleSize):
            pixelColors.append(img[y, x].tolist())

    for y in range(0, height):
        for x in range(width - 1, width - sampleSize, -1):
            pixelColors.append(img[y, x].tolist())

    for x in range(0, width):
        for y in range(0, sampleSize):
            pixelColors.append(img[y, x].tolist())

    for x in range(0, width):
        for y in range(height - 1, height - sampleSize, -1):
            pixelColors.append(img[y, x].tolist())

    #get medium
    pixelColors.sort()
    # print(pixelColors)
    middleIndex = int( len(pixelColors) / 2 )
    medium = pixelColors[middleIndex]

    return medium


def get_upper_and_lower_values_for_HSV(hsv_value):

    lower = (hsv_value[0] - 5, 0, 0)
    upper = (hsv_value[0] + 5, 255 , 255)

    return {
        'lower': lower,
        'upper': upper
    }


def scaleImage(img):
    image2 = cv2.imread('./assets/PCB 1.JPG')
    height = image2.shape[0]
    width = image2.shape[1]

    return cv2.resize(img, dsize=(width, height))

image1 = scaleImage(image1)
medium_pixel_value = get_medium_pixel_value_for_background(image1, 30)
inRange = get_upper_and_lower_values_for_HSV(medium_pixel_value)
print(inRange)

white_region = cv2.inRange(image1, inRange['lower'], inRange['upper'])
ROI_white = cv2.bitwise_and(image1, image1, mask=white_region)
cv2.imshow('white_region', white_region)
cv2.imshow('ROI_whit2e', ROI_white)


# cv2.imshow('image2_roi_hi', image1)
#
while True:
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyAllWindows()
        exit()