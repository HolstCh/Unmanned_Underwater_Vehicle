# Thruster class which assigns channel and motor speed values for each thruster

class Thruster:
    # recommended pwm values are the following: -3200: counterclockwise, 0: neutral position, 3200: clockwise
    def __init__(self, thruster_n, speed_range):
        self.thruster_n = thruster_n
        self.speed_range = speed_range
        self.min, self.default, self.max = speed_range