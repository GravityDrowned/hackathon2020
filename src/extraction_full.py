"""
An OpenCV extraction tool to get good images to feed into the temp analysis tool

It needs a lot of love in order to be amazing

@author: Michael Wagner
"""
# ToDo: debug your entire row/colum logic, 5€ theres an error in there
import cv2
import numpy as np
import os
# import analysis_hackaton2
from analysis_hackaton2 import *


def get_qr_code_coords(img):
    # exploit the qr code to get pos data
    qr = cv2.QRCodeDetector()
    img_qr = qr.detect(img)

    # list for return vals
    coords = []

    # draw little circles on the qr code
    if not img_qr[1] is None:
        for coord in img_qr[1]:
            # print("coord", coord[0])
            cv2.circle(img, (coord[0][0], coord[0][1]), 5, (0, 255, 0), -1)
            coords.append((coord[0][0], coord[0][1]))

    cv2.imshow('image', img)
    # cv2.resizeWindow('image', 1000, 1000)
    # cv2.waitKey(0)

    print(coords)

    qr_lower_left_point = coords[0]
    qr_height = coords[2][0] - coords[0][0]
    qr_width = \
        coords[2][1] - coords[0][1]

    return qr_lower_left_point, qr_height, qr_width


def polyPD(img, min_size):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 127, 255, 1)

    contours, h = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        # print(len(approx))

        if len(approx) == 4:
            # rectangle order: start links unten, counter clockwise
            # print("square", approx)

            if cnt[0][0][0] - cnt[0][0][1] > min_size:  # ToDo think about aproppriate value!
                # print("checking x size:", cnt[0][0][0], cnt[0][0][1])
                cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)

                # for i in range(0, 3):
                # cv2.circle(img, (cnt[i][0][0], cnt[i][0][1]), 5, (255, 0, 2), -1)

    cv2.imshow('img', img)
    # cv2.waitKey(0)


def get_corners_of_rect(img, qr_lower_left_point, qr_height, qr_width):
    height = img.shape[0]
    width = img.shape[1]

    # ToDo check if orientation is the right one
    x_min = width
    x_max = 0
    y_min = height
    y_max = 0

    # ToDo check if this runs correct (memory allocation, width or height rows in mem)
    for x in range(0, width):
        # for x in range(int(qr_lower_left_point[0]), int(qr_lower_left_point[0]+qr_width)):
        # for y in range(0, height):
        for y in range(int(qr_lower_left_point[1]), int(qr_lower_left_point[1] + qr_height)):
            if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 255:
                # print(img[y][x])
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

    cv2.circle(img, (x_min, y_min), 5, (255, 0, 2), -1)
    cv2.circle(img, (x_min, y_max), 5, (255, 0, 2), -1)
    cv2.circle(img, (x_max, y_min), 5, (255, 0, 2), -1)
    cv2.circle(img, (x_max, y_max), 5, (255, 0, 2), -1)

    cv2.imshow('img', img)
    # cv2.waitKey(0)

    return y_min, y_max, x_min, x_max


def extract(img_path):
    # read the img
    img = cv2.imread(img_path)
    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_src = cv2.imread(img_path)  # , cv2.IMREAD_COLOR)

    # get the qr coordinates
    qr_lower_left_point, qr_height, qr_width = get_qr_code_coords(img)

    # img = cv2.imread(img_path)
    # img_src = cv2.imread(img_path)
    min_size = qr_width
    polyPD(img, min_size)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    y_min, y_max, x_min, x_max = get_corners_of_rect(blur, qr_lower_left_point, qr_height, qr_width)

    crop_img = img_src[y_min:y_max, x_min:x_max]
    cv2.imshow('image', crop_img)

    # cv2.imwrite(os.path.join("./3.png"), crop_img);

    return crop_img


def main():
    for root, dirs, files in os.walk("../img/all", topdown=False):
        for f in files:
            print(os.path.join(root, f))
            try:
                crop_img = extract(os.path.join(root, f))
                resize_img = cv2.resize(crop_img, (500, 90))
                analysis(resize_img)
                cv2.waitKey(0)
            except:
                print("failed")
    # extract("../img/tee.png")
    # extract("../img/dummy.png")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
