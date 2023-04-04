import View
import socket
from time import sleep
from threading import Thread
import threading
from _thread import *

class Controller:
    def __init__(self):
        self.servo_left_param = "angle1"
        self.servo_right_param = "angle2"
        self.servo_tail_param = "angle3"
        self.thruster_left_param = "thruster1"
        self.thruster_right_param = "thruster2"
        self.thruster_tail_param = "thruster3"
        self.gripper_left_param = "gripper1"
        self.gripper_right_param = "gripper2"
        self.servo_left_value = 0.5
        self.servo_right_value = 0.5
        self.servo_tail_value = 0.5
        self.thruster_left_value = 0.5
        self.thruster_right_value = 0.5
        self.thruster_tail_value = 0.5
        self.gripper_left_value = 0.5
        self.gripper_right_value = 0.5
        self.client_socket = None
        self.x_accel = 0
        self.y_accel = 0
        self.z_accel = 0
        self.x_gyro = 0
        self.y_gyro = 0
        self.z_gyro = 0
        self.print_lock = threading.Lock()
        return

    def set_servo_left(self, value):
        self.servo_left_value = value

    def set_servo_right(self, value):
        self.servo_right_value = value

    def set_servo_tail(self, value):
        self.servo_tail_value = value

    def set_gripper_left(self, value):
        self.gripper_left_value = value

    def set_gripper_right(self, value):
        self.gripper_right_value = value

    def getXaccel(self):
        return self.x_accel

    def getYaccel(self):
        return self.y_accel

    def getZaccel(self):
        return self.z_accel

    def getXgyro(self):
        return self.x_gyro

    def getYgyro(self):
        return self.y_gyro

    def getZgyro(self):
        return self.z_gyro

    def convToMMS2(self, val):
        value = int(val)
        return value * (9.81 / 1000)

    def convToRads(self, val):
        value = int(val)
        return value / 1000

    def parse_IMU_data(self, raw_imu):
        data = raw_imu.split(", ")
        # Retrieve accel values only
        try:
            xaccel_raw = data[2].split(": ")
            xaccel = xaccel_raw[1]
            yaccel_raw = data[3].split(": ")
            yaccel = yaccel_raw[1]
            zaccel_raw = data[4].split(": ")
            zaccel = zaccel_raw[1]
            xgyro_raw = data[5].split(": ")
            xgyro = xgyro_raw[1]
            ygyro_raw = data[6].split(": ")
            ygyro = ygyro_raw[1]
            zgyro_raw = data[7].split(": ")
            zgyro = zgyro_raw[1]
            self.x_accel = round(self.convToMMS2(xaccel), 3)
            self.y_accel = round(self.convToMMS2(yaccel), 3)
            self.z_accel = round(self.convToMMS2(zaccel), 3)
            self.x_gyro = round(self.convToRads(xgyro), 3)
            self.y_gyro = round(self.convToRads(ygyro), 3)
            self.z_gyro = round(self.convToRads(zgyro), 3)
            print("X-accel: " + xaccel + ", Y-accel: " + yaccel + ", Z-accel: " + zaccel)
        except:
            print("could not retrieve IMU data from string")
        # print(data)

    def sendToModel(self, command):
        self.print_lock.acquire()
        self.client_socket.sendall(str.encode(command))
        data = self.client_socket.recv(1024)
        self.print_lock.release()
        print(f"Received '{data!r}' from server! ")
        imu_raw = data.decode()
        self.parse_IMU_data(imu_raw)
        return

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
            print("Connected to server")
        except:
            print("Could not connect to server, quitting")

    '''
    def get_IMU_loop(self):
        while True:
            IMU_data = self.UDP_socket.recvfrom(1024)
            IMU_msg = "{}".format(IMU_data[0])
            address = "{}".format(IMU_data[1])
            #self.parse_IMU_data(IMU_msg)
            print(IMU_msg)
            self.UDP_socket.sendto(str.encode("Received Data"), address)

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
    '''

    def createCommand(self, comp, value):
        cmd = "*** *** " + str(comp) + " " + str(value) + " ***"
        return cmd

    def create_commands(self, comp1, value1, comp2, value2, comp3, value3, comp4, value4, comp5, value5):
        cmd = "*** *** " + str(comp1) + " " + str(value1) + " " + str(comp2) + " " + str(value2) + " " + str(comp3) \
              + " " + str(value3) + " " + str(comp4) + " " + str(value4) + " " + str(comp5) + " " + str(value5) + " ***"
        return cmd
