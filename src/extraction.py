"""
An OpenCV extraction tool to get good images to feed into the temp analysis tool

@author: Michael Wagner
"""

import cv2
import numpy as np
import imutils
import argparse


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)


def main():
    # img_path = "../img/dummy.png"
    img_path = "../img/tee.png"
    # read the img
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_color = cv2.imread(img_path, cv2.IMREAD_COLOR)

    cv2.imshow('image', img)
    cv2.waitKey(0)

    # exploit the qr code to get pos data
    qr = cv2.QRCodeDetector()
    img_qr = qr.detect(img)

    # draw little cirlces on the qr code
    if not img_qr[1] is None:
        for coord in img_qr[1]:
            # print("coord", coord[0])
            cv2.circle(img_color, (coord[0][0], coord[0][1]), 5, (0, 0, 255), -1)

    cv2.imshow('image', img_color)
    cv2.resizeWindow('image', 1000, 1000)
    cv2.waitKey(0)

    # now smash a perspective transform on there
    src = np.zeros((4, 2), dtype="float32")

    coords = []
    i = 0
    if not img_qr[1] is None:
        for coord in img_qr[1]:
            src[i] = coord[0]
            coords.append(coord[0])
            i += 1

    print("coords\n", coords)
    qr_size = coords[2][0] - coords[0][0]

    # works too, doesn't look as nice: # dst = np.array([[0.0, 0.0], [200.0, 0.0], [200.0, 200.0], [0.0, 200.0]], dtype="float32")
    dst = np.array([[coords[0][0], coords[0][1]], [coords[0][0]+qr_size, coords[0][1]],[coords[0][0]+qr_size, coords[0][1]+qr_size],[coords[0][0], coords[0][1]+qr_size]], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    print(src)
    print(dst)
    print(M)
    warped = cv2.warpPerspective(img_color, M, (img_color.shape[0], img_color.shape[1]))
    cv2.imshow('image', warped)
    cv2.resizeWindow('image', 1000, 1000)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
