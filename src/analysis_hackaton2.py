# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:45:38 2020

@author: z003vjxs
"""
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
from matplotlib import pyplot as plt
import math


def analysis(image):
    plt.imshow(image)

    # create region of interest depending on position: verify that images have always same dimension?
    #roi = image[670:1050, 1350:3750]
    height = image.shape[0]
    width = image.shape[1]
    roi = image[0:height, 0:width]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define lower and uppper limits of what we call "blue"
    brown_lo = np.array([2, 2, 30])
    brown_hi = np.array([140, 255, 255])

    # Mask image to only select blues
    mask = cv2.inRange(hsv, brown_lo, brown_hi)

    # count how many boxes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    minimum_area = 200
    average_cell_area = 250
    connected_cell_area = 4000
    cells = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minimum_area:
            cv2.drawContours(roi, [c], - 1, (2, 255, 2), 2)
            if area > connected_cell_area:
                cells += math.ceil(area / average_cell_area)
            else:
                cells += 1

    temprature = 40 + (4 * cells)

    print('Boxes: {}'.format(cells))
    print('Temperatur: {}'.format(temprature))
    cv2.imshow('close', close)
    cv2.imshow('original', roi)
    #cv2.waitKey(0)


def main():
    #img = cv2.imread('C:/Users/z003vjxs/Desktop/hackaton/hackathon2020/img/dummy.png')
    img = cv2.imread('../img/3.png')
    analysis(img)


if __name__ == "__main__":
    main()
