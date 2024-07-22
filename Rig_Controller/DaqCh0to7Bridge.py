import nidaqmx
from nidaqmx import constants
from datetime import timedelta, datetime
import time
import paho.mqtt.client as mqtt
import atexit


# InitialStrainValueMod1Ch0 = -0.00015428
# InitialStrainValueMod1Ch1 = 0.00026183
# InitialStrainValueMod1Ch2 = -0.00041022
# InitialStrainValueMod1Ch3 = 0.00019359
# InitialStrainValueMod1Ch4 = 0.0010673
# InitialStrainValueMod1Ch5 = 0.00048554
# InitialStrainValueMod1Ch6 = 0.0024156
# InitialStrainValueMod1Ch7 = 0.0024035


InitialStrainValueMod1Ch0 = 0.000032218      
InitialStrainValueMod1Ch2 = 0.00089598       
InitialStrainValueMod1Ch3 = 0.001003         
InitialStrainValueMod1Ch4 = -0.008548        
InitialStrainValueMod1Ch5 = 0.00077476       
InitialStrainValueMod1Ch6 = 0.0012565        
InitialStrainValueMod1Ch7 = 0.0064892        



#Previous beta2 zero values from IHub
#InitialStrainValueMod1Ch2 = 0.001647        #HSRb2 - Strain 1
#InitialStrainValueMod1Ch3 = 0.0013664       #HSRb2 - Strain 2
#InitialStrainValueMod1Ch4 = 0.0018860       #HSRb2 - Strain 3
#InitialStrainValueMod1Ch5 = 0.0016572       #HSRb2 - Strain 4
#InitialStrainValueMod1Ch6 = 0.0018082       #HSRb2 - Strain 5
#InitialStrainValueMod1Ch7 = 0.0015998       #HSRb2 - Strain 6
#
#InitialStrainValueMod2Ch0 = 0.0010798       #HSRb2 - Strain 7
#InitialStrainValueMod2Ch1 = 0.0014655       #HSRb2 - Strain 8
#InitialStrainValueMod2Ch2 = 0.0016788       #HSRb2 - Strain 9

InitialStrainValueMod2Ch3 = 0
InitialStrainValueMod2Ch4 = 0
InitialStrainValueMod2Ch5 = 0
InitialStrainValueMod2Ch6 = 0

#Beta2 is from 2-7, 3-0 to 3-7
#New beta2 zero values after moving to SS
InitialStrainValueMod3Ch0 = 0.001647            #HSRb2 - Strain 1
InitialStrainValueMod3Ch1 = 0.0013664           #HSRb2 - Strain 2
InitialStrainValueMod3Ch2 = 0.0018860           #HSRb2 - Strain 3
InitialStrainValueMod3Ch3 = 0.0016572           #HSRb2 - Strain 4
InitialStrainValueMod3Ch4 = 0.0018082           #HSRb2 - Strain 5
InitialStrainValueMod3Ch5 = 0.0015998           #HSRb2 - Strain 6
InitialStrainValueMod3Ch6 = 0.0010798           #HSRb2 - Strain 7
InitialStrainValueMod3Ch7 = 0.0014655           #HSRb2 - Strain 8



#26-1-24 - New strain gauge values for HyNTS reactor, overwrite previous values
InitialStrainValueMod1Ch0 = 0.00043154
InitialStrainValueMod1Ch1 = -0.00071772

#8-2-24 - New strain gauge values for HyNTS SR3, overwrite previous values
                        
InitialStrainValueMod1Ch2 = -0.00067642
InitialStrainValueMod1Ch3 = 0.0012396
InitialStrainValueMod1Ch4 = -0.000090391
InitialStrainValueMod1Ch5 = 0.000054855

#7-3-24 New hynts SR4
InitialStrainValueMod1Ch6 = -0.00048184
InitialStrainValueMod1Ch7 = -0.00014297
InitialStrainValueMod2Ch6 = -0.00040027
InitialStrainValueMod2Ch5 = -0.00046881



#UPDATED HSRB3 STRAIN HYNTS 14/03/2024 14:50
#InitialStrainValueMod1Ch1 = 0.0011951        #HyNTS LR - Strain 1 SG1
#InitialStrainValueMod2Ch0 = 0.0010165        #HyNTS LR - Strain 2 SG2
#InitialStrainValueMod2Ch1 = 0.0003941467     #HyNTS LR - Strain 3 SG3
#InitialStrainValueMod2Ch2 = 0.0005038133     #HyNTS LR - Strain 4 SG4
#InitialStrainValueMod2Ch3 = 0.0003191667     #HyNTS LR - Strain 5 SG5
#InitialStrainValueMod2Ch4 = 0.0011981        #HyNTS LR - Strain 6 SG6
#InitialStrainValueMod2Ch7 = 0.0015048        #HyNTS LR - Strain 7 SG7
#InitialStrainValueMod3Ch0 = 0.0018114        #HyNTS LR - Strain 8 SG8
#InitialStrainValueMod3Ch1 = 0.0002880833     #HyNTS LR - Strain 9 SG9
#InitialStrainValueMod3Ch2 = 0.0007931000     #HyNTS LR - Strain 10 SG10
#InitialStrainValueMod3Ch3 = 0.0006789433     #HyNTS LR - Strain 11 SG11
#InitialStrainValueMod3Ch4 = 0.0013065        #HyNTS LR - Strain 12 SG12

#21-3-24 Updated zeros strain - HyJACK
#InitialStrainValueMod1Ch1 = 0.00089598      #HyJACK - Strain 1 SG1
#InitialStrainValueMod2Ch0 = 0.001003       #HyJACK - Strain 2 SG2
#InitialStrainValueMod2Ch1 = -0.008548         #HyJACK - Strain 3 SG3
#InitialStrainValueMod2Ch2 = 0.00077476        #HyJACK - Strain 4 SG4
#InitialStrainValueMod2Ch3 = 0.0012565       #HyJACK - Strain 5 SG5
#InitialStrainValueMod2Ch4 = 0.0064892        #HyJACK - Strain 6 SG6
#InitialStrainValueMod2Ch7 = 0.0012831        #HyJACK - Strain 7 SG7
#InitialStrainValueMod3Ch0 = 0.00086649       #HyJACK - Strain 8 SG8
#InitialStrainValueMod3Ch1 = 0.0013059        #HyJACK - Strain 9 SG9

#21-3-24 Updated zeros strain - HyJACK
InitialStrainValueMod1Ch1 = 0.0029325        #Beta4 - Strain 1  SG13
InitialStrainValueMod2Ch0 = 0.0012952        #Beta4 - Strain 2  SG14
InitialStrainValueMod2Ch1 = 0.0010645        #Beta4 - Strain 3  SG15
InitialStrainValueMod2Ch2 = 0.0006679        #Beta4 - Strain 4  SG16
InitialStrainValueMod2Ch3 = 0.0005426        #Beta4 - Strain 5  SG17
InitialStrainValueMod2Ch4 = 0.0018823        #Beta4 - Strain 6  SG18
InitialStrainValueMod2Ch7 = 0.0016281        #Beta4 - Strain 7  SG19
InitialStrainValueMod3Ch0 = 0.0005406        #Beta4 - Strain 8  SG20
InitialStrainValueMod3Ch1 = 0.0004835        #Beta4 - Strain 9  SG21
InitialStrainValueMod3Ch2 = 0.0011588        #Beta4 - Strain 10 SG22
InitialStrainValueMod3Ch3 = 0.0008410        #Beta4 - Strain 11 SG23
InitialStrainValueMod3Ch4 = 0.0017070        #Beta4 - Strain 12 SG24


PRINTEXCEPTIONS = False                         
tstart = time.time()


def MqttOnConnect(client, userdata, flags, rc):
    MqttClient.subscribe("DAQ/#")

def MqttOnMessage(client, userdata, msg):
    pass

def ChannelCloseHandling():
    Mod1Task0.close()
    Mod1Task1.close()
    Mod1Task2.close()
    Mod1Task3.close()
    Mod1Task4.close()
    Mod1Task5.close()
    Mod1Task6.close()
    Mod1Task7.close()

    Mod2Task0.close()
    Mod2Task1.close()
    Mod2Task2.close()
    Mod2Task3.close()
    Mod2Task4.close()
    Mod2Task5.close()
    Mod2Task6.close()
    Mod2Task7.close()

    Mod3Task0.close()
    Mod3Task1.close()
    Mod3Task2.close()
    Mod3Task3.close()
    Mod3Task4.close()
    Mod3Task5.close()
    Mod3Task6.close()
    Mod3Task7.close()

def ReadAndPublishAndPrintStrains():
    try:
        Mod1Ch0Strain = Mod1Task0.read(timeout=0.05)
        Mod1Task0.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch0Strain = '0xFF'
    try:
        Mod1Ch1Strain = Mod1Task1.read(timeout=0.05)
        Mod1Task1.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch1Strain = '0xFF'
    try:
        Mod1Ch2Strain = Mod1Task2.read(timeout=0.05)
        Mod1Task2.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch2Strain = '0xFF'
    try:
        Mod1Ch3Strain = Mod1Task3.read(timeout=0.05)
        Mod1Task3.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch3Strain = '0xFF'
    try:
        Mod1Ch4Strain = Mod1Task4.read(timeout=0.05)
        Mod1Task4.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch4Strain = '0xFF'
    try:
        Mod1Ch5Strain = Mod1Task5.read(timeout=0.05)
        Mod1Task5.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch5Strain = '0xFF'
    try:
        Mod1Ch6Strain = Mod1Task6.read(timeout=0.05)
        Mod1Task6.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch6Strain = '0xFF'
    try:
        Mod1Ch7Strain = Mod1Task7.read(timeout=0.05)
        Mod1Task7.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod1Ch7Strain = '0xFF'


    try:
        Mod2Ch0Strain = Mod2Task0.read(timeout=0.05)
        Mod2Task0.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch0Strain = '0xFF'
    try:
        Mod2Ch1Strain = Mod2Task1.read(timeout=0.05)
        Mod2Task1.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch1Strain = '0xFF'
    try:
        Mod2Ch2Strain = Mod2Task2.read(timeout=0.05)
        Mod2Task2.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch2Strain = '0xFF'
    try:
        Mod2Ch3Strain = Mod2Task3.read(timeout=0.05)
        Mod2Task3.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch3Strain = '0xFF'
    try:
        Mod2Ch4Strain = Mod2Task4.read(timeout=0.05)
        Mod2Task4.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch4Strain = '0xFF'
    try:
        Mod2Ch5Strain = Mod2Task5.read(timeout=0.05)
        Mod2Task5.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch5Strain = '0xFF'
    try:
        Mod2Ch6Strain = Mod2Task6.read(timeout=0.05)
        Mod2Task6.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch6Strain = '0xFF'
    try:
        Mod2Ch7Strain = Mod2Task7.read(timeout=0.05)
        Mod2Task7.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod2Ch7Strain = '0xFF'


    try:
        Mod3Ch0Strain = Mod3Task0.read(timeout=0.05)
        Mod3Task0.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch0Strain = '0xFF'
    try:
        Mod3Ch1Strain = Mod3Task1.read(timeout=0.05)
        Mod3Task1.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch1Strain = '0xFF'
    try:
        Mod3Ch2Strain = Mod3Task2.read(timeout=0.05)
        Mod3Task2.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch2Strain = '0xFF'
    try:
        Mod3Ch3Strain = Mod3Task3.read(timeout=0.05)
        Mod3Task3.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch3Strain = '0xFF'
    try:
        Mod3Ch4Strain = Mod3Task4.read(timeout=0.05)
        Mod3Task4.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch4Strain = '0xFF'
    try:
        Mod3Ch5Strain = Mod3Task5.read(timeout=0.05)
        Mod3Task5.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch5Strain = '0xFF'
    try:
        Mod3Ch6Strain = Mod3Task6.read(timeout=0.05)
        Mod3Task6.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch6Strain = '0xFF'
    try:
        Mod3Ch7Strain = Mod3Task7.read(timeout=0.05)
        Mod3Task7.stop()
    except Exception as e:
        if(PRINTEXCEPTIONS): print(e)
        Mod3Ch7Strain = '0xFF'

    MqttClient.publish("DAQ/m1ai0", Mod1Ch0Strain)
    MqttClient.publish("DAQ/m1ai1", Mod1Ch1Strain)
    MqttClient.publish("DAQ/m1ai2", Mod1Ch2Strain)
    MqttClient.publish("DAQ/m1ai3", Mod1Ch3Strain)
    MqttClient.publish("DAQ/m1ai4", Mod1Ch4Strain)
    MqttClient.publish("DAQ/m1ai5", Mod1Ch5Strain)
    MqttClient.publish("DAQ/m1ai6", Mod1Ch6Strain)
    MqttClient.publish("DAQ/m1ai7", Mod1Ch7Strain)
    MqttClient.publish("DAQ/m2ai0", Mod2Ch0Strain)
    MqttClient.publish("DAQ/m2ai1", Mod2Ch1Strain)
    MqttClient.publish("DAQ/m2ai2", Mod2Ch2Strain)
    MqttClient.publish("DAQ/m2ai3", Mod2Ch3Strain)
    MqttClient.publish("DAQ/m2ai4", Mod2Ch4Strain)
    MqttClient.publish("DAQ/m2ai5", Mod2Ch5Strain)
    MqttClient.publish("DAQ/m2ai6", Mod2Ch6Strain)
    MqttClient.publish("DAQ/m2ai7", Mod2Ch7Strain)
    MqttClient.publish("DAQ/m3ai0", Mod3Ch0Strain)
    MqttClient.publish("DAQ/m3ai1", Mod3Ch1Strain)
    MqttClient.publish("DAQ/m3ai2", Mod3Ch2Strain)
    MqttClient.publish("DAQ/m3ai3", Mod3Ch3Strain)
    MqttClient.publish("DAQ/m3ai4", Mod3Ch4Strain)
    MqttClient.publish("DAQ/m3ai5", Mod3Ch5Strain)
    MqttClient.publish("DAQ/m3ai6", Mod3Ch6Strain)
    MqttClient.publish("DAQ/m3ai7", Mod3Ch7Strain)
    
    #CliString = "Time: {:n}s ".format(time.time()-tstart) + "m1ai0: " + str(Mod1Ch0Strain) + "Strain, m1ai1: " + str(Mod1Ch1Strain) + "Strain, m1ai2: " + str(Mod1Ch2Strain) + "Strain, m1ai3: " + str(Mod1Ch3Strain) + "Strain, m1ai4: " + str(Mod1Ch4Strain) + "Strain, m1ai5: " + str(Mod1Ch5Strain) + "Strain, m1ai6: " + str(Mod1Ch6Strain) + "Strain, m1ai7: " + str(Mod1Ch7Strain) + "Strain, m2ai0: " + str(Mod1Ch0Strain) + "Strain, m2ai1: " + str(Mod1Ch1Strain) + "Strain, m2ai2: " + str(Mod1Ch2Strain) + "Strain, m2ai3: " + str(Mod1Ch3Strain) + "Strain, m2ai4: " + str(Mod1Ch4Strain) + "Strain, m2ai5: " + str(Mod1Ch5Strain) + "Strain, m2ai6: " + str(Mod1Ch6Strain) + "Strain, m2ai7: " + str(Mod1Ch7Strain) + "Strain, m3ai0: " + str(Mod1Ch0Strain) + "Strain, m3ai1: " + str(Mod1Ch1Strain) + "Strain, m3ai2: " + str(Mod1Ch2Strain) + "Strain, m3ai3: " + str(Mod1Ch3Strain) + "Strain, m3ai4: " + str(Mod1Ch4Strain) + "Strain, m3ai5: " + str(Mod1Ch5Strain) + "Strain, m3ai6: " + str(Mod1Ch6Strain) + "Strain, m3ai7: " + str(Mod1Ch7Strain)+"\n"# + "Strain"
    try:
        CliString = "Time: {}, m1ai0: {:.3e}, m1ai1: {:.3e}, m1ai2: {:.3e}, m1ai3: {:.3e}, m1ai4: {:.3e}, m1ai5: {:.3e}, m1ai6: {:.3e}, m1ai7: {:.3e}, m2ai0: {:.3e}, m2ai1: {:.3e}, m2ai2: {:.3e}, m2ai3: {:.3e}, m2ai4: {:.3e}, m2ai5: {:.3e}, m2ai6: {:.3e}, m2ai7: {:.3e}, m3ai0: {:.3e}, m3ai1: {:.3e}, m3ai2: {:.3e}, m3ai3: {:.3e}, m3ai4: {:.3e}, m3ai5: {:.3e}, m3ai6: {:.3e}, m3ai7: {:.3e}\n\n\n".format(
            datetime.now(), 
            Mod1Ch0Strain, Mod1Ch1Strain, Mod1Ch2Strain, Mod1Ch3Strain,
            Mod1Ch4Strain, Mod1Ch5Strain, Mod1Ch6Strain, Mod1Ch7Strain,
            Mod2Ch0Strain, Mod2Ch1Strain, Mod2Ch2Strain, Mod2Ch3Strain,
            Mod2Ch4Strain, Mod2Ch5Strain, Mod2Ch6Strain, Mod2Ch7Strain,
            Mod3Ch0Strain, Mod3Ch1Strain, Mod3Ch2Strain, Mod3Ch3Strain,
            Mod3Ch4Strain, Mod3Ch5Strain, Mod3Ch6Strain, Mod3Ch7Strain,
        )
    except Exception as e:
        CliString = "Strain not as a string! Continuing..."
        #Print debug
        CliString += "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},".format(
            Mod1Ch0Strain, Mod1Ch1Strain, Mod1Ch2Strain, Mod1Ch3Strain,
            Mod1Ch4Strain, Mod1Ch5Strain, Mod1Ch6Strain, Mod1Ch7Strain,
            Mod2Ch0Strain, Mod2Ch1Strain, Mod2Ch2Strain, Mod2Ch3Strain,
            Mod2Ch4Strain, Mod2Ch5Strain, Mod2Ch6Strain, Mod2Ch7Strain,
            Mod3Ch0Strain, Mod3Ch1Strain, Mod3Ch2Strain, Mod3Ch3Strain,
            Mod3Ch4Strain, Mod3Ch5Strain, Mod3Ch6Strain, Mod3Ch7Strain,
        )
    # CliString = "ai0: " + str(Mod1Ch0Strain)
    print(CliString.strip())

atexit.register(ChannelCloseHandling)

MqttClient = mqtt.Client()
MqttClient.on_connect = MqttOnConnect
MqttClient.on_message = MqttOnMessage
MqttClient.connect("localhost", 1883, 60)

print("H2GO Power (C)")
print("NI DAQ Strain Module 1 - 3 (ai0 - ai7) Bridge")
print("Deployed 28/06/2022 - M CHANA")
print("Modified 05/07/2022 - H Shallcross\n\n")
print("Modified 14/03/2024 - A Keshvari\n\n")

#Also this is where the double press enter comes from, you can see that there is only 1 input so double press isn't required lol
input("Please ensure DAQexpres is closed and hit quickly double press the Enter key to start DAQ bridge for RRC2 instances")

Mod1Task0 = nidaqmx.Task()
Mod1Task1 = nidaqmx.Task()
Mod1Task2 = nidaqmx.Task()
Mod1Task3 = nidaqmx.Task()
Mod1Task4 = nidaqmx.Task()
Mod1Task5 = nidaqmx.Task()
Mod1Task6 = nidaqmx.Task()
Mod1Task7 = nidaqmx.Task()
Mod2Task0 = nidaqmx.Task()
Mod2Task1 = nidaqmx.Task()
Mod2Task2 = nidaqmx.Task()
Mod2Task3 = nidaqmx.Task()
Mod2Task4 = nidaqmx.Task()
Mod2Task5 = nidaqmx.Task()
Mod2Task6 = nidaqmx.Task()
Mod2Task7 = nidaqmx.Task()
Mod3Task0 = nidaqmx.Task()
Mod3Task1 = nidaqmx.Task()
Mod3Task2 = nidaqmx.Task()
Mod3Task3 = nidaqmx.Task()
Mod3Task4 = nidaqmx.Task()
Mod3Task5 = nidaqmx.Task()
Mod3Task6 = nidaqmx.Task()
Mod3Task7 = nidaqmx.Task()
#19-3-24 HS - Updated strain gauge factors and poisson ratios for HyNTS
Mod1Task0.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai0", "Strain0", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod1Ch0, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task1.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai1", "Strain1", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod1Ch1, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task2.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai2", "Strain2", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod1Ch2, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task3.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai3", "Strain3", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod1Ch3, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task4.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai4", "Strain4", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod1Ch4, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task5.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai5", "Strain5", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod1Ch5, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task6.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai6", "Strain6", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod1Ch6, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task7.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod1/ai7", "Strain7", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod1Ch7, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task0.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai0", "Strain0", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod2Ch0, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task1.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai1", "Strain1", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod2Ch1, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task2.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai2", "Strain2", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod2Ch2, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task3.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai3", "Strain3", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod2Ch3, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task4.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai4", "Strain4", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod2Ch4, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task5.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai5", "Strain5", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.095, initial_bridge_voltage=InitialStrainValueMod2Ch5, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task6.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai6", "Strain6", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod2Ch6, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod2Task7.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod2/ai7", "Strain7", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod2Ch7, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task0.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai0", "Strain0", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod3Ch0, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task1.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai1", "Strain1", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod3Ch1, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task2.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai2", "Strain2", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod3Ch2, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task3.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai3", "Strain3", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod3Ch3, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task4.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai4", "Strain4", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.07, initial_bridge_voltage=InitialStrainValueMod3Ch4, nominal_gage_resistance=350.0, poisson_ratio=0.25, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task5.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai5", "Strain5", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.14, initial_bridge_voltage=InitialStrainValueMod3Ch5, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task6.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai6", "Strain6", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.14, initial_bridge_voltage=InitialStrainValueMod3Ch6, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod3Task7.ai_channels.add_ai_strain_gage_chan("cDAQ1Mod3/ai7", "Strain7", -0.005, 0.005, constants.StrainUnits.STRAIN, strain_config=constants.StrainGageBridgeType.QUARTER_BRIDGE_I, voltage_excit_source=constants.ExcitationSource.INTERNAL, voltage_excit_val=3.3, gage_factor=2.14, initial_bridge_voltage=InitialStrainValueMod3Ch7, nominal_gage_resistance=350.0, poisson_ratio=0.27, lead_wire_resistance=0.0, custom_scale_name="")
Mod1Task0.timing.samp_clk_rate = 800
Mod1Task0.timing.samp_quant_samp_per_chan = 500
Mod1Task1.timing.samp_clk_rate = 800
Mod1Task1.timing.samp_quant_samp_per_chan = 500
Mod1Task2.timing.samp_clk_rate = 800
Mod1Task2.timing.samp_quant_samp_per_chan = 500
Mod1Task3.timing.samp_clk_rate = 800
Mod1Task3.timing.samp_quant_samp_per_chan = 500
Mod1Task4.timing.samp_clk_rate = 800
Mod1Task4.timing.samp_quant_samp_per_chan = 500
Mod1Task5.timing.samp_clk_rate = 800
Mod1Task5.timing.samp_quant_samp_per_chan = 500
Mod1Task6.timing.samp_clk_rate = 800
Mod1Task6.timing.samp_quant_samp_per_chan = 500
Mod1Task7.timing.samp_clk_rate = 800
Mod1Task7.timing.samp_quant_samp_per_chan = 500
Mod2Task0.timing.samp_clk_rate = 800
Mod2Task0.timing.samp_quant_samp_per_chan = 500
Mod2Task1.timing.samp_clk_rate = 800
Mod2Task1.timing.samp_quant_samp_per_chan = 500
Mod2Task2.timing.samp_clk_rate = 800
Mod2Task2.timing.samp_quant_samp_per_chan = 500
Mod2Task3.timing.samp_clk_rate = 800
Mod2Task3.timing.samp_quant_samp_per_chan = 500
Mod2Task4.timing.samp_clk_rate = 800
Mod2Task4.timing.samp_quant_samp_per_chan = 500
Mod2Task5.timing.samp_clk_rate = 800
Mod2Task5.timing.samp_quant_samp_per_chan = 500
Mod2Task6.timing.samp_clk_rate = 800
Mod2Task6.timing.samp_quant_samp_per_chan = 500
Mod2Task7.timing.samp_clk_rate = 800
Mod2Task7.timing.samp_quant_samp_per_chan = 500
Mod3Task0.timing.samp_clk_rate = 800
Mod3Task0.timing.samp_quant_samp_per_chan = 500
Mod3Task1.timing.samp_clk_rate = 800
Mod3Task1.timing.samp_quant_samp_per_chan = 500
Mod3Task2.timing.samp_clk_rate = 800
Mod3Task2.timing.samp_quant_samp_per_chan = 500
Mod3Task3.timing.samp_clk_rate = 800
Mod3Task3.timing.samp_quant_samp_per_chan = 500
Mod3Task4.timing.samp_clk_rate = 800
Mod3Task4.timing.samp_quant_samp_per_chan = 500
Mod3Task5.timing.samp_clk_rate = 800
Mod3Task5.timing.samp_quant_samp_per_chan = 500
Mod3Task6.timing.samp_clk_rate = 800
Mod3Task6.timing.samp_quant_samp_per_chan = 500
Mod3Task7.timing.samp_clk_rate = 800
Mod3Task7.timing.samp_quant_samp_per_chan = 500

time.sleep(1)

while(1):
    try:
        ReadAndPublishAndPrintStrains()
    except KeyboardInterrupt:
        print("Closing program...")
        break