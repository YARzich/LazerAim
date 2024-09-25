import numpy as np


class PIDController:
    def __init__(self):
        self.Kp = 0.1
        self.Ki = 0.01
        self.Kd = 0.05
        self.previous_error_x = 0
        self.previous_error_y = 0
        self.integral_x = 0
        self.integral_y = 0
        self.pixels_per_degree = 100

    def update(self, error_x, error_y):
        proportional_x = self.Kp * error_x
        proportional_y = self.Kp * error_y

        self.integral_x += error_x
        self.integral_y += error_y
        integral_term_x = self.Ki * self.integral_x
        integral_term_y = self.Ki * self.integral_y

        derivative_x = error_x - self.previous_error_x
        derivative_y = error_y - self.previous_error_y
        derivative_term_x = self.Kd * derivative_x
        derivative_term_y = self.Kd * derivative_y

        correction_x = proportional_x + integral_term_x + derivative_term_x
        correction_y = proportional_y + integral_term_y + derivative_term_y

        correction_angle_x = correction_x / self.pixels_per_degree
        correction_angle_y = correction_y / self.pixels_per_degree

        correction_angle_x = np.clip(correction_angle_x, 55, 130)
        correction_angle_y = np.clip(correction_angle_y, 80, 130)
        #TODO: авто нахождение ограничительных углов

        return correction_angle_x, correction_angle_y

    def update_Kp(self, val):
        self.Kp = val / 100.0

    def update_Ki(self, val):
        self.Ki = val / 1000.0

    def update_Kd(self, val):
        self.Kd = val / 100.0

    def update_pixels_per_degree(self, val):
        self.pixels_per_degree = val
