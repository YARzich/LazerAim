import cv2


class MouseDetect:
    def __init__(self):
        self.mouseX = -1
        self.mouseY = -1
        self.left_button_pressed = False
        cv2.setMouseCallback("Camera", self.mouse_position)

    def mouse_position(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.left_button_pressed = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.left_button_pressed = False
        elif self.left_button_pressed:
            self.mouseX = x
            self.mouseY = y
