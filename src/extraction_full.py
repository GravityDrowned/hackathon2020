"""
An OpenCV extraction tool to get good images to feed into the temp analysis tool

proof of concept that needs a lot of love in order to be truly amazing

@author: Michael Wagner
"""
import cv2
import numpy as np
import os
from analysis_hackaton2 import *


def get_qr_code_coords(img):
    """
    finds a qr code inside of an image
    :param img: an image with a visible temp sticker
    :return: the lower left corner of the qr code, the skewed width & height
    """

    # exploit the qr code to get pos data
    qr = cv2.QRCodeDetector()
    img_qr = qr.detect(img)

    # list for return vals
    coords = []

    # draw little circles on the qr code
    if not img_qr[1] is None:
        for coord in img_qr[1]:
            cv2.circle(img, (coord[0][0], coord[0][1]), 5, (0, 255, 0), -1)
            coords.append((coord[0][0], coord[0][1]))

    # decrease the img size, in order to display it on 1920x1080
    frame_small = cv2.resize(img, (960, 540))
    cv2.imshow('get qr code coordinates', frame_small)

    # extract the qr code position and skewed height & width
    qr_lower_left_point = coords[0]
    qr_height = coords[2][0] - coords[0][0]
    qr_width = coords[2][1] - coords[0][1]

    return qr_lower_left_point, qr_height, qr_width


def polyPD(img, min_size):
    """
    marks the temp sensor area in red (0,255,255)
    :param img: the image one which you want to detect the thermometer sticker area
    :param min_size: the detected size of the qr-code
    :return: the in-image with the marked red area
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 1)
    contours, h = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if len(approx) == 4:
            # rectangle order: start links unten, counter clockwise
            # ToDo think about aproppriate value! things that are too small should not be detected
            # ToDo if rectangles are on the machine this will break
            if cnt[0][0][0] - cnt[0][0][1] > min_size:
                cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)

    frame_small = cv2.resize(img, (960, 540))
    cv2.imshow('polyPD()', frame_small)


def get_corners_of_rect(img, qr_lower_left_point, qr_height, qr_width):
    """
    detects the corners of the big rectangle,
    considers the position of the qr code in order to not search the entire image
    :param img: an img that was processed by polyPD
    :param qr_lower_left_point: yeah, the lower left point of the qr code
    :param qr_height: detected height of the qr code
    :param qr_width: detected width of the qr code
    :return: the 4 corners of the thermometer rectangle
    """
    height = img.shape[0]
    width = img.shape[1]

    x_min = width
    x_max = 0
    y_min = height
    y_max = 0

    # brute force pixel detection, not smart, exchange with an in-built opencv function - time pressure keeps me from it
    for x in range(0, width):
        for y in range(int(qr_lower_left_point[1]), int(qr_lower_left_point[1] + qr_height)):
            if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 255:
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
    # draw circles on the detected corners
    cv2.circle(img, (x_min, y_min), 5, (255, 0, 2), -1)
    cv2.circle(img, (x_min, y_max), 5, (255, 0, 2), -1)
    cv2.circle(img, (x_max, y_min), 5, (255, 0, 2), -1)
    cv2.circle(img, (x_max, y_max), 5, (255, 0, 2), -1)

    #resize and show result
    frame_small = cv2.resize(img, (960, 540))
    cv2.imshow('get_corners_of_rect', frame_small)  # too big

    return y_min, y_max, x_min, x_max


def extract(img, img_src):
    """
    extracts the intersting area (the sticker) out of an image
    :param img: an input img to work with (aka drawing in it)
    :param img_src: an image to keep the original (aka no painting on this)
    :return: the extracted image and a boolean if it was succesful
    """
    succesful = False
    crop_img = None
    # get the qr coordinates
    try:
        qr_lower_left_point, qr_height, qr_width = get_qr_code_coords(img)
        succesful = True
    except:
        print("extract of points failed in extract(img, img_src)")

    if succesful:
        min_size = qr_width
        polyPD(img, min_size)
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        y_min, y_max, x_min, x_max = get_corners_of_rect(blur, qr_lower_left_point, qr_height, qr_width)

        #print(x_min, y_min, img_src.shape)
        if x_min != img_src.shape[1]:

            crop_img = img_src[y_min:y_max, x_min:x_max]
            # cv2.imshow('image extract', crop_img)
            succesful = True
        else:
            succesful = False

    return crop_img, succesful


def ez_analysis(img):
    # ToDo detect bad images (aka not showing only the temp sensor area)
    # ToDo maybe consider past values? in need of a solution to make it more robust
    """
    since the result is ideally in the same format every time, I hard-coded the evaluation of thermometer slots
    instead of this you can also evaluate with analysis_hackathon2.py by Anja Amthor (needs fine-tuning)

    :param img: an extracted image, containing only the temperature sensor area (10 fields)
    :return: the number of "hot" fields
    """
    clean_img = img.copy()

    for x in range(35, img.shape[1], 48):
        # draw circles on the evaluation areas
        cv2.circle(img, (x, int(img.shape[0] / 2)), 5, (0, 0, 255), -1)
        cv2.imshow("ez_analysis()", img)
        x += 50

    # datapoints = []# collect colour values
    hot_marker = 0  # collect the number of "hot" fields
    for x in range(35, img.shape[1], 49):
        temp = clean_img[int(img.shape[0] / 2), x]
        # datapoints.append(temp)
        # ToDo: this is no permanent solution, normalise your image to deal with different brightness
        # ToDo: This whole function needs a way to deal with wrong images
        if temp[2] > 50:
            hot_marker += 1

    # print("hotmarkers", hot_marker, "datapoints", datapoints)
    return hot_marker


def main():
    """
    main function that walks a dir as input
    :return: -
    """
    for root, dirs, files in os.walk("../img/all", topdown=False):
        for f in files:
            print(os.path.join(root, f))
            try:
                img_path = os.path.join(root, f)
                img = cv2.imread(img_path)
                img_src = cv2.imread(img_path)  # , cv2.IMREAD_COLOR)
                crop_img, succesful = extract(img, img_src)
                if succesful:
                    resize_img = cv2.resize(crop_img, (500, 90))
                    # cv2.imwrite(os.path.join("./7.png"), resize_img); #
                    analysis(resize_img)
                    # cv2.waitKey(0)
                else:
                    print("extraction failed in main()")
            except:
                print("failed")

    cv2.destroyAllWindows()


def main_video_feed():
    """
    use a video to feed the pipeline
    skips frames atm (faster execution)
    :return: -
    """
    #cap = cv2.VideoCapture('../img/vid/1.Mov') #1,2,3,4
    print("If you get an CAP_IMAGES ERROR: You might want to change the .mov file (line 216) "
          "or download the demo hot.mov (contact michael.wagner.bamberg@gmail.com) \n"
          "or download IMG_2489.mov from https://www.fagservice.de/apps/files/?dir=/Temperatur%20Sticker%20Videoaufnahme&fileid=2359368"
          "see README for who to contact for login credentials")

    cap = cv2.VideoCapture('../img/vid/hot.mov')

    number_frames_to_skip = 600
    frameskip = 0
    temperature = 40

    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frameskip += 1
        if (frameskip > number_frames_to_skip):
            frameskip = 0
            img = frame.copy()  # cv2.resize(frame, (int(frame.shape[0]/4), int(frame.shape[1]/4)))
            img_src = img.copy()
            try:
                crop_img, successful = extract(img, img_src)
                if successful:
                    #resize to an arbitrary size (so it's always the same)
                    resize_img = cv2.resize(crop_img, (500, 90))
                    hot_marker = ez_analysis(resize_img)

                    #ToDo: sticker specific values, be careful when different stickers are used, ours are 40°C-80°C
                    print("TEMP:", hot_marker * 4 + 40)
                    temperature = hot_marker * 4 + 40

                else:
                    print("extraction failed in main_video_feed()")
            except IndexError as i_e:
                print("Index error: {0}".format(i_e))
            except:
                print("An error occurred")

        frame_small = cv2.resize(frame, (960, 540))
        frame_small_text = cv2.putText(frame_small, str(temperature) + 'C', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 10,
                                       (100, 150, 0), 20, cv2.LINE_AA)
        cv2.imshow('main video feed', frame_small_text)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()



if __name__ == "__main__":
    # main()
    main_video_feed()
