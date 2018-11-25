import roi_extraction
import differences
import cv2
import numpy as np
import removeFlash

image1 = cv2.imread('./assets/fifa1.jpg')
image2 = cv2.imread('./assets/fifa2.jpg')



def scaleImage(img):
    image2 = cv2.imread('./assets/PCB 2.JPG')
    height = image2.shape[0]
    width = image2.shape[1]

    return cv2.resize(img, dsize=(width, height))


image1 = scaleImage(image1)
image2 = scaleImage(image2)

red, image1 = removeFlash.remove(image1, 1, 'avg')
red, image2 = removeFlash.remove(image2, 1, 'avg')


image1_roi, image1_cropped_cords = roi_extraction.crop_roi(image1)
image2_roi, image2_cropped_cords = roi_extraction.crop_roi(image2)

print(image1_cropped_cords, image2_cropped_cords)

highlighted_difference_image1, highlighted_difference_image2 = differences.highligh_differences(image1_roi.copy(), image2_roi.copy(), 60, 60, 95, 150, image1_cropped_cords, image2_cropped_cords, image1.copy(), image2.copy())
cv2.imshow('image1_roi', image1_roi)
cv2.imshow('image2_roi', image2_roi)

cv2.imshow('image1_roi_hi', highlighted_difference_image1)
cv2.imshow('image2_roi_hi', highlighted_difference_image2)


while True:
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyAllWindows()
        exit()