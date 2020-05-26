import cv2
import numpy as np
import os

def size_down(img_path):
    img = cv2.imread(img_path)
    height = img.shape[0]
    width = img.shape[1]

    resize_factor = 5

    print("resize to",  int(width/resize_factor), int(height/resize_factor))
    img2 = cv2.resize(img, (int(width/resize_factor), int(height/resize_factor)))
    return img2


def main():
    for root, dirs, files in os.walk("../img/all", topdown=False):
        for f in files:
            print(os.path.join(root, f))
            #try:
            img = size_down(os.path.join(root, f))
            cv2.imwrite(os.path.join(root, f), img);

            #except:
                #print("failed")
    #extract("../img/tee.png")
    #extract("../img/dummy.png")


if __name__ == "__main__":
    main()
