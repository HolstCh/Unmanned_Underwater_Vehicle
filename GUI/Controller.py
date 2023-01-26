import View
import Model


class Controller():
    def __init__(self):
        self.thrust1Power = 0
        self.thrust2Power = 0
        self.thrust3Power = 0
        self.thrust1angle = 0
        self.thrust2angle = 0
        self.thrust3angle = 0
        self.maxThrust = 100
        self.minThrust = 0
        self.maxAngle = 90
        self.minAngle = -90
        self.model = Model()
        return

    def updateThrust(self, num, value):
        if value >= self.minThrust and value <= self.maxThrust:
            if num == 1:
                self.thrust1Power = value
            elif num == 2:
                self.thrust2Power = value
            elif num == 3:
                self.thrust3Power = value
            else:
                print("cannot set thruster")
        else:
            print("cannot set thruster")                
        return

    def updateAngle(self, num, value):
        if value >= self.minAngle and value <= self.maxAngle:
            if num == 1:
                self.thrust1Angle = value
            elif num == 2:
                self.thrust2Angle = value
            elif num == 3:
                self.thrust3Angle = value
            else:
                print("cannot set thruster")
        else:
            print("cannot set thruster")                
        return
    
    def sendToVehicle(self, component, value):      
        return