import cv2
import numpy as np


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

        self.kernel = np.ones((2, 2), np.uint8)

    def lazer_detected(self, img):
        hl = cv2.getTrackbarPos('HL', 'lazer')
        sl = cv2.getTrackbarPos('SL', 'lazer')
        vl = cv2.getTrackbarPos('VL', 'lazer')

        hh = cv2.getTrackbarPos('H', 'lazer')
        hs = cv2.getTrackbarPos('S', 'lazer')
        hv = cv2.getTrackbarPos('V', 'lazer')

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_lazer = (hl, sl, vl)
        upper_lazer = (hh, hs, hv)

        mask_lazer = cv2.inRange(hsv, lower_lazer, upper_lazer)

        result_mask_lazer = cv2.morphologyEx(cv2.morphologyEx(mask_lazer, cv2.MORPH_OPEN, self.kernel),
                                             cv2.MORPH_CLOSE, self.kernel)

        # result_mask_lazer_cpu = result_mask_lazer.download()qw

        contours_lazer, _ = cv2.findContours(result_mask_lazer, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        x, y, w, h = 0, 0, 0, 0

        if contours_lazer:
            area = cv2.contourArea(contours_lazer[0])
            # if area > 1:
            x, y, w, h = cv2.boundingRect(contours_lazer[0])
            # cv2.drawContours(img, [contours_lazer[0]], -1, (0, 255, 0), 2)
            # cv2.putText(img, "KILL ", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow('lazer', result_mask_lazer)

        return x, y
