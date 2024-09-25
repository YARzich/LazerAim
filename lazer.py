import cv2
import numpy as np
from cv2 import cuda


def nothing(x):
    pass


class Lazer:

    def __init__(self):
        cv2.namedWindow('lazer')

        cv2.createTrackbar('HL', 'lazer', 36, 180, nothing)
        cv2.createTrackbar('SL', 'lazer', 29, 255, nothing)
        cv2.createTrackbar('VL', 'lazer', 199, 255, nothing)
        cv2.createTrackbar('H', 'lazer', 98, 180, nothing)
        cv2.createTrackbar('S', 'lazer', 255, 255, nothing)
        cv2.createTrackbar('V', 'lazer', 255, 255, nothing)

        kernel = np.ones((2, 2), np.uint8)

        self.morph_open = cuda.createMorphologyFilter(cv2.MORPH_OPEN, cv2.CV_8U, kernel)
        self.morph_close = cuda.createMorphologyFilter(cv2.MORPH_CLOSE, cv2.CV_8U, kernel)

    def lazer_detected(self, img):
        hl = cv2.getTrackbarPos('HL', 'lazer')
        sl = cv2.getTrackbarPos('SL', 'lazer')
        vl = cv2.getTrackbarPos('VL', 'lazer')

        hh = cv2.getTrackbarPos('H', 'lazer')
        hs = cv2.getTrackbarPos('S', 'lazer')
        hv = cv2.getTrackbarPos('V', 'lazer')

        gpu_img = cuda.GpuMat()
        gpu_img.upload(img)

        hsv = cuda.cvtColor(gpu_img, cv2.COLOR_BGR2HSV)

        lower_lazer = (hl, sl, vl)
        upper_lazer = (hh, hs, hv)

        mask_lazer = cuda.inRange(hsv, lower_lazer, upper_lazer)

        result_mask_lazer = self.morph_close.apply(self.morph_open.apply(mask_lazer))

        result_mask_lazer_cpu = result_mask_lazer.download()

        contours_lazer, _ = cv2.findContours(result_mask_lazer_cpu, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        x, y, w, h = 0, 0, 0, 0

        if contours_lazer:
            area = cv2.contourArea(contours_lazer[0])
            # if area > 1:
            x, y, w, h = cv2.boundingRect(contours_lazer[0])
            # cv2.drawContours(img, [contours_lazer[0]], -1, (0, 255, 0), 2)
            # cv2.putText(img, "KILL ", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # cv2.imshow('cam', img)
        cv2.imshow('lazer', result_mask_lazer.download())

        return x, y
