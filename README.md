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

## Control Code Logic
Three python files are necessary

## HyCYCLE Data Analysis
