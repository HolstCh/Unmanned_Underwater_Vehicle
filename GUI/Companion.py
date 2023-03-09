import time
from pymavlink import mavutil
from Mavlink import Mavlink
from Autopilot import Autopilot
import os

# Communication from companion to GCS
class Companion:
      def __init__(self, master):
        self.master = master

    
# udpout is client, which is the companion computer, IPV4 is target address of GCS ethernet
mav_comp= Mavlink('udpout:192.168.137.1:14550', mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER, 
mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0, 127, mavutil.mavlink.MAV_COMP_ID_ONBOARD_COMPUTER)

# instantiate companion object and pass Companion-GCS-Mavlink connection
companion = Companion(mav_comp.get_connection())

# send HEARTBEAT message repeatedly every 1s
mav_comp.start_heartbeat()

# Wait for a heartbeat before sending commands
companion.master.wait_heartbeat()

# print mavlink system that made connection: GCS system ID = 255, Autopilot system ID = 1, Companion system ID = 127 
print("Source heartbeat from Companion system: (system %u component %u)" % (companion.master.source_system, companion.master.source_component))                                 
print("Target heartbeat from GCS system: (system %u component %u)" % (companion.master.target_system, companion.master.target_component))

# send PING message from RPi to GCS                                            
msg = None
while not msg:
    companion.master.mav.ping_send(
        int(time.time() * 1e6), # Unix time in microseconds
        0, # Ping number
        0, # Request ping of all systems
        0 # Request ping of all components
    )
    msg = companion.master.recv_match()
    time.sleep(0.5)

# recv message from GCS to RPi
while True:
    msg = companion.master.recv_match()
    if not msg:
        continue
    if msg.get_type() == 'HEARTBEAT' or msg.get_type() == 'PING':
        print("\n\n*****Got message: %s*****" % msg.get_type())
        print("Message: %s" % msg)