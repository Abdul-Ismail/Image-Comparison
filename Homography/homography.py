import cv2
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui
from skimage.measure import compare_ssim
import argparse
import imutils

# Define amount of features ORB will be locating
FEATURES = 100

#
MATCH_PERCENT = 0.15



def alignObjects(img1, img2):

    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Find ORB Locators and produce Descriptors
    orb = cv2.ORB_create(FEATURES)
    locators1, descriptors1 = orb.detectAndCompute(grayA, None)
    locators2, descriptors2 = orb.detectAndCompute(grayB, None)

    # Match the descriptors of each image against one another
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort Matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove matches that don't meet the MATCH_PERCENT threshold
    amtGoodMatches = int(len(matches) * MATCH_PERCENT)
    matches = matches[:amtGoodMatches]

    # Draw matches
    ImgMatches = cv2.drawMatches(img1, locators1, img2, locators2, matches, None)
    cv2.imwrite("matches.jpg", ImgMatches)

    # Extract coordinates of good matches
    locatorPoints1 = np.zeros((len(matches), 2), dtype=np.float32)
    locatorPoints2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        locatorPoints1[i, :] = locators1[match.queryIdx].pt
        locatorPoints2[i, :] = locators1[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(locatorPoints1, locatorPoints2, cv2.RANSAC)

    # Use homography
    height, width, channels = img2.shape
    img1Reg = cv2.warpPerspective(img1, h, (width, height))

    return img1Reg, h




refFilename = "PCB 1.JPG"
imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)


imFilename = "PCB 2.JPG"
im = cv2.imread(imFilename, cv2.IMREAD_COLOR)


imReg, h = alignObjects(im, imReference)


# Write result to disk
outFilename = "aligned.jpg"
print("Saving aligned image : ", outFilename);
cv2.imwrite(outFilename, imReg)

# Homography
print("Estimated homography : \n", h)

