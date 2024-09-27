import time

import cv2
import numpy as np

import lazer
import pid_controller
import mouse_detect
import arduino_connection


cv2.namedWindow("Camera")
cv2.resizeWindow("Camera", 1280, 720)

arduino = arduino_connection.Arduino()
pid = pid_controller.PIDController()
mouse = mouse_detect.MouseDetect()
lazer = lazer.Lazer()

cap = cv2.VideoCapture(0)

cv2.namedWindow("PID Controls")
cv2.createTrackbar("Kp", "PID Controls", int(pid.Kp * 100), 100, pid.update_Kp)
cv2.createTrackbar("Ki", "PID Controls", int(pid.Ki * 1000), 1000, pid.update_Ki)
cv2.createTrackbar("Kd", "PID Controls", int(pid.Kd * 100), 100, pid.update_Kd)
cv2.createTrackbar("Pixels/Degree", "PID Controls", pid.pixels_per_degree, 1000, pid.update_pixels_per_degree)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    currentX, currentY = lazer.lazer_detected(frame)

    if mouse.mouseX >= 0 and mouse.mouseY >= 0:
        error_x = mouse.mouseX - currentX
        error_y = mouse.mouseY - currentY

        correction_angle_x, correction_angle_y = pid.update(error_x, error_y)

        if mouse.left_button_pressed:
            arduino.set_correction_angle(int(correction_angle_x), int(correction_angle_y))
            print("mouseX: " + str(mouse.mouseX) + "\n" + "mouseY: " + str(mouse.mouseY))
            print("currentX: " + str(currentX) + "\n" + "currentY: " + str(currentY))
            print("error_x: " + str(error_x) + "\n" + "error_y: " + str(error_y))
            print("correction_angle_x: " + str(correction_angle_x) + "\n" + "correction_angle_y: " + str(correction_angle_y))

        previous_error_x = error_x
        previous_error_y = error_y

        time.sleep(0.001)

    cv2.circle(frame, (int(currentX), int(currentY)), 5, (0, 0, 255), -1)

    cv2.imshow("Camera", frame)

    controls_frame = np.zeros((100, 400, 3), dtype=np.uint8)

    cv2.putText(controls_frame, f'Kp: {pid.Kp:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(controls_frame, f'Ki: {pid.Ki:.4f}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(controls_frame, f'Kd: {pid.Kd:.2f}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(controls_frame, f'Pixels/Degree: {pid.pixels_per_degree}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 255), 2)

    cv2.imshow("PID Controls", controls_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        arduino.set_start_angle()
cap.release()
cv2.destroyAllWindows()
