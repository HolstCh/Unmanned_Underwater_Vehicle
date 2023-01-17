import tkinter as tk


class View(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # labels for each widget
        left_servo_angle = tk.Label(text="Left Thruster Angle (°)", anchor="w")
        left_thruster_force = tk.Label(text="Left Thruster Force (N)", anchor="w")
        right_servo_angle = tk.Label(text="Right Thruster Angle (°)", anchor="w")
        right_thruster_force = tk.Label(text="Right Thruster Force (N)", anchor="w")
        tail_servo_angle = tk.Label(text="Tail Thruster Angle (°)", anchor="w")
        tail_thruster_force = tk.Label(text="Tail Thruster Force (N)", anchor="w")

        # slider widgets
        left_servo_slider = tk.Scale(root, from_=90, to=-90, tickinterval=30)
        left_thruster_slider = tk.Scale(root, from_=28, to=-28, tickinterval=14)
        right_servo_slider = tk.Scale(root, from_=90, to=-90, tickinterval=30)
        right_thruster_slider = tk.Scale(root, from_=28, to=-28, tickinterval=14)
        tail_servo_slider = tk.Scale(root, from_=90, to=-90, tickinterval=30)
        tail_thruster_slider = tk.Scale(root, from_=28, to=-28, tickinterval=14)

        # widget and label placements within frame
        left_servo_angle.pack(side="left", fill="both", expand=True)
        left_servo_slider.pack(side="left", fill="both", expand=True)
        left_thruster_force.pack(side="left", fill="both", expand=True)
        left_thruster_slider.pack(side="left", fill="both", expand=True)

        right_servo_angle.pack(side="left", fill="both", expand=True)
        right_servo_slider.pack(side="left", fill="both", expand=True)
        right_thruster_force.pack(side="left", fill="both", expand=True)
        right_thruster_slider.pack(side="left", fill="both", expand=True)

        tail_servo_angle.pack(side="left", fill="both", expand=True)
        tail_servo_slider.pack(side="left", fill="both", expand=True)
        tail_thruster_force.pack(side="left", fill="both", expand=True)
        tail_thruster_slider.pack(side="left", fill="both", expand=True)

        # example of setting value of slider:
        val = 15
        left_servo_slider.set(val)