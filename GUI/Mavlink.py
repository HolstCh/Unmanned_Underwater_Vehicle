from threading import Thread
from pymavlink import mavutil
from time import sleep

# mavlink connection class for GCS or Autopilot
class Mavlink:
        def __init__(self, connection_string, mav_type, autopilot, base_mode, custom_mode, mav_version, source_system, source_component, dialect="common"):
            self.connection_string = connection_string
            self.mav_type = mav_type
            self.autopilot = autopilot
            self.base_mode = base_mode
            self.custom_mode = custom_mode
            self.mav_version = mav_version
            self.source_system = source_system
            self.source_component = source_component
            self.dialect = dialect

        def get_connection(self):
            if self.mav_type == mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER:
                # create the connection to the companion where system ID = 127, component ID = 191 in Mavlink network
                self.master = mavutil.mavlink_connection(self.connection_string, source_system=self.source_system, source_component=self.source_component, dialect=self.dialect)
            elif self.mav_type == mavutil.mavlink.MAV_TYPE_SUBMARINE:
                # create the connection to the autopilot where system ID = 1, component ID = 1 in Mavlink network
                self.master = mavutil.mavlink_connection(self.connection_string, baud=57600, source_system=self.source_system, source_component=self.source_component, dialect=self.dialect)
            elif self.mav_type == mavutil.mavlink.MAV_TYPE_GCS:
                # create the connection to the GCS where system ID = 255, component ID = 190 in Mavlink network
                self.master = mavutil.mavlink_connection(self.connection_string, source_system=self.source_system, source_component=self.source_component, dialect=self.dialect)
            return self.master

        def start_heartbeat(self):
            # create thread to and assign it to send heartbeat message until program exits
            self.thread = Thread(target=self.heartbeat_send_loop, daemon=True)
            self.thread.start()

        def heartbeat_send_loop(self):
            # send heartbeat message continously at 1 Hz, daemon thread runs until main thread is done executing
            while True:
                self.master.mav.heartbeat_send(self.mav_type, self.autopilot, self.base_mode, self.custom_mode, self.mav_version)
                sleep(1)
