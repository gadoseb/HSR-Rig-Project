# HyCYCLE-Project
This repository contains all the workflow performed in the development of a hydrogen storage testing rig, from the PID, to the reactor rig control and its data analysis according to the specific parameters of the experiments.

## Rig and Reactor Purposes
A small Hydrogen Storage Reactor (HSR) to rapidly ‘cycle’ between absorption and desorption, to study the effect of the cycling condtions on the storage material (metal hydride) and its lifetime. The additional vacuum pump is implemented to further push the activation of certain class of materials.

## Hydrogen Storage Reaction with Metal Hydrides
Hydrogen storage using metal hydrides involves the reversible chemical reaction between hydrogen gas (H₂) and a metal or alloy to form a metal hydride (MHₓ). This process can be represented by the equation:
<p align="center">
  <img src="Supporting_Pics_HyCYCLE/MH_StorageReaction.png" width="400">
</p>
Key parameters influencing this reaction include:

- Temperature: The absorption and desorption of hydrogen by the metal hydride are temperature-dependent. Higher temperatures typically favor desorption, while lower temperatures favor absorption.

- Pressure: Hydrogen storage capacity and kinetics are also influenced by the hydrogen gas pressure. Higher pressures generally enhance hydrogen uptake.

- Thermodynamics: Enthalpy and entropy changes during the reaction determine the equilibrium conditions.

- Kinetics: The reaction rates for hydrogen absorption and desorption depend on the metal's properties and surface characteristics.

- Material Properties: The choice of metal or alloy affects storage capacity, reversibility, and cycling stability. 

## PID and Rig Building
The rig was built with the use of 4 solenoid valves (SV) and a mass flow controller (MFC) to allow a flow of hydrogen from a main gas line to the reactor and from the reactor to an outlet. The basics function and the OpModes are described in details in the attached PID. The additional vacuum pump is connected through a manual three-way valve system (BV1). To monitor the pressure during operations, a digital pressure transducer has been installed (PT). Additional levels of safety operations were implemented with the installation of a manual venting and manual vacuum operations which were controlled by shut off valves or ball valves (BV). The PID's right hand side shows the heating management system with a cooling fan (for exothermic operations) and heater (for endothermic operations).
<p align="center">
  <img src="Supporting_Pics_HyCYCLE/HyCycle_Rig_P&ID_v3-Copy of V6.drawio.png" width="800">
  <img src="Supporting_Pics_HyCYCLE/IMG_2079.jpg" width="600">
</p>

# Control Code
Three python files are necessary (they can be found in the folder:

1. bronkhorst.py
2. ISAK2.py
3. SmallReactor_Main.py

## 1. bronkhorst.py Documentation
This code is a Python driver for Bronkhorst flow controllers, which are devices used to control and measure gas flow. The code includes a class Bronkhorst that provides methods to communicate with the device via a serial port, send commands, and read various parameters such as setpoint, flow, and device information.

**1. Import Statements:**

- Imports necessary libraries such as time, sys, and serial.

- The from __future__ import print_function ensures compatibility between Python 2 and Python 3 for the print function.

**2. Class Definition (Bronkhorst):**

- Initialization (__init__ method): Initializes the serial connection to the flow controller and verifies the connection.

- Communication Method (comm method): Sends a command to the device and receives the reply.

- Read Setpoint (read_setpoint method): Reads the current setpoint value from the device.

- Read Flow (read_flow method): Reads the actual flow value from the device.

- Set Flow (set_flow method): Sets a desired flow setpoint on the device.

- Read Counter Value (read_counter_value method): Reads the valve counter value (not fully implemented).

- Set Control Mode (set_control_mode method): Sets the control mode to accept RS232 setpoints.

- Read Serial (read_serial method): Reads the serial number of the device.

- Read Unit (read_unit method): Reads the flow unit from the device.

- Read Capacity (read_capacity method): Reads the capacity from the device (the exact meaning is unclear).

If the script is run directly, it creates an instance of the Bronkhorst class and calls various methods to interact with the device.

## 2. ISAK2.py Documentation

## 3. SmallReactor_Main.py Documentation

# Data Analysis Code
