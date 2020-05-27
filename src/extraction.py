"""
An OpenCV extraction tool to get good images to feed into the temp analysis tool (extraction_full.py)
proof of concept of how you can transform images for further handling

generally speaking affine transformations aren't enough for photos (perfect solution)
you might want to look into b-splines
my recommendation/idea is to look into template matching and markers
I would recommend to put markers in the corners of the sticker so you can transform it

https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
https://docs.opencv.org/master/db/da9/tutorial_aruco_board_detection.html

@author: Michael Wagner
"""

import cv2
import numpy as np


def main(img_path):
    """
    opens a test image, gets the qr code corners and applies a perspective transformation
    :return:
    """
    # read the img
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_color = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # display the orig image
    cv2.imshow('image', img)
    cv2.waitKey(0)

    # exploit the qr code to get pos data
    qr = cv2.QRCodeDetector()
    img_qr = qr.detect(img)

    # draw little cirlces on the qr code
    if not img_qr[1] is None:
        for coord in img_qr[1]:
            cv2.circle(img_color, (coord[0][0], coord[0][1]), 5, (0, 0, 255), -1)

    # display the detected qr code corners in image
    cv2.imshow('image', img_color)
    cv2.waitKey(0)

    # now smash a perspective transform on there
    src = np.zeros((4, 2), dtype="float32")
    # extract the qr code corners
    coords = []
    i = 0
    if not img_qr[1] is None:
        for coord in img_qr[1]:
            src[i] = coord[0]
            coords.append(coord[0])
            i += 1

    # transform it close to the original location of the qr code
    qr_size = coords[2][0] - coords[0][0]
    dst = np.array([[coords[0][0], coords[0][1]], [coords[0][0] + qr_size, coords[0][1]],
                    [coords[0][0] + qr_size, coords[0][1] + qr_size], [coords[0][0], coords[0][1] + qr_size]],
                   dtype="float32")

    # transformation matrix M
    M = cv2.getPerspectiveTransform(src, dst)

    # apply the trans matrix M
    warped = cv2.warpPerspective(img_color, M, (img_color.shape[0], img_color.shape[1]))

    # display result
    cv2.imshow('image', warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Tip: Now you can cut the transformed image and put it in the next processing step (extraction_full.py)


if __name__ == "__main__":
    img_path = "../img/tee.png"
    main(img_path)
