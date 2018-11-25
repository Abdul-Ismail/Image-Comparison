'''
Given an array of bgr values or any format with 3 channels, it will return the average
The average will be for each individual channel e.g bgr - all b values will be average together
'''
def averageOfRGB(BGR_values, calculationType):
    b = []
    g = []
    r = []

    #put b g r into separate arrays
    for bgr in BGR_values:
        b.append(bgr[0])
        g.append(bgr[1])
        r.append(bgr[2])

    if calculationType == 'avg':
        average = []
        average.append(sum(b) / len(b))
        average.append(sum(g) / len(g))
        average.append(sum(r) / len(r))
        return average

    elif calculationType == 'mean':
        mean = []
        middle = int(len(b)/2)
        mean.append(sorted(b)[middle] - 40)
        mean.append(sorted(g)[middle] - 40)
        mean.append(sorted(r)[middle] - 40)
        return mean


'''
@passedImage: image that we want to remove the flash from
@amountOftimestoRemove: The amount of times to attempt to remove the flash e.g 2 will remove it once and then try and remove it again from the removed image,
                        this has proved to remove twice the amount of flash (try play around with this number and you will see much more removed with more attempts)
@return: returns two images, one with the flash parts covered with the average, the other with the flash parts filled with the color red, this is to help with identifying what pixels were changed 
         The changes shown in the red image will only be the changes made on the final iteration
'''
def remove(passedImage, amountOftimestoRemove, calculationType):
    #working of copy as seems like passing img passes it by refernece so changes orignal outside of scope
    orignal = passedImage.copy()
    img = passedImage.copy()
    img1 = passedImage.copy()
    averagedImg = passedImage.copy()
    height = img.shape[0]
    width = img.shape[1]


    for i in range(amountOftimestoRemove):
        print('running', i)
        # loop through each pixel
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # if the pixel is white then it might be flash so check surrounding pixels
                if (img[y, x].tolist() > [200, 200, 200]):

                    # get bgr values for all of the surrouding pixels
                    RGB_values = [img[y - 1, x].tolist(), img[y + 1, x].tolist(), img[y, x - 1].tolist(), img[y, x + 1].tolist(),
                                  img[y + 1, x + 1].tolist(), img[y + 1, x - 1].tolist(), img[y - 1, x + 1].tolist(), img[y - 1, x - 1].tolist()]

                    average = averageOfRGB(RGB_values, calculationType)
                    img1[y, x] = [0, 0, 255]
                    averagedImg[y, x] = average

        img = averagedImg
        if (i != amountOftimestoRemove - 1): img1 = orignal


    return img1, averagedImg


def smoothImage(passedImage, amountOftimestoCalculate, calculationType):
    #working of copy as seems like passing img passes it by refernece so changes orignal outside of scope
    img = passedImage.copy()
    averagedImg = passedImage.copy()

    height = img.shape[0]
    width = img.shape[1]

    for i in range(amountOftimestoCalculate):
        print('running', i)
        # loop through each pixel
        for y in range(1, height - 2):
            for x in range(1, width - 2):

                # get bgr values for all of the surrouding pixels
                RGB_values = [img[y - 1, x].tolist(), img[y + 1, x].tolist(), img[y, x - 1].tolist(),
                              img[y, x + 1].tolist(),
                              img[y + 1, x + 1].tolist(), img[y + 1, x - 1].tolist(), img[y - 1, x + 1].tolist(),
                              img[y - 1, x - 1].tolist(),
                              img[y - 2, x - 2].tolist(), img[y - 2, x - 1].tolist(), img[y - 2, x].tolist(),
                              img[y - 2, x + 1].tolist(), img[y - 2, x + 2].tolist(),
                              img[y, x + 2].tolist(), img[y + 1, x + 2].tolist(), img[y + 2, x + 2].tolist(),
                              img[y - 1, x + 2].tolist(), img[y - 2, x + 2].tolist()]

                average = averageOfRGB(RGB_values, calculationType)
                averagedImg[y, x] = average

        img = averagedImg
    return averagedImg