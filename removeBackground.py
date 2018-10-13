import cv2

'''
grab coords for top section, left section, right section and bottom section by a given width
pixel values of these coordinates will be put into an array and it will be used it to remove the background
we will loop through the pixels and remove any pixel that has a color value which is present in the array
'''

def getArrayOfRGBColorsFromSideOfImages(img):
    height= img.shape[0]
    width = img.shape[1]

    sideRGBColors = []
    inRange = 30

    limit = [200, 200, 200]

    # loop over the image, pixel by pixel
    for y in range(0, height):
        for x in range(0, inRange):
            # sideRGBColors.append(img[y, x].tolist())
            if (img[y, x].tolist() not in sideRGBColors) and img[y, x].tolist() < limit:
                sideRGBColors.append(img[y, x].tolist())

    for y in range(0, height):
        for x in range(width - 1, width - inRange, -1):
            # sideRGBColors.append(img[y, x].tolist())
            if (img[y, x].tolist() not in sideRGBColors) and img[y, x].tolist() < limit:
                sideRGBColors.append(img[y, x].tolist())

    for x in range(0, width):
        for y in range(0, inRange):
            # sideRGBColors.append(img[y, x].tolist())
            if (img[y, x].tolist() not in sideRGBColors) and img[y, x].tolist() < limit:
                sideRGBColors.append(img[y, x].tolist())

    for x in range(0, width):
        for y in range(height - 1, height - inRange, -1):
            # sideRGBColors.append(img[y, x].tolist())
            if (img[y, x].tolist() not in sideRGBColors) and img[y, x].tolist() < limit:
                sideRGBColors.append(img[y, x].tolist())

    return sideRGBColors


def whitenCoordinatesThatHaveRGBValueFromAGivenArray(colors, imgRef):
    img = imgRef.copy()
    height= img.shape[0]
    width = img.shape[1]

    sideRGBColors = []
    # loop over the image, pixel by pixel
    for y in range(0, height):
        for x in range(0, width):
            if (img[y, x].tolist() in colors):

                img[y, x] = [255, 255, 255]

    return img


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a


def getRangeOfPixels(pixels):
    sortedColors = sorted(pixels)
    return {
        'start': sortedColors[0],
        'end': sortedColors[len(sortedColors) - 1]
    }


def removedBasedOnPixels(image):
    img = image.copy()
    colors = getArrayOfRGBColorsFromSideOfImages(img)
    backgroundClearedImage = whitenCoordinatesThatHaveRGBValueFromAGivenArray(colors, img)
    return backgroundClearedImage


def removeSinglePixelsWithWhiteNeighbours(passedImage, amountOftimestoRemove):
    original = passedImage.copy()
    img = passedImage.copy()
    convertedImage = passedImage.copy()
    pixelsBRGThatChanged = []

    height = img.shape[0]
    width = img.shape[1]
    for i in range(amountOftimestoRemove):
        print('running', i)
        # loop through each pixel
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # if the pixel is white then it might be flash so check surrounding pixels
                if (img[y, x].tolist() != [255, 255, 255]):

                    # get bgr values for all of the surrouding pixels
                    RGB_values = [img[y - 1, x].tolist(), img[y + 1, x].tolist(), img[y, x - 1].tolist(), img[y, x + 1].tolist(),
                                  img[y + 1, x + 1].tolist(), img[y + 1, x - 1].tolist(), img[y - 1, x + 1].tolist(), img[y - 1, x - 1].tolist()]

                    sortedValue = sorted(RGB_values)

                    #if the last value is 255's means the whole array is 255's so the surrounding of the pixel is white
                    if (sortedValue[len(sortedValue) - 1] > [220, 220, 220]):
                        convertedImage[y, x] = [255, 255, 255]

                        if (img[y, x].tolist() not in pixelsBRGThatChanged):
                            pixelsBRGThatChanged.append(img[y, x].tolist())

        sortedPixelsBRGThatChanged = pixelsBRGThatChanged
        first = sortedPixelsBRGThatChanged[0]
        last = sortedPixelsBRGThatChanged[len(sortedPixelsBRGThatChanged) - 5]

        startInRegion = [first[0] - 30, first[1] - 30, first[2] - 30]
        endInRegion= [last[0] + 30, last[1] + 30, last[2] + 30]

        for y in range(0, height):
            for x in range(0, width):
                if (img[y, x].tolist() > startInRegion and img[y, x].tolist() < endInRegion) and img[y, x].tolist() != [255, 255, 255]:
                    convertedImage[y, x] = [255, 255, 255]

        img = convertedImage.copy()

    return convertedImage


def removeBackgroundBasedOnRegion(image):
    img = image.copy()
    colors = getArrayOfRGBColorsFromSideOfImages(img)
    backgroundClearedImage = cv2.inRange(img, totuple(colors['start']), totuple(colors['end']))
    noiseRemoved = removeSinglePixelsWithWhiteNeighbours(backgroundClearedImage, 1)
    return noiseRemoved

