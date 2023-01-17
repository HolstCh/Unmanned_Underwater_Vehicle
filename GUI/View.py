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
        left_servo_angle.grid(column=0, row=0)
        left_servo_slider.grid(column=0, row=1)
        left_thruster_force.grid(column=1, row=0, padx=10)
        left_thruster_slider.grid(column=1, row=1, padx=10)

        right_servo_angle.grid(column=0, row=2)
        right_servo_slider.grid(column=0, row=3)
        right_thruster_force.grid(column=1, row=2, padx=10)
        right_thruster_slider.grid(column=1, row=3, padx=10)

        tail_servo_angle.grid(column=0, row=4)
        tail_servo_slider.grid(column=0, row=5)
        tail_thruster_force.grid(column=1, row=4, padx=10)
        tail_thruster_slider.grid(column=1, row=5, padx=10)

        # example of setting value of slider:
        val = 15
        left_servo_slider.set(val)