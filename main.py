import cv2
import removeFlash
import removeBackground
import numpy as np

i = cv2.imread('./assets/processedImages/image1-backgroundRemoved-mean-neightbours-removed.jpg')
i2 = cv2.imread('./assets/processedImages/image2-backgroundRemoved-mean-neightbours-removed.jpg')
PCB1 = cv2.imread('./assets/PCB 1.jpg')
PCB2 = cv2.imread('./assets/PCB 2.jpg')



# orignal = i.copy()
# iGrayScale = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
# cv2.imshow("iGrayScale", iGrayScale)
# b = cv2.bilateralFilter(i,255,2,50)
# cv2.imshow("bilateralFilter", b)
# threshold, binaryThreshold = cv2.threshold(iGrayScale, 100, 255, cv2.THRESH_BINARY)
# adaptiveThreshold = cv2.adaptiveThreshold (iGrayScale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 10)
# cv2.imshow("adaptiveThreshold", adaptiveThreshold)




# flashless = removeFlash.remove(i2, 5, 'mean')
# backgroundClearedImage = removeBackground.removedBasedOnPixels(flashless[1])
# backgroundClearedImage = removeBackground.removeSinglePixelsWithWhiteNeighbours(backgroundClearedImage, 5)
# cv2.imwrite("image2-backgroundRemoved-mean-neightbours-removed-5.jpg", backgroundClearedImage)

'''
check first pixel from each side of the image to get a rectangle/square shaped roi. The pixel will have to be a pixel that has not all white neighbours
this is to deal with scenerios where a single pixel is present in the background in a case where the background is not fully removed
'''


def getRGBValueOfNeighbours(img, y, x):
    return [img[y - 1, x].tolist(), img[y + 1, x].tolist(), img[y, x - 1].tolist(), img[y, x + 1].tolist(),
            img[y + 1, x + 1].tolist(), img[y + 1, x - 1].tolist(), img[y - 1, x + 1].tolist(),img[y - 1, x - 1].tolist()]


def getROIOfImageWithBackgroundRemoved(image, drawCircle):
    img = image.copy()

    height = img.shape[0]
    width = img.shape[1]

    pixelCoordinates = {}

    # loop over the image, pixel by pixel

#find the top
    break_loop = False
    for y in range(1, height - 1):
        if break_loop: break
        for x in range(1, width - 1):
            if break_loop: break

            #if the pixel is not white
            if (img[y, x].tolist() != [255, 255, 255]):
                # if the pixel has no white neighbours, avoids use single pixel from bad background removal
                neighbour_rgb_values = getRGBValueOfNeighbours(img, y, x)
                sorted_neighbour_rgb_values = sorted(neighbour_rgb_values)
                # if [255, 255, 255] not in neighbour_rgb_values:
                #     img[y, x] = [0, 0, 255]

                if sorted_neighbour_rgb_values[len(sorted_neighbour_rgb_values) - 3] < [240, 240, 240]:
                    img[y, x] = [0, 0, 255]
                    pixelCoordinates['top'] = [y, x]
                    if drawCircle: cv2.circle(img,(x, y), 10, (255,0,0), -1)

                    break_loop = True

    #right sid
    break_loop = False
    for x in range(width - 2, 5, - 1):
        if break_loop: break
        for y in range(1, height - 1):
            if break_loop: break
            neighbour_rgb_values = getRGBValueOfNeighbours(img, y, x)
            sorted_neighbour_rgb_values = sorted(neighbour_rgb_values)

            if sorted_neighbour_rgb_values[len(sorted_neighbour_rgb_values) - 3] < [240, 240, 240]:
                img[y, x] = [0, 0, 255]
                pixelCoordinates['right'] = [y, x]
                if drawCircle: cv2.circle(img, (x, y), 10, (0, 255, 0), -1)


                break_loop = True


    #find the left hand side
    break_loop = False
    for x in range(1, width - 1):
        if break_loop: break
        for y in range(1, height - 1):
            if break_loop: break
            neighbour_rgb_values = getRGBValueOfNeighbours(img, y, x)
            sorted_neighbour_rgb_values = sorted(neighbour_rgb_values)

            if sorted_neighbour_rgb_values[len(sorted_neighbour_rgb_values) - 3] < [240, 240, 240]:
                img[y, x] = [0, 0, 255]
                pixelCoordinates['left'] = [y, x]
                if drawCircle: cv2.circle(img, (x, y), 10, (0, 0, 255), -1)

                break_loop = True

    #find bottom
    break_loop = False
    for y in range(height - 2, 2, -1):
        if break_loop: break
        for x in range(1, width - 1):
            if break_loop: break

            if (img[y, x].tolist() != [255, 255, 255]):
                neighbour_rgb_values = getRGBValueOfNeighbours(img, y, x)
                sorted_neighbour_rgb_values = sorted(neighbour_rgb_values)

                if sorted_neighbour_rgb_values[len(sorted_neighbour_rgb_values) - 3] < [240, 240, 240]:
                    img[y, x] = [0, 0, 255]
                    pixelCoordinates['bottom'] = [y, x]
                    if drawCircle: cv2.circle(img, (x, y), 10, (40, 40, 200), -1)

                    break_loop = True

    return pixelCoordinates, img



cords1, img1 = getROIOfImageWithBackgroundRemoved(i, True)
cords2, img2 = getROIOfImageWithBackgroundRemoved(i2, True)

PCB1_flashed_removed = removeFlash.remove(PCB1, 5, 'avg')
PCB2_flashed_removed = removeFlash.remove(PCB2, 5, 'avg')

print(cords1)
cv2.imshow("1", PCB1_flashed_removed[1][cords1['top'][0]:cords1['bottom'][0], cords1['left'][1] : cords1['right'][1]])
cv2.imshow("2", PCB2_flashed_removed[1][cords1['top'][0]:cords2['bottom'][0], cords2['left'][1] : cords2['right'][1]])

cv2.imshow("1", PCB1_flashed_removed[1][cords1['top'][0]:cords1['bottom'][0], cords1['left'][1] : cords1['right'][1]])
cv2.imshow("2", PCB2_flashed_removed[1][cords1['top'][0]:cords2['bottom'][0], cords2['left'][1] : cords2['right'][1]])

# adaptiveThreshold = cv2.adaptiveThreshold(cv2.cvtColor(backgroundClearedImage, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 10)
# cv2.imshow("adaptiveThreshold", adaptiveThreshold)

# for y in range(width, 1, -1): print(y)
key = cv2.waitKey(0)

