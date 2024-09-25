import time
import serial


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
        self.set_angle(self.angle_x, self.angle_y)

    def set_angle(self, angle_x, angle_y):
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.ser.write(f"{int(angle_x)},{int(angle_y)};".encode())

    def __del__(self):
        self.ser.close()
