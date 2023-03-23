import View
import Model
import socket
from time import sleep
from threading import Thread


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
        self.client_socket = None
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
    
    def sendToVehicle(self, command):
        self.client_socket.sendall(str.encode(command))
        data = self.client_socket.recv(1024)
        print(f"Received '{data!r}' from server! ")      
        return
    
    def start_gcs_connection(self):
        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        client_address = ('0.0.0.0', 5000)
        try:
            self.client_socket.connect(client_address)
        except:
            print("Could not connect to server, quitting")
        return
    
    def end_gcs_connection(self):
        try:
           self.client_socket.close()
        except:
            print("could not close socket properly")
        return
    
    def createCommand(self, comp, value):
        cmd = "*** " + str(comp) + " " + str(value) + " ***"
        return cmd