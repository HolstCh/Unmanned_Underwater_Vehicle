import socket
from time import sleep
from threading import Thread
from Autopilot import Autopilot
from Servo import Servo
from Gripper import Gripper
from Mavlink import Mavlink
from pymavlink import mavutil

class Model:
    def __init__(self):
       self.gcs_connection = None
       self.gcs_address = None
       self.autopilot = None
       self.IMU_data = {}

    # AUX channels are channels 9-16
    def instantiate_servos(self):
        # create a Servo instance on servo_10 (AUX output 2 which is the same as servo output channel 10)
        self.servo_left = Servo(10)
        # create a Servo instance on servo_11 (AUX output 3 which is the same as servo output channel 11)
        self.servo_right = Servo(11)
        # create a Servo instance on servo_12 (AUX output 4 which is the same as servo output channel 12)
        self.servo_tail = Servo(12)
    
    def instantiate_grippers(self):
        # create a Gripper instance on gripper_13 (AUX output 5 which is the same as gripper output channel 13)
        self.gripper_left = Gripper(13)
        # create a Gripper instance on gripper_14 (AUX output 6 which is the same as gripper output channel 14)
        self.gripper_right = Gripper(14)

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

    def set_servo(self, channel, pwm):
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

    def set_all_servos_default(self):
        self.autopilot.set_servo(self.servo_left.servo_n, self.servo_left.default)
        self.autopilot.set_servo(self.servo_right.servo_n, self.servo_right.default)
        self.autopilot.set_servo(self.servo_tail.servo_n, self.servo_tail.default)

    def open_gripper(self, channel):
        if channel == self.gripper_left.gripper_n:
            print(channel, self.gripper_left.max)
            self.autopilot.set_servo(self.gripper_left.gripper_n, self.gripper_left.max)
        elif channel == self.gripper_right.gripper_n:
            print(channel, self.gripper_right.max)
            self.autopilot.set_servo(self.gripper_right.gripper_n, self.gripper_right.max)
        else:
            print("Error: gripper instances are only available on AUX outputs: " + str(self.gripper_left.gripper_n-8) + ", " + str(self.gripper_right.gripper_n-8) + "/channels: " +
                  str(self.gripper_left.gripper_n) + ", " + str(self.gripper_right.gripper_n))
    
    def close_gripper(self, channel):
        if channel == self.gripper_left.gripper_n:
            print(channel, self.gripper_left.min)
            self.autopilot.set_servo(self.gripper_left.gripper_n, self.gripper_left.min)
        elif channel == self.gripper_right.gripper_n:
            print(channel, self.gripper_right.min)
            self.autopilot.set_servo(self.gripper_right.gripper_n, self.gripper_right.min)
        else:
            print("Error: gripper instances are only available on AUX outputs: " + str(self.gripper_left.gripper_n-8) + ", " + str(self.gripper_right.gripper_n-8) + "/channels: " +
                  str(self.gripper_left.gripper_n) + ", " + str(self.gripper_right.gripper_n))

    def get_data(self, param):
        return self.autopilot.get_param_dict(param)
    
    def update_IMU_loop(self):
        while True:
            self.IMU_data = self.autopilot.get_param_dict("RAW_IMU")
            print(self.IMU_data)
            sleep(1)
    
    def update_IMU(self):
        # create thread to and assign it to update IMU data every 1s until program exits for real time data display
        self.thread = Thread(target=self.update_IMU_loop, daemon=True)
        self.thread.start()

    def get_angle_pwm(self, angle):
        conv_factor = 1000
        if(angle < 0 and angle >= -90):
            return -1*conv_factor*angle
        elif(angle >= 0 and angle <= 90):
            return conv_factor*angle
        else:
            print("Could not convert the invalid angle value, returning current value")
            return -1

    def get_gripper_pwm(self, state):
        if(state == "open"): #range is 1530 < value < 1900
            return self.gripper_left.max
        elif(state == "closed"): #range is 1100 < value < 1470
            return self.gripper_left.min
        else:
            print("could not parse gripper pwm input, returning current state")
            return self.gripper_left.default #pwm is 1500 for current state

    def parse_command(self, command):
        #split the command by spaces
        cmd_info = command.split()
        #If the first block is not " *** ", reject the command
        if cmd_info[0] != "***":
            print("Could not parse command, command rejected")
            return 
        else: #scan for gripper, servo, or thruster requested
            if(cmd_info[1] == "a1"): #angle 1
                try:
                    value = self.get_angle_pwm(cmd_info[2].float())
                except:
                    print("Could not parse angle value, try an actual number")
                    return
                if(value == -1):
                    print("Could not convert angle value to pwm, leaving at original value")
                    return
                else:
                    self.set_servo(self.servo_left.servo_n, value)
                    print("Set servo command processed")
                    return
            elif(cmd_info[1] == "a2"): #angle 2
                try:
                    value = self.get_angle_pwm(cmd_info[2].float())
                except:
                    print("Could not parse angle value, try an actual number")
                    return
                if(value == -1):
                    print("Could not convert angle value to pwm, leaving at original value")
                    return
                else:
                    self.set_servo(self.servo_right.servo_n, value)
                    print("Set servo command processed")
                    return
            elif(cmd_info[1] == "a3"): #angle 3
                try:
                    value = self.get_angle_pwm(cmd_info[2].float())
                except:
                    print("Could not parse angle value, try an actual number")
                    return
                if(value == -1):
                    print("Could not convert angle value to pwm, leaving at original value")
                    return
                else:
                    self.set_servo(self.servo_tail.servo_n, value)
                    print("Set servo command processed")
                    return    

    
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
                    # send command for parsing
                    # self.parse_command(self, data)
                    if data:
                        print('Sending data back to the client')
                        connection.sendall(data)
                    else:
                        print('No more data from', client_address)
                        break

            finally:
                # Clean up the connection
                connection.close()

if __name__ == '__main__':
    model = Model()
    model.start_autopilot_connection()
    model.instantiate_servos()
    model.instantiate_grippers()
    # model.set_flight_mode("MANUAL")
    # model.arm()
    model.set_servo(model.servo_left.servo_n, 1610)
    model.set_servo(model.servo_right.servo_n, 1611)
    model.set_servo(model.servo_tail.servo_n, 1612)
    model.close_gripper(model.gripper_left.gripper_n)
    model.open_gripper(model.gripper_right.gripper_n)
    model.autopilot.read_param('SERVO_OUTPUT_RAW')
    # model.update_IMU()
    # model.start_gcs_connection()

"""
        for us in range(1100, 1900, 50):
            autopilot.master.set_servo(11, us)
            sleep(0.5)

        while True:
            autopilot.master.set_servo(servo_left.servo_n, servo_left.min)
            autopilot.read_param('SERVO_OUTPUT_RAW')
            sleep(5)
            autopilot.master.set_servo(servo_left.servo_n, servo_left.default)
            autopilot.read_param('SERVO_OUTPUT_RAW')
            sleep(5)
            autopilot.master.set_servo(servo_left.servo_n, servo_left.max)
            autopilot.read_param('SERVO_OUTPUT_RAW')
            sleep(5)

        autopilot.stop_servo(9)
        autopilot.disarm()

        # note: manual mode used for RC inputs which use servo functions to map to servo output channels.
        # set RC channels all to 65355 which means ignore
        autopilot.set_default_rc_channels()
        # autopilot.arm()
        # set each input RC channel PWM 
        autopilot.set_pitch(1160) # RC input channel 1
        autopilot.set_roll(1160) # RC input channel 2
        autopilot.set_throttle(1160) # RC input channel 3
        autopilot.set_yaw(1160) # RC input channel 4
        autopilot.set_forward(1180) # RC input channel 5
        autopilot.set_lateral(1180) # RC input channel 6
        autopilot.master.SERVO10_FUNCTION = 1 # enable RCPassThru on AUX servo output channel 10
        autopilot.master.SERVO11_FUNCTION = 1 # enable RCPassThru on AUX servo output channel 11
        autopilot.master.SERVO12_FUNCTION = 1 # enable RCPassThru on AUX servo which is output channel 12
        autopilot.read_param('RC_CHANNELS')
        autopilot.read_param('SERVO_OUTPUT_RAW')
        # autopilot.disarm()
"""
