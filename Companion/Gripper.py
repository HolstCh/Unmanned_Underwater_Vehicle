class Gripper:
    # recommended pwm values are the following: closed state: 1100-1470, default (previous state): 1500 open state: 1530-1900
    def __init__(self, master, servo_n, pwm_range=[1200, 1500, 1800]):
        self.master = master
        self.servo_n = servo_n
        self.pwm_range = pwm_range
        self.min, self.default, self.max = pwm_range

    def open(self):
        return self.max
    
    def close(self):
        return self.min
