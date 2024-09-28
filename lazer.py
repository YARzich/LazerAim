import cv2
import numpy as np


def nothing(x):
    pass


class Lazer:

    def __init__(self):
        cv2.namedWindow('lazer_Lab')
        cv2.createTrackbar('L_min', 'lazer_Lab', 218, 255, nothing)
        cv2.createTrackbar('A_min', 'lazer_Lab', 70, 255, nothing)
        cv2.createTrackbar('B_min', 'lazer_Lab', 100, 255, nothing)
        cv2.createTrackbar('L_max', 'lazer_Lab', 255, 255, nothing)
        cv2.createTrackbar('A_max', 'lazer_Lab', 120, 255, nothing)
        cv2.createTrackbar('B_max', 'lazer_Lab', 138, 255, nothing)

        self.kernel = np.ones((2, 2), np.uint8)

    def lazer_detected(self, img):

        # result_mask_lazer = self.create_mask_HSV(img)
        result_mask_lazer = self.create_mask_Lab(img)

        contours_lazer = self.contours(result_mask_lazer)

        x, y, w, h = 0, 0, 0, 0

        if contours_lazer:
            x, y, w, h = cv2.boundingRect(contours_lazer[0])

        return x, y

    def contours(self, mask_lazer):
        contours_lazer, _ = cv2.findContours(mask_lazer, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours_lazer

    def create_mask_Lab(self, img):
        l_min = cv2.getTrackbarPos('L_min', 'lazer_Lab')
        a_min = cv2.getTrackbarPos('A_min', 'lazer_Lab')
        b_min = cv2.getTrackbarPos('B_min', 'lazer_Lab')

        l_max = cv2.getTrackbarPos('L_max', 'lazer_Lab')
        a_max = cv2.getTrackbarPos('A_max', 'lazer_Lab')
        b_max = cv2.getTrackbarPos('B_max', 'lazer_Lab')

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)

        lower_lazer = (l_min, a_min, b_min)
        upper_lazer = (l_max, a_max, b_max)

        mask_lazer = cv2.inRange(lab, lower_lazer, upper_lazer)

        result_mask_lazer = cv2.morphologyEx(cv2.morphologyEx(mask_lazer, cv2.MORPH_OPEN, self.kernel),
                                             cv2.MORPH_CLOSE, self.kernel)

        cv2.imshow('lazer_Lab', result_mask_lazer)

        return result_mask_lazer
