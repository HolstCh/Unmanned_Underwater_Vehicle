import socket
from time import sleep, time
from threading import Thread
from Autopilot import Autopilot
from Servo import Servo
from Gripper import Gripper
from Thruster import Thruster
from Mavlink import Mavlink
from pymavlink import mavutil
from smc import SMC
from Config import *

"""The Model class is responsible for connections, computations, and commands sent and data recieved involving the Autopilot class/PX4.
The class recieves all input values corresponding to the Config.py file involving channels, pwm, and thruster/motor controller speed
AUX channels/pins are channels 9-16 (used for pwm servos/grippers) and MAIN channels are 1-9 (used for thrusters)"""
class Model:
    def __init__(self):
       self.gcs_connection = None
       self.gcs_address = None
       self.autopilot = None
       self.UDP_client = None
       self.IMU_data = {}

    """ 
        instantiate_servos() creates three Servo objects to organize each servo's channel and pwm range

        Output:
        servo_left, servo_right, and servo_tail objects which take values from Config.py
    """
    def instantiate_servos(self):
        # create a Servo instance on servo_10 (AUX output 2 which is the same as servo output channel 10)
        self.servo_left = Servo(LEFT_SERVO_CHANNEL, LEFT_SERVO_PWM_RANGE)
        # create a Servo instance on servo_11 (AUX output 3 which is the same as servo output channel 11)
        self.servo_right = Servo(RIGHT_SERVO_CHANNEL, RIGHT_SERVO_PWM_RANGE)
        # create a Servo instance on servo_12 (AUX output 4 which is the same as servo output channel 12)
        self.servo_tail = Servo(TAIL_SERVO_CHANNEL, TAIL_SERVO_PWM_RANGE)
    
    """ 
        instantiate_grippers() creates three Gripper objects to organize each gripper's channel and pwm range

        Output:
        gripper_left and gripper_right objects which take values from Config.py
    """
    def instantiate_grippers(self):
        # create a Gripper instance on gripper_13 (AUX output 5 which is the same as gripper output channel 13)
        self.gripper_left = Gripper(LEFT_GRIPPER_CHANNEL, LEFT_GRIPPER_PWM_RANGE)
        # create a Gripper instance on gripper_14 (AUX output 6 which is the same as gripper output channel 14)
        self.gripper_right = Gripper(RIGHT_GRIPPER_CHANNEL, RIGHT_GRIPPER_PWM_RANGE)

    """ 
        instantiate_thrusters() creates three Thruster objects to organize each thruster/motor controller channel and pwm range

        Output:
        thruster_left, thruster_right, and thruster_tail objects which take values from Config.py
    """
    def instantiate_thrusters(self):
        # create a Thruster instance that has a communication channel from the GUI but is not connected to hardware
        self.thruster_left = Thruster(LEFT_THRUSTER_CHANNEL, LEFT_THRUSTER_SPEED_RANGE)
        # create a Thruster instance that has a communication channel from the GUI but is not connected to hardware
        self.thruster_right = Thruster(RIGHT_THRUSTER_CHANNEL, RIGHT_THRUSTER_SPEED_RANGE)
        # create a Thruster instance that has a communication channel from the GUI but is not connected to hardware
        self.thruster_tail = Thruster(TAIL_THRUSTER_CHANNEL, TAIL_THRUSTER_SPEED_RANGE)
    
    # could be used to connect motor controllers from RPi through 3 USB ports or serial connections (currently inoperable)
    def start_motor_connection(self):
        serial_connections_to_motor_controllers = 3
        # self.mc1 = SMC('/dev/ttyUSB0', 115200)
        # self.mc2 = SMC('/dev/ttyUSB1', 115200)
        # self.mc3 = SMC('/dev/ttyUSB2', 115200)
        # open serial port and exit safe mode
        # self.mc1.init()

    """ 
        start_autopilot_connection() establishes a serial connection from the RPi to the PX4 using the Mavlink and Autopilot classes

        Output:
        Autopilot object that is used for communicating with the PX4
    """
    def start_autopilot_connection(self):
        # instantiate Mavlink object and pass connection data to establish mavlink connection to autopilot through serial
        mav_autopilot = Mavlink("/dev/ttyACM0", mavutil.mavlink.MAV_TYPE_SUBMARINE, mavutil.mavlink.MAV_AUTOPILOT_PX4, 
        0, 0, 0, 1, mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1)

        # instantiate Autopilot object, pass autopilot-mavlink connection data, and return Autopilot object to Model class
        self.autopilot = Autopilot(mav_autopilot.get_connection())

        # send HEARTBEAT message repeatedly from Companion to Autopilot every 1s or else Autopilot goes into failsafe mode
        mav_autopilot.start_heartbeat()

        # wait for a heartbeat from the autopilot before sending commands
        self.autopilot.master.wait_heartbeat()

        # print mavlink system that made connection: Companion system ID =  and Autopilot system ID = 1
        print("Source heartbeat from companion system: (system %u component %u)" % (self.autopilot.master.source_system, self.autopilot.master.source_component))
        print("Target heartbeat from autopilot system: (system %u component %u)" % (self.autopilot.master.target_system, self.autopilot.master.target_component))

        # set configurations for autopilot
        self.autopilot.set_config()
    
    def arm(self):
        self.autopilot.arm()

    def disarm(self):
        self.autopilot.disarm()
    
    def set_flight_mode(self, mode):
        # set flight mode: ['STABILIZE', 'ACRO', 'ALT_HOLD', 'AUTO', 'GUIDED', 'CIRCLE', 'SURFACE', 'POSHOLD', 'MANUAL']
        self.autopilot.set_mode(mode)

    """ 
        set_servo_pwm() communicates with Autopilot class and then the PX4 to send servo pwm to the correct channel/pin
        
        Inputs: 
        channel: corresponds to AUX pin/channel on the power management board
        pwm: corresponds to desired pwm value for servo

        Output:
        calls the set_servo() function within the Autopilot class which uses MAVlink to communicate to the PX4
    """
    def set_servo_pwm(self, channel, pwm):
        if channel == self.servo_left.servo_n:
            print(channel, pwm)
            self.autopilot.set_servo(self.servo_left.servo_n, pwm)
        elif channel == self.servo_right.servo_n:
            print(channel, pwm)
            self.autopilot.set_servo(self.servo_right.servo_n, pwm)
        elif channel == self.servo_tail.servo_n:
            print(channel, pwm)
            self.autopilot.set_servo(self.servo_tail.servo_n, pwm)
        else:
            print("Error: servo instances are only available on AUX outputs: " +  str(self.servo_left.servo_n-8) + ", " + str(self.servo_right.servo_n-8) + ", " + str(self.servo_tail.servo_n-8) + "/channels: " + 
                  str(self.servo_left.servo_n) + ", " + str(self.servo_right.servo_n) + ", " + str(self.servo_tail.servo_n))
    
    """ 
        set_gripper_pwm() communicates with Autopilot class and then the PX4 to send gripper pwm to the correct channel/pin

        Inputs: 
        channel: corresponds to AUX pin/channel on the power management board
        pwm: corresponds to desired pwm value for servo

        Output:
        calls the set_servo() function within the Autopilot class which uses MAVlink to communicate to the PX4
    """
    def set_gripper_pwm(self, channel, pwm):
        if channel == self.gripper_left.gripper_n:
            print(channel, pwm)
            self.autopilot.set_servo(self.gripper_left.gripper_n, pwm)
        elif channel == self.gripper_right.gripper_n:
            print(channel, pwm)
            self.autopilot.set_servo(self.gripper_right.gripper_n, pwm)
        else:
            print("Error: gripper instances are only available on AUX outputs: " + str(self.gripper_left.gripper_n-8) + ", " + str(self.gripper_right.gripper_n-8) + "/channels: " +
                  str(self.gripper_left.gripper_n) + ", " + str(self.gripper_right.gripper_n))
    
    # could be used to set thruster speeds to their corresponding channels but does not function right now
    def set_thruster_speed(self, channel, speed):
        if channel == self.thruster_left.thruster_n:
            print(channel, speed)
            #self.mc.speed(speed)
        elif channel == self.thruster_right.thruster_n:
            print(channel, speed)
        elif channel == self.thruster_tail.thruster_n:
            print(channel, speed)
        else:
            print("Error: thruster instance unavailable")

    # gets parameter from Autopilot and returns as dictionary
    def get_data(self, param):
        return self.autopilot.get_param_dict(param)
    
    # uses a thread to get IMU data every 1s from Autopilot
    def update_IMU_loop(self):
        #while True:
            self.IMU_data = self.autopilot.get_param_dict("RAW_IMU")
            #print(self.IMU_data)
            return str(self.IMU_data)

    """ 
        get_angle_pwm() uses the slider input from 0 - 1 and uses a linear conversion with the formula MINpwm + percent(MAXpwm - MINpwm).
        All pwm values are taken from the Config.py file.

        Inputs: 
        percent: value from 0 - 1 taken from the slider in the View module
        channel: corresponds to AUX pin/channel on the power management board

        Output:
        returns pwm value to be sent to a specific servo 
    """
    def get_angle_pwm(self, percent, channel):
        if channel == self.servo_left.servo_n:
            return (self.servo_left.min + (percent*(self.servo_left.max-self.servo_left.min)))
        elif channel == self.servo_right.servo_n:
            return (self.servo_right.min + (percent*(self.servo_right.max-self.servo_right.min)))
        elif channel == self.servo_tail.servo_n:
            return (self.servo_tail.min + (percent*(self.servo_tail.max-self.servo_tail.min)))
        else:
            print("Could not convert the invalid angle value, returning current value")
            return -1
        
    """ 
        get_state_pwm() uses the slider input from 0 - 1 and uses a linear conversion with the formula MINpwm + percent(MAXpwm - MINpwm).
        All pwm values are taken from the Config.py file.

        Inputs: 
        percent: value from 0 - 1 taken from the slider in the View module
        channel: corresponds to AUX pin/channel on the power management board

        Output:
        returns pwm value to be sent to a specific gripper channel on the power management board
    """
    def get_state_pwm(self, percent, channel):
        if channel == self.gripper_left.gripper_n:
            return (self.gripper_left.min + (percent*(self.gripper_left.max-self.gripper_left.min)))
        elif channel == self.gripper_right.gripper_n:
            return (self.gripper_right.min + (percent*(self.gripper_right.max-self.gripper_right.min)))
        else:
            print("Could not convert the invalid gripper state value, returning current value")
            return -1
    
    # get thruster speed (not functioning)
    def get_thruster_speed(self, percent, channel):
        if channel == self.thruster_left.thruster_n:
            return (self.thruster_left.min + (percent*(self.thruster_left.max-self.thruster_left.min)))
        elif channel == self.thruster_right.thruster_n:
            return (self.thruster_right.min + (percent*(self.thruster_right.max-self.thruster_right.min)))
        elif channel == self.thruster_tail.thruster_n:
            return (self.thruster_tail.min + (percent*(self.thruster_tail.max-self.thruster_tail.min)))
        else:
            print("Could not convert the invalid thruster power value, returning current value")
            return -1

    """ 
        parse_command() sorts each command recieved from the Controller module on the GCS and distributes value to corresponding channel/pin
        
        Input: 
        command: message that comes in a single pair such as "servo1 0.5" or a long message with all pairs included

        Output:
        calls get/set functions specific to the channel/electronic component
    """
    def parse_command(self, command):
        #s plit the command by spaces
        cmd_info = command.split()
        # If the first and second block is not "***", reject the command
        if cmd_info[0] != "***" and cmd_info[1] != "***":
            print("Could not parse command, command rejected")
            return 
        else: # scan for gripper, servo, or thruster requested
            end = len(cmd_info)
            for i in range(2, end, 1):
                if i%2 == 1:
                    i=i+1
                    continue
                if i%2 == 0:
                    if(cmd_info[i] == "IMU"): #If it is IMU update command, simply return to the start_gcs_connection while loop to send back data
                        return
                if i%2 == 0:
                    if(cmd_info[i] == "servo1"): #angle 1
                        try:
                            value = self.get_angle_pwm(float(cmd_info[i+1]), self.servo_left.servo_n)
                        except:
                            print("Could not parse angle value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert angle value to pwm, leaving at original value")
                            return
                        else:
                            print(value)
                            self.set_servo_pwm(self.servo_left.servo_n, int(value))
                            print("Left set servo command processed")
                    elif(cmd_info[i] == "servo2"): #angle 2
                        try:
                            value = self.get_angle_pwm(float(cmd_info[i+1]), self.servo_right.servo_n)
                        except:
                            print("Could not parse angle value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert angle value to pwm, leaving at original value")
                            return
                        else:
                            self.set_servo_pwm(self.servo_right.servo_n, int(value))
                            print("Right set servo command processed")
                    elif(cmd_info[i] == "servo3"): #angle 3
                        try:
                            value = self.get_angle_pwm(float(cmd_info[i+1]), self.servo_tail.servo_n)
                        except:
                            print("Could not parse angle value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert angle value to pwm, leaving at original value")
                            return
                        else:
                            self.set_servo_pwm(self.servo_tail.servo_n, int(value))
                            print("Tail set servo command processed")
                    elif(cmd_info[i] == "gripper1"): # left gripper
                        try:
                            value = self.get_state_pwm(float(cmd_info[i+1]), self.gripper_left.gripper_n)
                            print(value)
                        except:
                            print("Could not parse angle value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert angle value to pwm, leaving at original value")
                            return
                        else:
                            self.set_gripper_pwm(self.gripper_left.gripper_n, value)
                            print("Left set gripper command processed")
                    elif(cmd_info[i] == "gripper2"): # right gripper 
                        try:
                            value = self.get_state_pwm(float(cmd_info[i+1]), self.gripper_right.gripper_n)
                        except:
                            print("Could not parse angle value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert angle value to pwm, leaving at original value")
                            return
                        else:
                            self.set_gripper_pwm(self.gripper_right.gripper_n, value)
                            print("Right set gripper command processed")
                    elif(cmd_info[i] == "thruster1"): # left thruster
                        try:
                            value = self.get_thruster_speed(float(cmd_info[i+1]), self.thruster_left.thruster_n)
                        except:
                            print("Could not parse thruster power value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert thruster power value, leaving at original value")
                            return
                        else:
                            self.set_thruster_speed(self.thruster_left.thruster_n, value)
                            print("Left set thruster command processed")
                    elif(cmd_info[i] == "thruster2"): # left thruster
                        try:
                            value = self.get_thruster_speed(float(cmd_info[i+1]), self.thruster_right.thruster_n)
                        except:
                            print("Could not parse angle value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert thruster power value, leaving at original value")
                            return
                        else:
                            self.set_thruster_speed(self.thruster_right.thruster_n, value)
                            print("Right set thruster command processed")
                    elif(cmd_info[i] == "thruster3"): # left thruster
                        try:
                            value = self.get_thruster_speed(float(cmd_info[i+1]), self.thruster_tail.thruster_n)
                        except:
                            print("Could not parse angle value, try an actual number")
                            return
                        if(value == -1):
                            print("Could not convert thruster power value, leaving at original value")
                            return
                        else:
                            self.set_thruster_speed(self.thruster_tail.thruster_n, value)
                            print("Tail set thruster command processed")
    
    """ 
        start_gcs_connection() initiates a TCP connection in order to recieve requests or send responses to the GCS

        Output:
        maintains a connection with the GCS in a while loop that checks for requests being sent from the GCS. Also, sends IMU data to the GCS
    """                   
    def start_gcs_connection(self):
        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_address = ('', 5000) #server_address = ('0.0.0.0', 5000)
        server_socket.bind(server_address)

        # Listen for incoming connections
        server_socket.listen(4)
        print('Server is listening on {}:{}'.format(*server_address))

        while True:
            # Wait for a connection
            print('Waiting for a connection...')
            connection, client_address = server_socket.accept()
            try:
                print('Connection from', client_address)

                # initialize gcs connection and address to Model class
                self.gcs_connection = connection
                self.gcs_address = client_address 

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    print('Received {!r}'.format(data))
                    print(data.decode())
                    # send command for parsing
                    self.parse_command(data.decode())
                    # just for checking values changing:
                    self.autopilot.read_param('SERVO_OUTPUT_RAW')
                    if data:
                        print('Sending data back to the client')
                        IMU_data = self.update_IMU_loop()
                        connection.sendall(str.encode(IMU_data))
                    else:
                        print('No more data from', client_address)
                        break

            finally:
                # Clean up the connection
                connection.close()

# point of execution when running this file, this function inputs all values and starts all connections
if __name__ == '__main__':
    model = Model()
    model.start_autopilot_connection()
    model.instantiate_servos()
    model.instantiate_grippers()
    model.instantiate_thrusters()
    model.start_motor_connection()
    model.start_gcs_connection()
    
