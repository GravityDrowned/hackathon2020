import numpy as np
import cv2

img_path = "../img/dummy.png"
import numpy as np
import cv2 as cv

im = cv.imread(img_path)
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

cv2.imshow('image', imgray)
cv2.waitKey(0)

ret, thresh = cv.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
