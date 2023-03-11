# servo class which assigns channel and pwm values for each servo
class Servo:
    # recommended pwm values are the following: 1100: full reverse, 1500: stopped/default, 1900: full forward
    def __init__(self, master, servo_n, pwm_range=[1100,1500,1900]):
        self.master = master
        self.servo_n = servo_n
        self.pwm_range = pwm_range
        self.min, self.default, self.max = pwm_range
