import View
import socket
from time import sleep
from threading import Thread
import threading
from _thread import *

""" Controller class assigns values to each electronic component, creates and sends commands to Model, receives IMU data
 from Model. The class supports additional electronic components by adding params and values to send different types of 
 messages """


class Controller:
    def __init__(self):
        self.servo_left_param = "servo1"
        self.servo_right_param = "servo2"
        self.servo_tail_param = "servo3"
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

    """ 
        set_() functions assign a value to their corresponding electronic component
        
        Input
        value: percent value from 0 - 1 from each corresponding slider
        
        Output
        sets value in Controller object within the View module
    """

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

    def set_thruster_left(self, value):
        self.thruster_left_value = value

    def set_thruster_right(self, value):
        self.thruster_right_value = value

    def set_thruster_tail(self, value):
        self.thruster_tail_value = value

    """
        single_command_() functions create a single command corresponding to a specific electronic component and sends 
        the command to Model class
        
        Output
        takes parameter names/values from within Controller class that are set, creates a command, and then sends the
        command to Model.py on the RPi
    """

    def single_command_servo_left(self):
        cmd = self.create_command(self.servo_left_param, self.servo_left_value)
        self.sendToModel(cmd)

    def single_command_servo_right(self):
        cmd = self.create_command(self.servo_right_param, self.servo_right_value)
        self.sendToModel(cmd)

    def single_command_servo_tail(self):
        cmd = self.create_command(self.servo_tail_param, self.servo_tail_value)
        self.sendToModel(cmd)

    def single_command_gripper_right(self):
        cmd = self.create_command(self.gripper_right_param, self.gripper_right_value)
        self.sendToModel(cmd)

    def single_command_gripper_left(self):
        cmd = self.create_command(self.gripper_left_param, self.gripper_left_value)
        self.sendToModel(cmd)

    def single_command_thruster_left(self):
        cmd = self.create_command(self.thruster_left_param, self.thruster_left_value)
        self.sendToModel(cmd)

    def single_command_thruster_right(self):
        cmd = self.create_command(self.thruster_right_param, self.thruster_right_value)
        self.sendToModel(cmd)

    def single_command_thruster_tail(self):
        cmd = self.create_command(self.thruster_tail_param, self.thruster_tail_value)
        self.sendToModel(cmd)

    """
      multiple_commands() creates all commands for all electronic components and sends 
      the command to Model class on RPi

      Output
      takes all parameter names/values from within Controller class that are set, creates all commands, and then sends the
      commands to Model.py on the RPi
    """

    def multiple_commands(self):
        cmd = self.create_commands()
        self.sendToModel(cmd)

    # get data from IMU dictionary that is returned
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

    # conversions for IMU data to be displayed
    def convToMMS2(self, val):
        value = int(val)
        return value * (9.81 / 1000)

    def convToRads(self, val):
        value = int(val)
        return value / 1000

    # parse IMU data from dictionary that is sent from Model class
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
        except:
            print("could not retrieve IMU data from string")

    # sends command to Model where the Model deciphers which electronic component to send the command to
    def sendToModel(self, command):
        self.print_lock.acquire()
        self.client_socket.sendall(str.encode(command))
        data = self.client_socket.recv(1024)
        self.print_lock.release()
        # print(f"Received '{data!r}' from server! ")
        imu_raw = data.decode()
        self.parse_IMU_data(imu_raw)
        return

    # end TCP connection from GCS to RPi
    def end_gcs_connection(self):
        try:
            self.client_socket.close()
        except:
            print("could not close socket properly")
        return

    # create TCP connection from GCS to RPi
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

    # creates command for a single electronic component and sends it to Model
    def create_command(self, comp, value):
        cmd = "*** *** " + str(comp) + " " + str(value) + " ***"
        return cmd

    # creates commands for every electronic component and sends them to Model
    def create_commands(self):
        cmd = "*** *** " + self.servo_left_param + " " + str(self.servo_left_value) + " " + self.servo_right_param + " " \
              + str(self.servo_right_value) + " " + self.servo_tail_param + " " + str(self.servo_tail_value) + " " + \
              self.gripper_left_param + " " + str(self.gripper_left_value) + " " + self.gripper_right_param + " " + \
              str(self.gripper_right_value) + " " + self.thruster_left_param + " " + str(self.thruster_left_value) + " " \
              + self.thruster_right_param + " " + str(
            self.thruster_right_value) + " " + self.thruster_tail_param + " " + \
              str(self.thruster_tail_value) + " ***"
        return cmd
