import cv2
import numpy as np


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
    inRange_of_lower_and_ipper = cv2.inRange(roi, lower_region, upper_region)
    pixelCount = np.count_nonzero(inRange_of_lower_and_ipper == 255)
    # print(pixelCount)
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
            # pixel_count_map['white'] = get_region_color_count_for_specific_region(img, x, y,
            #                                                                                          region_width,
            #                                                                                          region_height,
            #                                                                                          (0, 0, 0),
            #                                                                                          (360, 2, 255))

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
def highlight_areas_for_given_cords(img1, img2, cords, region_width, region_height):
    img1_overlay = img1.copy()
    img2_overlay = img2.copy()


    for cord in cords:
        # img1[cord['y']:cord['y'] + region_height, cord['x']:cord['x'] + region_width] = 0
        # img2[cord['y']:cord['y'] + region_height, cord['x']:cord['x'] + region_width] = 0
        # cv2.rectangle(img1, (cord['x'] - region_width, cord['y'] - region_height), (cord['x'] - region_width, cord['y'] + region_height), (0, 0, 255), -1)

        cv2.rectangle(img=img1_overlay, pt1=(cord['x'], cord['y'] ), pt2=(cord['x'] + ( int(region_width)), cord['y'] + (int(region_height)) ), color=(0, 0, 255), thickness=-1)
        cv2.rectangle(img=img2_overlay, pt1=(cord['x'], cord['y'] ), pt2=(cord['x'] + ( int(region_width)), cord['y'] + (int(region_height)) ), color=(0, 0, 255), thickness=-1)


        # cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    opacity = 0.4
    cv2.addWeighted(img1_overlay, opacity, img1, 1 - opacity, 0, img1)
    cv2.addWeighted(img2_overlay, opacity, img2, 1 - opacity, 0, img2)


    return img1, img2


''' 
call all the sequences above
@img1: First image we want to compare
@img2: Second image we want to compare
@region_width: The height of the region
@region_height: The width of the region
@percetange_difference_allowed: The percentage of difference allowed for each color region between two regions
'''
def highligh_differences(img1, img2, region_width, region_height, percetange_difference_allowed, min_pixel_count):
    data = map_colors(img1, region_width, region_height)
    data2 = map_colors(img2, region_width, region_height)
    cords_with_most_changes = compare_regions(data, data2, percetange_difference_allowed, min_pixel_count)
    img1_highlited, img2_highlighted = highlight_areas_for_given_cords(img1, img2, cords_with_most_changes, region_width, region_height)

    return img1_highlited, img2_highlighted

