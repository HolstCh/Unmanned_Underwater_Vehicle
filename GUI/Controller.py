import View
import socket
from time import sleep
from threading import Thread


class Controller:
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
        self.client_socket = None
        self.UDP_socket = None
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

    def sendToModel(self, command):
        self.client_socket.sendall(str.encode(command))
        data = self.client_socket.recv(1024)
        print(f"Received '{data!r}' from server! ")
        return
    
    def parse_IMU_data(self, raw_imu):
        data = raw_imu.split(" ")


    def end_gcs_connection(self):
        try:
            self.client_socket.close()
        except:
            print("could not close socket properly")
        return

    def start_gcs_connection(self):
        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        client_address = (socket.gethostbyname("raspberrypi.local"), 5000)
        try:
            self.client_socket.connect(client_address)
        except:
            print("Could not connect to server, quitting")

    def get_IMU_loop(self):
        while True:
            IMU_data = self.UDP_socket.recvfrom(1024)
            IMU_msg = "{}".format(IMU_data)
            #self.parse_IMU_data(IMU_msg)
            print(IMU_msg)
            #self.UDP_socket.sendto(str.encode("Received Data"))
    
    def start_IMU_connection(self):
        #Create a UDP Server socket
        self.UDP_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        server_address = ("172.28.96.1", 6000)
        self.UDP_socket.bind(server_address)
        print("UDP Server started")
        try:
            self.thread = Thread(target=self.get_IMU_loop, daemon=True)
            self.thread.start()
        except:
            print("Could not start IMU loop")


    def createCommand(self, comp, value):
        cmd = "*** *** " + str(comp) + " " + str(value) + " ***"
        return cmd

    def create_commands(self, comp1, value1, comp2, value2, comp3, value3, comp4, value4, comp5, value5):
        cmd = "*** *** " + str(comp1) + " " + str(value1) + " " + str(comp2) + " " + str(value2) + " " + str(comp3) \
              + " " + str(value3) + " " + str(comp4) + " " + str(value4) + " " + str(comp5) + " " + str(value5) + " ***"
        return cmd
