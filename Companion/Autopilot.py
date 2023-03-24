import sys
from time import sleep
from pymavlink import mavutil
from Mavlink import Mavlink
import os

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
        self.master.mav.param_request_read_send(self.master.target_system, self.master.target_component, str.encode(param), -1)
        msg = self.master.recv_match(type=param, blocking=True).to_dict()
        print(msg)
    
    def get_param_dict(self, param):
        self.master.mav.param_request_read_send(self.master.target_system, self.master.target_component, str.encode(param), -1)
        return self.master.recv_match(type=param, blocking=True).to_dict()

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
        # set version to Mavlink 2
        os.environ['MAVLINK20'] = '1'
        # disable servo functions to use MAV_CMD_DO_SET_SERVO
        self.master.SERVO10_FUNCTION = 0 
        self.master.SERVO11_FUNCTION = 0
        self.master.SERVO12_FUNCTION = 0
        self.master.SERVO13_FUNCTION = 0
        self.master.SERVO14_FUNCTION = 0

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

    # RC channels are for further development involving joystick/controller device using RC reciever                                              
    def set_default_rc_channels(self):
        self.rc_channel_values = [65535 for i in range(18)] # set first 18 RC channels, 65535 means ignore; otherwise use pwm values

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
