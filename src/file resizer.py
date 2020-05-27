import cv2
import numpy as np
import os


# resizes a file by "resize_factor"
def size_down(img_path, resize_factor):
    img = cv2.imread(img_path)
    height = img.shape[0]
    width = img.shape[1]


    print("resize to", int(width / resize_factor), int(height / resize_factor))
    img2 = cv2.resize(img, (int(width / resize_factor), int(height / resize_factor)))
    return img2

#iterates over dir and calls resize on all files (original files are lost)
def main():
    for root, dirs, files in os.walk("../img/all", topdown=False):
        for f in files:
            print(os.path.join(root, f))
            # try:
            img = size_down(os.path.join(root, f), 5)
            cv2.imwrite(os.path.join(root, f), img)


if __name__ == "__main__":
    main()
