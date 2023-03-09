#import pymavlink
import Controller
import View
from Autopilot import Autopilot

class Model():
    def __init__(self):
        self.value = 0
        self.mavlink = Autopilot(self)
        return

    def sendToVehicle(self, value, component):
        self.mavlink.attemptPrint(value)
        return