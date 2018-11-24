import roi_extraction
import differences
import cv2
import numpy as np
import removeFlash

image1 = cv2.imread('./assets/PCB 1.jpg')
image2 = cv2.imread('./assets/PCB 2.jpg')

# red, image1 = removeFlash.remove(image1, 5, 'avg')
# red, image2 = removeFlash.remove(image2, 5, 'avg')

image1_roi = roi_extraction.crop_roi(image1)
image2_roi = roi_extraction.crop_roi(image2)


highlighted_difference_image1, highlighted_difference_image2 = differences.highligh_differences(image1_roi.copy(), image2_roi.copy(), 60, 60, 95, 100)
cv2.imshow('image1_roi', image1_roi)
cv2.imshow('image2_roi', image2_roi)

cv2.imshow('image1_roi_hi', highlighted_difference_image1)
cv2.imshow('image2_roi_hi', highlighted_difference_image2)

while True:
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyAllWindows()
        exit()