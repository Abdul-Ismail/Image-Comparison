import cv2, math
import numpy as np
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

img1 = cv2.imread('./assets/AnimalFarm-original.jpg', cv2.IMREAD_COLOR)
img2 = cv2.imread('./assets/AnimalFarm-changed.jpg', cv2.IMREAD_COLOR)

#this will not work yet as we need to align the images
# img2 = cv2.imread('./assets/AnimalFarm-changed-smaller.jpg', cv2.IMREAD_COLOR)


'''
Get the cordinates of all pixels that are different
This will only working assuming there is the exact amount of pixels on both images, 
we will need to align the images together before getting this, this is just a quick test
'''
def getCordsOfPixelsThatHAveChanged(image1, image2):
    cords = []
    for y in range(0, image1.shape[0]):  #looping through each rows
         for x in range(0, image2.shape[1]): #looping through each column
             if image1[x, y].all() != image2[x, y].all():
                img2[x, y] = [255, 255, 255]
                cords.append([x, y])

    return cords


def printClusters(X, ms):
    # Plot result
    import matplotlib.pyplot as plt
    from itertools import cycle

    plt.figure(1)
    plt.clf()

    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    print(cluster_centers[0][0])
    n_clusters_ = len(labels_unique)

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()


'''
@cordinates: the cordinates of where the circles will be drawn (cordinates will be the centre of each cluste)
@image: the image that will have the circle drawn on
'''
def drawCircles(cordinates, image):
    for cord in cordinates:
        cv2.circle(image, (int(cord[0]), int(cord[1])), 30, (0, 0, 255), 2)

    return

'''
Will take the cordinates and cluster them together to figure out which changes are similar to each other
@cordinates: the cordinates of each pixel that are different 
@return: the center of each cluster point
'''
def clusterTheCordinates(cordinates):
    bandwidth = estimate_bandwidth(cordinates, quantile=0.05, n_samples=100)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(cordinates)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    labels_unique = np.unique(labels)

    # the number of cluster should be equal to the amount of changes in the picture, getting this accurate will be a challenge
    print("number of estimated clusters : %d" % len(cluster_centers))

    # printClusters(cordinates, ms)
    return cluster_centers


cordinatesOfPixelsThatHaveChanged = np.array(getCordsOfPixelsThatHAveChanged(img1, img2))
cluster_centers_cords = clusterTheCordinates(cordinatesOfPixelsThatHaveChanged)


drawCircles(cluster_centers_cords, img2)

cv2.imshow('image', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()


