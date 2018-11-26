'''
***************** NOTE: RUN WITH PYTHON 3 *****************
Title: Finding difference between two images


Group members:
  - Thuy Nguyen
  - Ronalds Upenieks
  - Abdulaziz Ismail


Project Objective:
    The objective of this project is to take two images and highlight any differences that the image have.
    The solution should be able to spot the difference between two photographed images. The images
    can have the objects positioned at different areas in the image e.g object in image-a can be in the center
    and the object in image-b cna be at the top left corner.
    Images do not have to have the same lighting conditions e.g flash or shadow can be present in one or both of the images.

Challenges:
    - The solution has to be designed in a way that it could deal with objects from each images being location in different parts of the image
    - Flash present on images which does not equate to a difference in the image
    - Scale of the image
    - Lighting in the image


Step by step to our solution:
    1 - Extracting the ROI. We needed to crop out the image and only include the ROI. This helped deal with issues where the
        object in the image is located in different positions. ROI cropped by detecting pixel value differences in comparison to
        the background.
    2 - Removing the flash. This was done by detecting while pixels in comparison to their neighbors and then detected pixels
        are blended in with their neighbours. To blend the pixel in with their neighbours we get the average pixel value
        of all the neighbor pixels.
    3 - Map each region in the image to the occurrences of a range of HSV colors. HSV color range is used as it helps us
        deal with flash and lighting issues such as shadow because we can simply ignore those factors by having a threshold
        on the saturation and value. HSV allowed us to pick a color based on the HUE and then we were able to adjust
        the saturation value and the value/brightness value.
    4 - compare the mapped regions from both images and return coordinates of any regions that have a difference in mapped values.
        The way this comparison is done is that each region has an occurrence amount for a given pixel range, if any of these
        occurrences differ to the region from another image then we can consider it to be a difference. To deal with issues such that
        there might be small amount of pixel difference that does not necessarily equate to a difference we have a threshold on
        what the difference should be. We place a 95% threshold, if the difference between both values is greater than 95% then we
        can consider the regions to be different.
        Another issue that arises from this algorithm is that there tends to be some pixels in regions that are different, but these pixels
        don't equate to any differences and usually it is a small amount, e.g a region can have 1 or 2 pixel value that another region does not
        have, this is a 100% difference compared to the other region which does not have any occurrences of this pixex but its not a change. To deal
        with this issue we places a threshold/minimum amount of pixels that should be present before considering it to be a changed region.
    5 - Highlight the regions that have changed using the coordinates from the above step. To highlight each region we simply
        use the coordinate from above and use that coordinate to draw a rectangle thats filled. WE then add a weight to the images
        to allow for the transparency look, this is done by using the built in function of opencv addWeighted.
        Up to this point everything was done on the cropped image, step 5 is done on the original image as we want the highlighted
        parts to be done in the original image. Since the coordinate for the region we have is of the cropped image we need to
        map this value to the original image which is a bigger size. e.g a region change at coordinate (5, 10) will not be the
        same region in the original image as the cropped images could have been of the center of the original image. To deal with
        this we had the x and y points of where the original image was cropped from. We then use the cropped coordinates x and y and add
        coordinate of the region coordinate to map the region in the cropped coordinate to the region in the orignal image.
        e,g if image-a was cropped at x=50 and y=50 and the cropped image has a change located at x=10 and y=5 then the change
        in the original image would be at x=50+10 and y=50+5.
'''


import cv2
import numpy as np

image1 = cv2.imread('./assets/PCB 1.jpg')
image2 = cv2.imread('./assets/PCB 2.jpg')

region_width = 60
region_height = 60
percetange_difference_allowed = 95
min_pixel_count = 150

'''
Scale image to 860x720
@img: The image to scale
'''
def scaleImage(img):
    width = 860
    height = 720
    return cv2.resize(img, dsize=(width, height))


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
def removeFlash(passedImage, amountOftimestoRemove, calculationType):
    #working of copy as seems like passing img passes it by refernece so changes orignal outside of scope
    orignal = passedImage.copy()
    img = passedImage.copy()
    img1 = passedImage.copy()
    averagedImg = passedImage.copy()
    height = img.shape[0]
    width = img.shape[1]


    for i in range(amountOftimestoRemove):
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


#split image into YUV channel and return v channel
def splitYUV(img):
    YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(YUV)
    return v


#crop image based on darkest pixel compared to the background
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


#crop the roi
def crop_roi(img):
    img = img.copy()
    v = splitYUV(img.copy())
    bottom1, top1, left1, right1 = cropImage(v)
    image1_cropped = img[bottom1 - 50:top1 + 50, left1 - 50:right1 + 50]
    return image1_cropped, {'y': bottom1 - 50, 'x': left1 - 50}


'''
Will return the number of pixels for a region of color
@lower_region: Lower region of pixel
@upper_region: Upper region of pixel
@img: image being compared
@x: current x position of region
@y: current y position of region
@region_width: The height of the region
@region_height: The width of the region
@return: returns the count for the region
'''
def get_region_color_count_for_specific_region(img, x, y, region_width, region_height, lower_region, upper_region):
    roi = img[y:y + region_height, x:x + region_width]
    inRange_of_lower_and_upper = cv2.inRange(roi, lower_region, upper_region)
    pixelCount = np.count_nonzero(inRange_of_lower_and_upper == 255)
    return pixelCount


'''
for each region get number of values for each region color
'''
def map_colors(img, region_width, region_height):
    region_pixel_map = []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    height = img.shape[0]
    width = img.shape[1]

    #loop though the image by regions
    for y in range(region_height + 1, height - region_height, region_height):
        for x in range(region_width + 1, width - region_width, region_width):

            #map region to each pixel from range 0 - 180
            pixel_count_map = {}
            for i in range(0, 180, 2):
                pixel_count_map[str(i) + '-' + str(i+10)] = get_region_color_count_for_specific_region(img, x, y, region_width, region_height, (i, 30, 0), (i + 1, 255, 255))

            #add white regions
            # pixel_count_map['white'] = get_region_color_count_for_specific_region(img, x, y, region_width, region_height, (0, 0, 0), (360, 2, 255))

            region_pixel_map.append({
                'cords': {
                    'x': x,
                    'y': y
                },
                'map': pixel_count_map
            })

    return region_pixel_map


'''
get percentage change of 2 given values
@current: Current value thats being compared
@Previous: Previous value thats being compared
'''
def get_change(current, previous):
    diff = abs(current - previous)
    total = current + previous

    if total == 0: return 0

    return (100 / total) * diff


'''
Compare the given regions mapped to pixel color count
if there sa certain percentage change between the two images, we can assume it is different
'''
def compare_regions(region_data1, region_data2, percetange_difference_allowed, min_pixel_count):
    region_pixels_with_significant_changes = []

    for i in range(len(region_data1)):
        for key, value in region_data1[i]['map'].items():
            percentage_change_black = get_change(region_data1[i]['map'][key], region_data2[i]['map'][key])

            if (percentage_change_black > percetange_difference_allowed and (region_data1[i]['map'][key] > min_pixel_count or region_data2[i]['map'][key] > min_pixel_count)):
                region_pixels_with_significant_changes.append(region_data1[i]['cords'])

    return region_pixels_with_significant_changes



'''
highlight cords for given list of x and y and the region width and height
'''
def highlight_areas_for_given_cords(img1, img2, cords, region_width, region_height, image1_cropped_cords, image2_cropped_cords):
    img1_overlay = img1.copy()
    img2_overlay = img2.copy()

    for cord in cords:
        x1 = image1_cropped_cords['x'] + cord['x']
        y1 = image1_cropped_cords['y'] + cord['y']

        x2 = image2_cropped_cords['x'] + cord['x']
        y2 = image2_cropped_cords['y'] + cord['y']

        cv2.rectangle(img=img1_overlay, pt1=(x1, y1 ), pt2=(x1 + (int(region_width) ), y1 + (int(region_height)) ), color=(0, 0, 255), thickness=-1)
        cv2.rectangle(img=img2_overlay, pt1=(x2, y2 ), pt2=(x2 + (int(region_width) ), y2 + (int(region_height)) ), color=(0, 0, 255), thickness=-1)


    opacity = 0.4
    cv2.addWeighted(img1_overlay, opacity, img1, 1 - opacity, 0, img1)
    cv2.addWeighted(img2_overlay, opacity, img2, 1 - opacity, 0, img2)


    return img1, img2


#scale the image
image1 = scaleImage(image1)
image2 = scaleImage(image2)

#remove any flash from the image
red, image1 = removeFlash(image1, 1, 'avg')
red, image2 = removeFlash(image2, 1, 'avg')

#crop the image to the ROI (object we want to check for differences)
image1_roi, image1_cropped_cords = crop_roi(image1.copy())
image2_roi, image2_cropped_cords = crop_roi(image2.copy())

#for each region map the occurences for each HSV range
data = map_colors(image1_roi, region_width, region_height)
data2 = map_colors(image2_roi, region_width, region_height)

#get coordinates of regions that have changed
cords_with_most_changes = compare_regions(data, data2, percetange_difference_allowed, min_pixel_count)

#highlight the regions that have changed
img1_highlighted, img2_highlighted = highlight_areas_for_given_cords(image1, image2, cords_with_most_changes, region_width, region_height, image1_cropped_cords, image2_cropped_cords)

cv2.imshow('image1', img1_highlighted)
cv2.imshow('image2', img2_highlighted)


while True:
    if cv2.waitKey(33) == ord('q'):
        cv2.destroyAllWindows()
        exit()