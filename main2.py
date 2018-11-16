import roi_extraction
import differences
import cv2
import numpy as np

image1 = cv2.imread('./assets/PCB 1.JPG')
image2 = cv2.imread('./assets/PCB 2.JPG')

image1_roi = cv2.imread('./assets/pic1.jpg')
image2_roi = cv2.imread('./assets/pic2.jpg')

# image1_roi = roi_extraction.crop_roi(image1)
# image2_roi = roi_extraction.crop_roi(image2)


# highlighted_difference_image1, highlighted_difference_image2 = differences.highligh_differences(image1_roi, image2_roi, 30, 30, 80)
highlighted_difference_image1, highlighted_difference_image2 = differences.highligh_differences_grey_scale(image1_roi, image2_roi, 30, 30, 50)


cv2.imshow('image1_roi', highlighted_difference_image1)
cv2.imshow('image2_roi', highlighted_difference_image2)



while True:
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyAllWindows()
        exit()