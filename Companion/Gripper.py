class Gripper:
    # recommended pwm values are the following: 1100: closed state, 1100: closed/default, 1500: open state
    def __init__(self, master, servo_n, pwm_range=[1100,1100,1500]):
        self.master = master
        self.servo_n = servo_n
        self.pwm_range = pwm_range
        self.min, self.default, self.max = pwm_range

    def open(self):
        return self.max
    
    def close(self):
        return self.min