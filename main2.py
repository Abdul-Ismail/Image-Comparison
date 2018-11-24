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

# image1_roi = cv2.imread('./assets/l1.png')
# image2_roi = cv2.imread('./assets/l2.png')

# img = img[y:y + 50, x:x + 50]
# img = img[y:y + 50, x:x + 50]

# img = cv2.cvtColor(image1_roi.copy(), cv2.COLOR_BGR2HSV)
# y = 1
# x = 1
# # white_region = cv2.inRange(img, (0, 0, 0), (180, 255, 100))
# white_region = cv2.inRange(img, (95, 0, 0), (96, 255, 255))
# ROI_white = cv2.bitwise_and(img, img, mask=white_region)
# cv2.imshow('ROI_white', white_region)
#
# img = cv2.cvtColor(image2_roi.copy(), cv2.COLOR_BGR2HSV)
# # white_region = cv2.inRange(img, (0, 0, 0), (180, 255, 100))
# white_region = cv2.inRange(img, (95, 0, 0), (96, 255, 255))
# ROI_white = cv2.bitwise_and(img, img, mask=white_region)
# cv2.imshow('ROI_whit2e', white_region)
# #
#
highlighted_difference_image1, highlighted_difference_image2 = differences.highligh_differences(image1_roi.copy(), image2_roi.copy(), 60, 60, 95, 100)
cv2.imshow('image1_roi', image1_roi)
cv2.imshow('image2_roi', image2_roi)

cv2.imshow('image1_roi_hi', highlighted_difference_image1)
cv2.imshow('image2_roi_hi', highlighted_difference_image2)



while True:
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyAllWindows()
        exit()