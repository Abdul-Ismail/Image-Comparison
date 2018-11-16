import cv2
import numpy as np

'''
for each region get number of values for each region color
'''
def map_colors(img, region_width, region_height):
    region_pixel_map = []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    height = img.shape[0]
    width = img.shape[1]

    #loop though the image by regions
    for y in range(1, height - region_height, region_height):
        for x in range(1, width - region_width, region_width):
            roi = img[y:y + region_height, x:x + region_width]
            black_region = cv2.inRange(roi, (0, 0, 0), (360, 100, 40))
            black_count = np.count_nonzero(black_region == 255)


            region_pixel_map.append({
                'cords': {
                    'x': x,
                    'y': y
                },
                'map': {
                    'black': black_count

                }
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
def compare_regions(region_data1, region_data2, percetange_difference_allowed):
    region_pixels_with_significant_changes = []

    for i in range(len(region_data1)):
        percentage_change_black = get_change(region_data1[i]['map']['black'], region_data2[i]['map']['black'] )
        # print(percentage_change_black)

        if (percentage_change_black > percetange_difference_allowed):
            region_pixels_with_significant_changes.append(region_data1[i]['cords'])

    return region_pixels_with_significant_changes


'''
highlight cords for given list of x and y and the region width and height
'''
def highlight_areas_for_given_cords(img1, img2, cords, region_width, region_height):
    for cord in cords:
        img1[cord['y']:cord['y'] + region_height, cord['x']:cord['x'] + region_width] = 0
        img2[cord['y']:cord['y'] + region_height, cord['x']:cord['x'] + region_width] = 0

    return img1, img2


'''
call all the sequences above
@img1: First image we want to compare
@img2: Second image we want to compare
@region_width: The height of the region
@region_height: The width of the region
@percetange_difference_allowed: The percentage of difference allowed for each color region between two regions
'''
def highligh_differences(img1, img2, region_width, region_height, percetange_difference_allowed):
    data = map_colors(img1, region_width, region_height)
    data2 = map_colors(img2, region_width, region_height)
    cords_with_most_changes = compare_regions(data, data2, percetange_difference_allowed)
    img1_highlited, img2_highlighted = highlight_areas_for_given_cords(img1, img2, cords_with_most_changes, region_width, region_height)

    return img1_highlited, img2_highlighted
