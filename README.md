# Unmanned Underwater Vehicle Control System

**Table of Contents**
1. [Product Name](#product-name)
2. [Project Overview](#project-overview)
3. [Main Product Elements](#main-product-elements)
4. [Vehicle Features](#vehicle-features)
5. [Technical Specifications](#technical-specifications)
6. [User Interface](#user-interface)
7. [Safety Warnings](#safety-warnings)
8. [Installation Instructions](#installation-instructions)
9. [Software Operation](#software-operation)
10. [Maintenance Information](#maintenance-information)
11. [Glossary](#glossary)

## 1. Product Name
Unmanned Underwater Robot (Version 3)

## 2. Intended Use
This research project involves designing and implementing a software/hardware integration to provide underwater drone control for Unmanned Vehicles Robotarium research lab. Our team successfully integrated various electronic components and developed software to control the underwater drone. We had developed a GUI using Python that is capable of communicating with a Raspberry Pi and PX4 flight controller to send commands and read movement data. The project consists of a custom GUI, a Raspberry Pi 3 Model B, Pixhawk 4 autopilot, a drone prototype, and a list of other various electronic components. The project’s main objective is deploying and navigating the drone prototype within confined underwater spaces.

## 3. Main Product Elements
- Right Thruster
- Right Thruster Servo Motor
- Right Camera
- Right Gripper Arm
- Left Camera
- Left Gripper Arm
- Left Thruster
- Left Thruster Servo Motor
- Rear Thruster
- Rear Thruster Servo Motor

## 4. Vehicle Features
- Three thrusters for movement and maneuverability
- Three servo motors for each thruster, providing 6 degrees of freedom
- Two grippers with open and close states
- Two front-facing cameras
- GPS tracking system

## 5. Technical Specifications
| Component                   | Rating                             |
| --------------------------- | ---------------------------------- |
| Seabotix Thruster           | 110W Max, 80W Continuous           |
| Hitec HS422 Servo Motor     | 5W (4.8-6V, 0.8A)                  |
| Subsea Gripper              | 108W                               |
| Pixhawk 4                   | 12.5W USB Supply                   |
| Pololu Motor Controller     | 15W                                |
| HolyBro PM07-V21 Board      | 45W                                |
| Raspberry Pi 3B             | 12.5W USB Supply                   |
| BlueRobotics LiPo Battery   | 14.8V, 15.6Ah                      |

## 6. User Interface
The user interface has seven sections:
- Thruster angle sliders
- Thruster RPM sliders
- Open/close gripper sliders
- Reset State button
- Command Mode dropdown
- Send Commands button
- IMU data display (acceleration and angular speed in x, y, and z directions)


## 7. Safety Warnings
- General Safety Guides
- Battery Safety Guides
- Gripper Safety Guides
- Thrusters Safety Guides

## 8. Installation Instructions
See the pin diagram for HMAUV connections and installation.

## 9. Software Operation
- Python 3.8 is required on GCS.
- Required packages: customtkinter, numpy, Pillow.
- RPi requires pymavlink, smc (currently inoperable), MAVProxy.

## 10. Maintenance Information
### 10.1 Charging the battery
- Blue Robotics H6 PRO Lithium Battery Charger recommended.
- Lithium-ion Battery (14.8V, 15.6 Ah) charging settings provided.

### 10.2 Discharging the battery
- Connect XT90S discharge plug to the vehicle.
- Monitor battery voltage to prevent over-discharging.

## 11. Glossary
- ESC: Electronic Speed Control
- FXTI: Fathom X Tether Interface
- GUI: Graphical User Interface
- HMAUV: Highly Maneuverable Autonomous Underwater Vehicle
- IO: Input/Output
- LiPo: Lithium-Ion Polymer Battery
- MVC: Model-View-Controller
- PCB: Printed Circuit Board
- PWM: Pulse-Width Modulation
- UI: User Interface
- RPi: Raspberry Pi 3B
- SSH: Secure Shell Protocol

## Installation Instructions
To learn more about the project, install the hardware, and run the software, please see our [User Manual.](./User%20Manual.pdf)


