import sys
from time import sleep
from pymavlink import mavutil
from Mavlink import Mavlink

# thruster class which assigns channel and pwm values for it's corresonding servo
class Thruster:
    # recommended pwm values are the following: 1000: full reverse, 1500: stopped/default, 2000: full forward supplied to ESC
    def __init__(self, master, servo_n, pwm_range=[1000,1500,2000]):
        self.master = master
        self.servo_n = servo_n
        self.pwm_range = pwm_range
        self.min, self.default, self.max = pwm_range
        
# Communication between companion and autopilot
class Autopilot:
    def __init__(self, master):
        self.master = master
    
    def read_params(self):
        self.master.mav.param_request_list_send(
        self.master.target_system, self.master.target_component
        )
        while True:
            sleep(0.01)
            try:
                message = self.master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
                print('name: %s\tvalue: %d' % (message['param_id'],
                                            message['param_value']))
            except Exception as error:
                print(error)

    def read_param(self, param):
        """self.master.mav.param_request_read_send(self.master.target_system, self.master.target_component, str.encode(param), -1)
        message = self.master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('name: %s\tvalue: %d' % (message['param_id'], message['param_value']))"""
        msg = self.master.recv_match(type=param, blocking=True).to_dict()
        print(msg)

    def arm(self):
            self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0)
            print("Waiting for the vehicle to arm ...\n")
            self.master.motors_armed_wait()
            print('Motors armed!\n')

    def disarm(self):
            self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0)
            print("Waiting for the vehicle to disarm ...\n")
            self.master.motors_disarmed_wait()
            print('Motors disarmed!\n')

    def set_config(self):
        # set # of FMU PWM outputs to motor controller which are pins: AUX1, AUX2, AUX3, and AUX4
        self.master.BRD_PWM_COUNT = 6

    def set_mode(self, mode):
        # Check if mode is available
        if mode not in self.master.mode_mapping():
            print('Unknown mode : {}'.format(mode))
            print('Try:', list(self.master.mode_mapping().keys()))
            sys.exit(1)

        # Get mode ID
        mode_id = self.master.mode_mapping()[mode]
        # Set new mode
        self.master.set_mode(mode_id)

        while True:
            # Wait for ACK command
            # Would be good to add mechanism to avoid endlessly blocking
            # if the autopilot sends a NACK or never receives the message
            ack_msg = self.master.recv_match(type='COMMAND_ACK', blocking=True)
            ack_msg = ack_msg.to_dict()

            # Continue waiting if the acknowledged command is not `set_mode`
            if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
                continue

            # Print the ACK result !
            print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
            break

    def set_servo(self, channel, pwm):
        self.master.mav.command_long_send(self.master.target_system,
                                                   self.master.target_component,
                                                   mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0,
                                                   channel, pwm,
                                                   0, 0, 0, 0, 0)
    def stop_servo(self, channel, pwm=1500):
        self.master.mav.command_long_send(self.master.target_system,
                                                   self.master.target_component,
                                                   mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0,
                                                   channel, pwm,
                                                   0, 0, 0, 0, 0)
    def set_default_rc_channels(self):
        self.rc_channel_values = [65535 for i in range(18)] # set first 9 RC channels, 65535 means ignore; otherwise use pwm values

    def set_rc_channel_pwm(self, channel_id, pwm=1500):

        if channel_id < 1 or channel_id > 18:
            print("Channel must be between 1-18")
            return

        self.rc_channel_values[channel_id - 1] = pwm
        self.master.mav.rc_channels_override_send(
            self.master.target_system,                # target_system
            self.master.target_component,             # target_component
            *self.rc_channel_values)                  # RC channel list, in microseconds.
            
    def set_pitch(self, pwm):
        self.set_rc_channel_pwm(1, pwm)
    
    def set_roll(self, pwm):
        self.set_rc_channel_pwm(2, pwm)
    
    def set_throttle(self, pwm):
        self.set_rc_channel_pwm(3, pwm)
    
    def set_yaw(self, pwm):
        self.set_rc_channel_pwm(4, pwm)
    
    def set_forward(self, pwm):
        self.set_rc_channel_pwm(5, pwm)
    
    def set_lateral(self, pwm):
        self.set_rc_channel_pwm(6, pwm)

if __name__ == '__main__':
    
    # establish mavlink connection to autopilot through serial
    mav_autopilot = Mavlink("/dev/ttyACM0", mavutil.mavlink.MAV_TYPE_SUBMARINE, mavutil.mavlink.MAV_AUTOPILOT_PX4, 
    0, 0, 0, 1, mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1)

    # instantiate autopilot object and pass autopilot-mavlink connection
    autopilot = Autopilot(mav_autopilot.get_connection())
   
    # send HEARTBEAT message repeatedly from Companion to Autopilot every 1s or else Autopilot goes into failsafe mode
    mav_autopilot.start_heartbeat()

    # Wait for a heartbeat from the PX4 before sending commands
    autopilot.master.wait_heartbeat()

    # print mavlink system that made connection: Companion system ID = 127, GCS system ID = 255, Autopilot system ID = 1
    print("Source heartbeat from companion system: (system %u component %u)" % (autopilot.master.source_system, autopilot.master.source_component))
    print("Target heartbeat from autopilot system: (system %u component %u)" % (autopilot.master.target_system, autopilot.master.target_component))

    # set configurations for autopilot
    autopilot.set_config()

    # set mode: ['STABILIZE', 'ACRO', 'ALT_HOLD', 'AUTO', 'GUIDED', 'CIRCLE', 'SURFACE', 'POSHOLD', 'MANUAL']
    # note: manual mode used for RC inputs which use servo functions to map to servo output channels.
    autopilot.set_mode('MANUAL')
    
    RC_MODE = 0
    SERVO_MODE = 1

    if RC_MODE:
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
        autopilot.master.SERVO9_FUNCTION = 1 # enable RCPassThru on AUX servo output channel 9
        autopilot.master.SERVO10_FUNCTION = 1 # enable RCPassThru on AUX servo output channel 10
        autopilot.master.SERVO11_FUNCTION = 1 # enable RCPassThru on AUX servo which is output channel 11
        autopilot.read_param('RC_CHANNELS') # only works with MAVlink V1.0?
        autopilot.read_param('SERVO_OUTPUT_RAW')
        # autopilot.disarm()

    if SERVO_MODE:
        autopilot.arm()
        autopilot.master.SERVO9_FUNCTION = 0 # disable servo functions to use set_servo()
        autopilot.master.mav.command_long_send(autopilot.master.target_system, autopilot.master.target_component, mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0, 0, 300, 0, 0, 0, 0, 0, 1)
        print(mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE)
        ack = False
        while not ack:
            ack_msg = autopilot.master.recv_match(type='COMMAND_ACK', blocking=True)
            ack_msg = ack_msg.to_dict()
            print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
            print(ack_msg)
            break
            
        # create a thruster instance on servo_9 (AUX output 1 which is same as servo output channel 9)
        thruster1 = Thruster(autopilot.master, 9)
        # create a thruster instance on servo_1 (AUX output 2 which is same as servo output channel 10)
        # thruster2 = Thruster(autopilot.master, 10)
        # create a thruster instance on servo_1 (AUX output 3 which is same as servo output channel 11)
        # thruster3 = Thruster(autopilot.master, 11)

        for i in range(3):
            autopilot.master.set_servo(thruster1.servo_n, thruster1.default)
            autopilot.read_param('SERVO_OUTPUT_RAW')
            sleep(1)

        autopilot.stop_servo(9)
        autopilot.disarm()