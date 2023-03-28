# Servo class which assigns channel and pwm values for each servo

class Servo:
    # recommended pwm values are the following: 900: full rotation counterclockwise, 1500: neutral position/default, 2100: full rotation clockwise
    def __init__(self, servo_n, pwm_range):
        self.servo_n = servo_n
        self.pwm_range = pwm_range
        self.min, self.default, self.max = pwm_range
