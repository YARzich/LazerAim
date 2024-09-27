import time
import serial
import numpy as np


class Arduino:
    def __init__(self):
        while True:
            try:
                self.ser = serial.Serial('COM3', 115200)
                break
            except serial.SerialException:
                print("Турелька не подключена.")
                time.sleep(1)
        self.angle_x = 90
        self.angle_y = 90
        self.set_start_angle()

    def set_correction_angle(self, correction_angle_x, correction_angle_y):
        self.angle_x += correction_angle_x
        self.angle_y += correction_angle_y

        # TODO: авто нахождение ограничительных углов
        self.angle_x = np.clip(self.angle_x, 65, 105)
        self.angle_y = np.clip(self.angle_y, 65, 120)

        self.set_angle(self.angle_x, self.angle_y)

    def set_angle(self, angle_x, angle_y):
        print("angle_x: " + str(angle_x) + "\n" + " angle_y: " + str(angle_y))
        self.ser.write(f"{int(angle_x)},{int(angle_y)};".encode())

    def set_start_angle(self):
        self.set_angle(90, 90)

    def __del__(self):
        self.ser.close()
