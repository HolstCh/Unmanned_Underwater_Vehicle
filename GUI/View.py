import customtkinter as CTk
from Controller import Controller
import tkinter as Tk
import numpy
from PIL import Image, ImageTk
import os
from _thread import *
import threading
from threading import Thread
from time import sleep


# inherits from CTK's frame class and calls that constructor
class View(CTk.CTkFrame):
    def __init__(self, root, master, **kwargs):
        super().__init__(master, **kwargs)
        CTk.set_appearance_mode("dark")

        robotarium = CTk.CTkImage(Image.open(r"robotarium.png"), size=(260, 100))
        robotarium_label = CTk.CTkLabel(master=root, text="", image=robotarium)
        robotarium_label.image = robotarium

        uofc = CTk.CTkImage(Image.open(r"uofc.png"), size=(180, 100))
        uofc_label = CTk.CTkLabel(master=root, text="", image=uofc)
        uofc_label.image = uofc

        # labels for each widget
        left_servo_label = CTk.CTkLabel(master=root, text="Left Thruster Angle", anchor="w")
        left_thruster_label = CTk.CTkLabel(master=root, text="Left Thruster Power", anchor="w")
        right_servo_label = CTk.CTkLabel(master=root, text="Right Thruster Angle", anchor="w")
        right_thruster_label = CTk.CTkLabel(master=root, text="Right Thruster Power", anchor="w")
        tail_servo_label = CTk.CTkLabel(master=root, text="Tail Thruster Angle", anchor="w")
        tail_thruster_label = CTk.CTkLabel(master=root, text="Tail Thruster Power", anchor="w")
        left_gripper_open_label = CTk.CTkLabel(master=root, text="Left Gripper Open", anchor="w")
        left_gripper_closed_label = CTk.CTkLabel(master=root, text="Left Gripper Closed", anchor="w")
        right_gripper_open_label = CTk.CTkLabel(master=root, text="Right Gripper Open", anchor="w")
        right_gripper_closed_label = CTk.CTkLabel(master=root, text="Right Gripper Closed", anchor="w")

        # slider widgets
        self.left_servo_slider = CTk.CTkSlider(master=root, from_=0, to=1, orientation="vertical")
        self.left_servo_slider.bind("<ButtonRelease-1>", self.get_left_servo)
        self.left_thruster_slider = CTk.CTkSlider(master=root, from_=0, to=1, orientation="vertical")
        self.left_thruster_slider.bind("<ButtonRelease-1>", self.get_left_thruster)
        self.right_servo_slider = CTk.CTkSlider(master=root, from_=0, to=1, orientation="vertical")
        self.right_servo_slider.bind("<ButtonRelease-1>", self.get_right_servo)
        self.right_thruster_slider = CTk.CTkSlider(master=root, from_=0, to=1, orientation="vertical")
        self.right_thruster_slider.bind("<ButtonRelease-1>", self.get_right_thruster)
        self.tail_servo_slider = CTk.CTkSlider(master=root, from_=-0, to=1, orientation="vertical")
        self.tail_servo_slider.bind("<ButtonRelease-1>", self.get_tail_servo)
        self.tail_thruster_slider = CTk.CTkSlider(master=root, from_=0, to=1, orientation="vertical")
        self.tail_thruster_slider.bind("<ButtonRelease-1>", self.get_tail_thruster)
        self.left_gripper_slider = CTk.CTkSlider(master=root, from_=0, to=1, orientation="vertical")
        self.left_gripper_slider.bind("<ButtonRelease-1>", self.get_left_gripper)
        self.right_gripper_slider = CTk.CTkSlider(master=root, from_=0, to=1, orientation="vertical")
        self.right_gripper_slider.bind("<ButtonRelease-1>", self.get_right_gripper)

        # Dynamic Labels
        initial_servo = "0.0" + u'\N{DEGREE SIGN}'
        self.left_servo_value = CTk.StringVar(value=initial_servo)
        self.right_servo_value = CTk.StringVar(value=initial_servo)
        self.tail_servo_value = CTk.StringVar(value=initial_servo)
        self.left_servo_label_value = CTk.CTkLabel(master=root, textvariable=self.left_servo_value, anchor="w")
        self.right_servo_label_value = CTk.CTkLabel(master=root, textvariable=self.right_servo_value, anchor="w")
        self.tail_servo_label_value = CTk.CTkLabel(master=root, textvariable=self.tail_servo_value, anchor="w")

        initial_xaccel = "X-Direction Acceleration: 0.0 " + "m/s\N{SUPERSCRIPT TWO}"
        initial_yaccel = "Y-Direction Acceleration: 0.0 " + "m/s\N{SUPERSCRIPT TWO}"
        initial_zaccel = "Z-Direction Acceleration: 0.0 " + "m/s\N{SUPERSCRIPT TWO}"
        initial_xgyro = "X-Direction Angular Rotation: 0.0 " + "rad/s"
        initial_ygyro = "Y-Direction Angular Rotation: 0.0 " + "rad/s"
        initial_zgyro = "Z-Direction Angular Rotation: 0.0 " + "rad/s"
        self.x_accel_value = CTk.StringVar(value=initial_xaccel)
        self.y_accel_value = CTk.StringVar(value=initial_yaccel)
        self.z_accel_value = CTk.StringVar(value=initial_zaccel)
        self.x_gyro_value = CTk.StringVar(value=initial_xgyro)
        self.y_gyro_value = CTk.StringVar(value=initial_ygyro)
        self.z_gyro_value = CTk.StringVar(value=initial_zgyro)
        self.x_accel_label = CTk.CTkLabel(master=root, textvariable=self.x_accel_value, anchor="w", width=250)
        self.y_accel_label = CTk.CTkLabel(master=root, textvariable=self.y_accel_value, anchor="w", width=250)
        self.z_accel_label = CTk.CTkLabel(master=root, textvariable=self.z_accel_value, anchor="w", width=250)
        self.x_gyro_label = CTk.CTkLabel(master=root, textvariable=self.x_gyro_value, anchor="w", width=250)
        self.y_gyro_label = CTk.CTkLabel(master=root, textvariable=self.y_gyro_value, anchor="w", width=250)
        self.z_gyro_label = CTk.CTkLabel(master=root, textvariable=self.z_gyro_value, anchor="w", width=250)

        self.left_thruster_value = CTk.StringVar(value="0.0 %")
        self.right_thruster_value = CTk.StringVar(value="0.0 %")
        self.tail_thruster_value = CTk.StringVar(value="0.0 %")
        self.left_thruster_label_value = CTk.CTkLabel(master=root, textvariable=self.left_thruster_value, anchor="w")
        self.right_thruster_label_value = CTk.CTkLabel(master=root, textvariable=self.right_thruster_value, anchor="w")
        self.tail_thruster_label_value = CTk.CTkLabel(master=root, textvariable=self.tail_thruster_value, anchor="w")

        # combo box widgets
        # motor_status = CTk.CTkOptionMenu(master=root, values=["Disarmed", "Armed"])
        self.command_mode_value = CTk.StringVar(value="Single Command Mode")  # set initial value
        self.command_mode_menu = CTk.CTkOptionMenu(master=root,
                                                   values=["Single Command Mode", "Multiple Commands Mode"],
                                                   variable=self.command_mode_value, width=195)

        """
        # switch widget variables
        self.left_gripper_state = CTk.StringVar(value="open")
        self.right_gripper_state = CTk.StringVar(value="open")

        # switch widgets
        self.left_gripper_switch = CTk.CTkSwitch(master=root, text="Open Left Gripper", command=self.get_left_gripper,
                                                 variable=self.left_gripper_state, onvalue="open", offvalue="closed",
                                                 switch_width=75)
        self.right_gripper_switch = CTk.CTkSwitch(master=root, text="Open Right Gripper",
                                                  command=self.get_right_gripper,
                                                  variable=self.right_gripper_state, onvalue="open", offvalue="closed",
                                                  switch_width=75)
        
        """
        # button widgets
        self.reset_state = CTk.CTkButton(master=root, text="Reset State", command=self.set_state_default)
        self.multiple_commands = CTk.CTkButton(master=root, text="Send Commands", command=self.send_commands)

        # widget and label placements within frame
        robotarium_label.grid(column=0, row=0, pady=15)
        uofc_label.grid(column=5, row=0, pady=15)

        # Acceleration value/label placement
        self.x_accel_label.grid(column=0, row=2, padx=5, pady=15)
        self.y_accel_label.grid(column=0, row=3, padx=5, pady=15)
        self.z_accel_label.grid(column=0, row=4, padx=5, pady=15, sticky="N")
        self.x_gyro_label.grid(column=0, row=5, padx=20, pady=15)
        self.y_gyro_label.grid(column=0, row=6, padx=20, pady=15)
        self.z_gyro_label.grid(column=0, row=7, padx=20, pady=15, sticky="N")

        self.command_mode_menu.grid(column=3, row=0, padx=15)

        self.reset_state.grid(column=2, row=0, padx=10)
        self.multiple_commands.grid(column=4, row=0, padx=10)

        # self.left_gripper_switch.grid(column=2, row=1, padx=15)
        # self.right_gripper_switch.grid(column=3, row=1, padx=15)

        left_servo_label.grid(column=2, row=1)  # 2,2,2 - 2,3,4
        self.left_servo_slider.grid(column=2, row=2, rowspan=3)
        self.left_servo_label_value.grid(column=2, row=5, padx=15)

        tail_servo_label.grid(column=3, row=1)  # 2,2,2 - 10,11,12
        self.tail_servo_slider.grid(column=3, row=2, rowspan=3)
        self.tail_servo_label_value.grid(column=3, row=5, padx=15)

        right_servo_label.grid(column=4, row=1)  # 2,2,2 - 6,7,8
        self.right_servo_slider.grid(column=4, row=2, rowspan=3)
        self.right_servo_label_value.grid(column=4, row=5, padx=15)

        left_thruster_label.grid(column=2, row=6, padx=10)  # 3,3,3 - 2,3,4
        self.left_thruster_slider.grid(column=2, row=7, rowspan=3, padx=10)
        self.left_thruster_label_value.grid(column=2, row=10, padx=15)

        tail_thruster_label.grid(column=3, row=6, padx=10)  # 3,3,3 - 10,11,12
        self.tail_thruster_slider.grid(column=3, row=7, rowspan=3, padx=10)
        self.tail_thruster_label_value.grid(column=3, row=10, padx=15)

        right_thruster_label.grid(column=4, row=6, padx=10)  # 3,3,3 - 6,7,8
        self.right_thruster_slider.grid(column=4, row=7, rowspan=3, padx=10)
        self.right_thruster_label_value.grid(column=4, row=10, padx=15)

        left_gripper_open_label.grid(column=5, row=1, padx=10)
        self.left_gripper_slider.grid(column=5, row=2, rowspan=3, padx=10)
        left_gripper_closed_label.grid(column=5, row=5, padx=10)

        right_gripper_open_label.grid(column=5, row=6, padx=10)
        self.right_gripper_slider.grid(column=5, row=7, rowspan=3, padx=10)
        right_gripper_closed_label.grid(column=5, row=10, padx=10)

        self.controller = Controller()
        self.controller.start_gcs_connection()
        IMU_dummy = r"{'mavpackettype': 'RAW_IMU', 'time_usec': 287026014, 'xacc': -91, 'yacc': 445, 'zacc': -2318, 'xgyro': -91, 'ygyro': -872, 'zgyro': -449, 'xmag': 0, 'ymag': 0, 'zmag': 0}"

        self.root = master

    def threaded_IMU_updates(self):
        self.controller.sendToModel("*** *** IMU ***")
        self.update_IMU_labels()
        # sleep(1)

    def update_label(self):
        self.threaded_IMU_updates()
        self.root.after(500, self.update_label)

    def update_IMU_labels(self):
        x_accel = "X-Direction Acceleration: " + str(self.controller.getXaccel()) + " m/s\N{SUPERSCRIPT TWO}"
        y_accel = "Y-Direction Acceleration: " + str(self.controller.getYaccel()) + " m/s\N{SUPERSCRIPT TWO}"
        z_accel = "Z-Direction Acceleration: " + str(self.controller.getZaccel()) + " m/s\N{SUPERSCRIPT TWO}"
        x_gyro = "X-Direction Angular Rotation: " + str(self.controller.getXgyro()) + " rad/s"
        y_gyro = "Y-Direction Angular Rotation: " + str(self.controller.getYgyro()) + " rad/s"
        z_gyro = "Z-Direction Angular Rotation: " + str(self.controller.getZgyro()) + " rad/s"
        self.x_accel_value.set(x_accel)
        self.y_accel_value.set(y_accel)
        self.z_accel_value.set(z_accel)
        self.x_gyro_value.set(x_gyro)
        self.y_gyro_value.set(y_gyro)
        self.z_gyro_value.set(z_gyro)

    def convert_to_angle(self, value):
        return numpy.rint(-90 + value * (180))

    def convert_to_power(self, value):
        if value < 0.5:  # 0.0 to 0.49
            return numpy.rint((200 * value) - 100)
        elif value == 0.5:
            return 0.0
        elif value > 0.5:  # 0.51 to 1.0
            return numpy.rint((value - 0.5) * 2 * 100)

    def get_left_servo(self, event):
        print(self.left_servo_slider.get())
        angle = self.convert_to_angle(self.left_servo_slider.get())
        to_display = str(angle) + u'\N{DEGREE SIGN}'
        self.left_servo_value.set(to_display)
        if self.command_mode_menu.get() == "Single Command Mode":
            command = self.controller.createCommand("a1", self.left_servo_slider.get())
            self.controller.sendToModel(command)
        self.update_IMU_labels()

    def get_right_servo(self, event):
        print(self.right_servo_slider.get())
        angle = self.convert_to_angle(self.right_servo_slider.get())
        to_display = str(angle) + u'\N{DEGREE SIGN}'
        self.right_servo_value.set(to_display)
        if self.command_mode_menu.get() == "Single Command Mode":
            command = self.controller.createCommand("a2", self.right_servo_slider.get())
            self.controller.sendToModel(command)
        self.update_IMU_labels()

    def get_tail_servo(self, event):
        print(self.tail_servo_slider.get())
        angle = self.convert_to_angle(self.tail_servo_slider.get())
        to_display = str(angle) + u'\N{DEGREE SIGN}'
        self.tail_servo_value.set(to_display)
        if self.command_mode_menu.get() == "Single Command Mode":
            command = self.controller.createCommand("a3", self.tail_servo_slider.get())
            self.controller.sendToModel(command)
        self.update_IMU_labels()

    def get_left_thruster(self, event):
        print(self.left_thruster_slider.get())
        power = self.convert_to_power(self.left_thruster_slider.get())
        to_display = str(power) + " %"
        self.left_thruster_value.set(to_display)
        if self.command_mode_menu.get() == "Single Command Mode":
            command = self.controller.createCommand("t1", self.left_thruster_slider.get())
            self.controller.sendToModel(command)
        self.update_IMU_labels()

    def get_right_thruster(self, event):
        print(self.right_thruster_slider.get())
        power = self.convert_to_power(self.right_thruster_slider.get())
        to_display = str(power) + " %"
        self.right_thruster_value.set(to_display)
        self.update_IMU_labels()

    def get_tail_thruster(self, event):
        print(self.tail_thruster_slider.get())
        power = self.convert_to_power(self.tail_thruster_slider.get())
        to_display = str(power) + " %"
        self.tail_thruster_value.set(to_display)
        self.update_IMU_labels()

    def get_left_gripper(self, event):
        print(self.left_gripper_slider.get())
        if self.command_mode_menu.get() == "Single Command Mode":
            command = self.controller.createCommand("g1", self.left_gripper_slider.get())
            self.controller.sendToModel(command)
        self.update_IMU_labels()

    def get_right_gripper(self, event):
        print(self.left_gripper_slider.get())
        if self.command_mode_menu.get() == "Single Command Mode":
            command = self.controller.createCommand("g2", self.left_gripper_slider.get())
            self.controller.sendToModel(command)
        self.update_IMU_labels()

    def set_state_default(self):
        self.left_servo_slider.set(0.5)
        self.right_servo_slider.set(0.5)
        self.tail_servo_slider.set(0.5)
        self.left_thruster_slider.set(0.5)
        self.right_thruster_slider.set(0.5)
        self.tail_thruster_slider.set(0.5)
        to_display_servo = str(self.convert_to_angle(self.right_servo_slider.get())) + u'\N{DEGREE SIGN}'
        self.right_servo_value.set(to_display_servo)
        self.left_servo_value.set(to_display_servo)
        self.tail_servo_value.set(to_display_servo)
        self.left_gripper_slider.set(0.5)
        self.right_gripper_slider.set(0.5)
        commands = self.controller.create_commands("a1", self.left_servo_slider.get(), "a2",
                                                   self.right_servo_slider.get(), "a3", self.tail_servo_slider.get(),
                                                   "g1", self.left_gripper_slider.get(),
                                                   "g2", self.right_gripper_slider.get())
        self.controller.sendToModel(commands)
        self.update_IMU_labels()

    def send_commands(self):
        if self.command_mode_menu.get() == "Multiple Commands Mode":
            commands = self.controller.create_commands("a1", self.left_servo_slider.get(), "a2",
                                                       self.right_servo_slider.get(), "a3",
                                                       self.tail_servo_slider.get(),
                                                       "g1", self.left_gripper_slider.get(),
                                                       "g2", self.right_gripper_slider.get())
            self.controller.sendToModel(commands)

"""
    def get_left_gripper(self):
        print(self.left_gripper_state.get())
        command = self.controller.createCommand("g1", self.left_gripper_state.get())
        self.controller.sendToModel(command)

    def get_right_gripper(self):
        print(self.right_gripper_state.get())
        command = self.controller.createCommand("g2", self.right_gripper_state.get())
        self.controller.sendToModel(command)
"""
