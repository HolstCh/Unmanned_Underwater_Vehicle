import pymavlink
import Controller
import View

class Model():
    def __init__(self):
        self.value = 0
        self.mavlink = pymavlink.vehicle
        return

    def sendToVehicle(self, value, component):
        self.mavlink.send(value)
        return