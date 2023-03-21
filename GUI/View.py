import customtkinter as CTk
import tkinter as Tk


# inherits from CTK's frame class and calls that constructor
class View(CTk.CTkFrame):
    def __init__(self, root, master, **kwargs):
        super().__init__(master, **kwargs)
        CTk.set_appearance_mode("dark")

        # labels for each widget
        left_servo_label = CTk.CTkLabel(master=root, text="Left Thruster Angle (°)", anchor="w")
        left_thruster_label = CTk.CTkLabel(master=root, text="Left Thruster RPM", anchor="w")
        right_servo_label = CTk.CTkLabel(master=root, text="Right Thruster Angle (°)", anchor="w")
        right_thruster_label = CTk.CTkLabel(master=root, text="Right Thruster RPM", anchor="w")
        tail_servo_label = CTk.CTkLabel(master=root, text="Tail Thruster Angle (°)", anchor="w")
        tail_thruster_label = CTk.CTkLabel(master=root, text="Tail Thruster RPM", anchor="w")
        motor_status_label = CTk.CTkLabel(master=root, text="Motor Status", anchor="w")
        flight_mode_label = CTk.CTkLabel(master=root, text="Flight Mode", anchor="w")

        # slider widgets
        self.left_servo_slider = CTk.CTkSlider(master=root, from_=-90, to=90, orientation="vertical")
        self.left_servo_slider.bind("<ButtonRelease-1>", self.get_left_servo)
        self.left_thruster_slider = CTk.CTkSlider(master=root, from_=-28, to=28, orientation="vertical")
        self.left_thruster_slider.bind("<ButtonRelease-1>", self.get_left_thruster)
        self.right_servo_slider = CTk.CTkSlider(master=root, from_=-90, to=90, orientation="vertical")
        self.right_servo_slider.bind("<ButtonRelease-1>", self.get_right_servo)
        self.right_thruster_slider = CTk.CTkSlider(master=root, from_=-28, to=28, orientation="vertical")
        self.right_thruster_slider.bind("<ButtonRelease-1>", self.get_right_thruster)
        self.tail_servo_slider = CTk.CTkSlider(master=root, from_=-90, to=90, orientation="vertical")
        self.tail_servo_slider.bind("<ButtonRelease-1>", self.get_tail_servo)
        self.tail_thruster_slider = CTk.CTkSlider(master=root, from_=-28, to=28, orientation="vertical")
        self.tail_thruster_slider.bind("<ButtonRelease-1>", self.get_tail_thruster)

        # combo box widgets
        motor_status = CTk.CTkOptionMenu(master=root, values=["Disarmed", "Armed"])
        flight_mode = CTk.CTkOptionMenu(master=root,
                                        values=["Manual", "Stabilize", "Acro", "Altitude Hold", "Auto", "Guided",
                                                "Circle", "Surface", "Position Hold"])
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

        # widget and label placements within frame
        motor_status_label.grid(column=0, row=0, pady=15)
        motor_status.grid(column=0, row=1, sticky="N", padx=15)

        flight_mode_label.grid(column=1, row=0, pady=15)
        flight_mode.grid(column=1, row=1, sticky="N", padx=15)

        self.left_gripper_switch.grid(column=2, row=0, padx=15)
        self.right_gripper_switch.grid(column=3, row=0, padx=15)

        left_servo_label.grid(column=2, row=1)
        self.left_servo_slider.grid(column=2, row=2, rowspan=3)

        left_thruster_label.grid(column=3, row=1, padx=10)
        self.left_thruster_slider.grid(column=3, row=2, rowspan=3, padx=10)

        right_servo_label.grid(column=2, row=5)
        self.right_servo_slider.grid(column=2, row=6, rowspan=3)

        right_thruster_label.grid(column=3, row=5, padx=10)
        self.right_thruster_slider.grid(column=3, row=6, rowspan=3, padx=10)

        tail_servo_label.grid(column=2, row=9)
        self.tail_servo_slider.grid(column=2, row=10, rowspan=3)

        tail_thruster_label.grid(column=3, row=9, padx=10)
        self.tail_thruster_slider.grid(column=3, row=10, rowspan=3, padx=10)

        # example of setting value of slider:
        val = 95
        self.left_servo_slider.set(val)

    def get_left_servo(self, event):
        print(self.left_servo_slider.get())

    def get_right_servo(self, event):
        print(self.right_servo_slider.get())

    def get_tail_servo(self, event):
        print(self.tail_servo_slider.get())

    def get_left_thruster(self, event):
        print(self.left_thruster_slider.get())

    def get_right_thruster(self, event):
        print(self.right_thruster_slider.get())

    def get_tail_thruster(self, event):
        print(self.tail_thruster_slider.get())

    def get_left_gripper(self):
        print(self.left_gripper_state.get())

    def get_right_gripper(self):
        print(self.right_gripper_state.get())
