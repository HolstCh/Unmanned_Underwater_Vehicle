import customtkinter as CTk
import tkinter as Tk


# inherits from CTK's frame class and calls that constructor
class View(CTk.CTkFrame):
    def __init__(self, root, master, **kwargs):
        super().__init__(master, fg_color="gray22", **kwargs)
        CTk.set_appearance_mode("dark")

        # labels for each widget
        left_servo_angle = CTk.CTkLabel(master=root, text="Left Thruster Angle (°)", fg_color="gray22", anchor="w")
        left_thruster_force = CTk.CTkLabel(master=root, text="Left Thruster RPM", fg_color="gray22", anchor="w")
        right_servo_angle = CTk.CTkLabel(master=root, text="Right Thruster Angle (°)", fg_color="gray22", anchor="w")
        right_thruster_force = CTk.CTkLabel(master=root, text="Right Thruster RPM", fg_color="gray22", anchor="w")
        tail_servo_angle = CTk.CTkLabel(master=root, text="Tail Thruster Angle (°)", fg_color="gray22", anchor="w")
        tail_thruster_force = CTk.CTkLabel(master=root, text="Tail Thruster RPM", fg_color="gray22", anchor="w")
        motor_status_label = CTk.CTkLabel(master=root, text="Motor Status", fg_color="gray22", anchor="w")
        flight_mode_label = CTk.CTkLabel(master=root, text="Flight Mode", fg_color="gray22", anchor="w")

        # slider widgets
        left_servo_slider = CTk.CTkSlider(master=root, from_=90, to=-90, orientation="vertical")
        left_thruster_slider = CTk.CTkSlider(master=root, from_=28, to=-28, orientation="vertical")
        right_servo_slider = CTk.CTkSlider(master=root, from_=90, to=-90, orientation="vertical")
        right_thruster_slider = CTk.CTkSlider(master=root, from_=28, to=-28, orientation="vertical")
        tail_servo_slider = CTk.CTkSlider(master=root, from_=90, to=-90, orientation="vertical")
        tail_thruster_slider = CTk.CTkSlider(master=root, from_=28, to=-28, orientation="vertical")

        # combo box widgets
        motor_status = CTk.CTkOptionMenu(master=root, values=["Disarmed", "Armed"])
        flight_mode = CTk.CTkOptionMenu(master=root,
                                        values=["Manual", "Stabilize", "Acro", "Altitude Hold", "Auto", "Guided",
                                                "Circle", "Surface", "Poshold"])

        # widget and label placements within frame

        motor_status_label.grid(column=0, row=0)
        motor_status.grid(column=0, row=1)
        flight_mode_label.grid(column=1, row=0)
        flight_mode.grid(column=1, row=1)

        left_servo_angle.grid(column=2, row=0, pady=10)
        left_servo_slider.grid(column=2, row=1)
        left_thruster_force.grid(column=3, row=0, padx=10)
        left_thruster_slider.grid(column=3, row=1, padx=10)

        right_servo_angle.grid(column=2, row=4)
        right_servo_slider.grid(column=2, row=5)
        right_thruster_force.grid(column=3, row=4, padx=10)
        right_thruster_slider.grid(column=3, row=5, padx=10)

        tail_servo_angle.grid(column=2, row=6)
        tail_servo_slider.grid(column=2, row=7)
        tail_thruster_force.grid(column=3, row=6, padx=10)
        tail_thruster_slider.grid(column=3, row=7, padx=10)

        # example of setting value of slider:
        val = 15
        left_servo_slider.set(val)
