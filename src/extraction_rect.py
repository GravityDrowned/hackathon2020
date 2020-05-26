import numpy as np
import cv2


def polyPD(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 127, 255, 1)

    contours, h = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        # print(len(approx))

        if len(approx) == 4:
            # rectangle order: start links unten, counter clockwise
            # print("square", approx)

            if cnt[0][0][0] - cnt[0][0][1] > 200:  # ToDo think about aproppriate value!
                print("checking x size:", cnt[0][0][0], cnt[0][0][1])
                cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)

                # for i in range(0, 3):
                # cv2.circle(img, (cnt[i][0][0], cnt[i][0][1]), 5, (255, 0, 2), -1)

    cv2.imshow('img', img)
    cv2.waitKey(0)


def get_corners_of_rect(img):
    height = img.shape[0]
    width = img.shape[1]

    # ToDo check if orientation is the right one
    x_min = width
    x_max = 0
    y_min = height
    y_max = 0

    # ToDo check if this runs correct (memory allocation, width or height rows in mem)
    for x in range(0, width):
        for y in range(0, height):
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
    cv2.waitKey(0)

    return y_min, y_max, x_min, x_max


def smash(img, src):
    # now smash a perspective transform on there
    # src = np.zeros((4, 2), dtype="float32")
    dst = np.array([[0.0, 0.0], [500.0, 0.0], [500.0, 500.0], [0.0, 500.0]], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    print(src)
    print(dst)
    print(M)
    warped = cv2.warpPerspective(img, M, (img.shape[0], img.shape[1]))
    cv2.imshow('image', warped)
    cv2.resizeWindow('image', 1000, 1000)
    cv2.waitKey(0)


def main():
    img_path = "../img/bigger.png"

    img = cv2.imread(img_path)
    img_src = cv2.imread(img_path)
    polyPD(img)

    y_min, y_max, x_min, x_max = get_corners_of_rect(img)

    crop_img = img_src[y_min:y_max, x_min:x_max]
    cv2.imshow('image', crop_img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
