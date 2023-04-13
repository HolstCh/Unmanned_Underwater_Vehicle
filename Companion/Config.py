# configurations for each electronic components in case of component or channel (pin) change; all values in program will change:

# pwm ranges for each servo: [min, default, max]
# set 25 pwm above recommended min and 25 pwm below recommended max
LEFT_SERVO_PWM_RANGE = [925,1500,2075]
RIGHT_SERVO_PWM_RANGE = [925,1500,2075]
TAIL_SERVO_PWM_RANGE = [925,1500,2075]

# channels for each servo (AUX pwm output pins):
LEFT_SERVO_CHANNEL = 10
RIGHT_SERVO_CHANNEL = 11
TAIL_SERVO_CHANNEL = 12

# pwm ranges for each gripper: [min (closed state), default (previous state), max (open state)]
LEFT_GRIPPER_PWM_RANGE = [1200,1500,1800]
RIGHT_GRIPPER_PWM_RANGE = [1200,1500,1800]

# channels for each gripper (AUX pwm output pins):
LEFT_GRIPPER_CHANNEL = 13
RIGHT_GRIPPER_CHANNEL = 14

# range for adjusting bidirectional speed of motor controller for thruster RPM
LEFT_THRUSTER_SPEED_RANGE = [-3200, 0, 3200]
RIGHT_THRUSTER_SPEED_RANGE = [-3200, 0, 3200]
TAIL_THRUSTER_SPEED_RANGE = [-3200, 0, 3200]

LEFT_THRUSTER_CHANNEL = 3
RIGHT_THRUSTER_CHANNEL = 4
TAIL_THRUSTER_CHANNEL = 5