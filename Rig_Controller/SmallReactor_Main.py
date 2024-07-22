import nidaqmx
from nidaqmx import constants
import serial
import bronkhorst
import datetime
from datetime import timedelta
import time
import paho.mqtt.client as mqtt
import queue
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client import ModbusTcpClient as ModbusClient
import ISAK2
import warnings
warnings.filterwarnings("ignore")

#MbDevice = ModbusClient(host="192.168.1.222", port=502)
#
#try:
#    # ElecOutletPsi3 = ISAK2.EnapterEl20ModbusRx(MbDevice, 163, 32, 2.33e-07)
#    ElecOutletPsi3 = ISAK2.EnapterEl21ModbusRx(MbDevice, 7514, "float32")
#    GlobalGw_ElectrolyserOutletPressure =  ISAK2.CanTx32BitHexAssemble(ElecOutletPsi3)
#except Exception as e:
#    print("ElecOutletPsi3 " + str(e))
#    ElecOutletPsi3 = 0

# MQTT to get data from DAQ bridge
StrainCh9MqttSubscribeQueue = queue.Queue()
StrainCh10MqttSubscribeQueue = queue.Queue()

StrainM2AI3MqttSubscribeQueue = queue.Queue()
StrainM2AI4MqttSubscribeQueue = queue.Queue()

StrainM1AI2MqttSubscribeQueue = queue.Queue()
StrainM1AI3MqttSubscribeQueue = queue.Queue()
StrainM1AI4MqttSubscribeQueue = queue.Queue()
StrainM1AI5MqttSubscribeQueue = queue.Queue()

StrainM1AI6MqttSubscribeQueue = queue.Queue()
StrainM1AI7MqttSubscribeQueue = queue.Queue()
StrainM2AI6MqttSubscribeQueue = queue.Queue()
StrainM2AI5MqttSubscribeQueue = queue.Queue()

UPPER_LIMIT = 0.0003

def MapFunction(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((float(value) - istart) / (istop - istart))

def MqttOnConnect(client, userdata, flags, rc):
    MqttClient.subscribe("UI/#")
    MqttClient.subscribe("DAQ/#")

def MqttOnMessage(client, userdata, msg):
    global Ai0MqttSubscribeQueue
    global Ai1MqttSubscribeQueue

    if msg.topic == "DAQ/m1ai0":
        StrainCh9MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m1ai1":
        StrainCh10MqttSubscribeQueue.put(msg.payload.decode())
        
    #HS Add 26-1-24 for HyNTS
    if msg.topic == "DAQ/m2ai3":
        StrainM2AI3MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m2ai4":
        StrainM2AI4MqttSubscribeQueue.put(msg.payload.decode())
        
    #HS Add 8/2/24 for HyNTS SR3
    if msg.topic == "DAQ/m1ai2":
        StrainM1AI2MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m1ai3":
        StrainM1AI3MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m1ai4":
        StrainM1AI4MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m1ai5":
        StrainM1AI5MqttSubscribeQueue.put(msg.payload.decode())
        
    #HS Add 8/3/24 for HyNTS SR4
    if msg.topic == "DAQ/m1ai6":
        StrainM1AI6MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m1ai7":
        StrainM1AI7MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m2ai6":
        StrainM2AI6MqttSubscribeQueue.put(msg.payload.decode())
    if msg.topic == "DAQ/m2ai5":
        StrainM2AI5MqttSubscribeQueue.put(msg.payload.decode())

def StopAndTransitionMode(MfcComInstance, ArdComInstance):
    MfcComInstance.set_flow(0)
    time.sleep(1)
    ArdComInstance.write("S".encode())
    time.sleep(1)

StrainCh9Value= 0
StrainCh10Value = 0
StrainM2AI3Value= 0 
StrainM2AI4Value = 0
StrainM1AI2Value= 0 
StrainM1AI3Value= 0 
StrainM1AI4Value= 0 
StrainM1AI5Value= 0 
StrainM1AI6Value= 0 
StrainM1AI7Value= 0 
StrainM2AI6Value= 0 
StrainM2AI5Value = 0
    
def SampleAndPrint():

    global H2FlowRate
    global H2FlowRatePrev
    global H2TransferredInLitres
    global H2TransferredInLitresPrev
    global H2FlowDelta
    global H2RxTimestampPrev
    global H2RxTimestampDelta
    global H2RxTimestampDeltaSecs
    global H2TransferredInLitresTotal
    global StrainM2AI3Value
    global StrainM2AI4Value
    global StrainM1AI2Value
    global StrainM1AI3Value
    global StrainM1AI4Value
    global StrainM1AI5Value
    global StrainM1AI6Value
    global StrainM1AI7Value
    global StrainM2AI6Value
    global StrainM2AI5Value
    global StrainCh9Value
    global StrainCh10Value

    Timestamp = datetime.datetime.now()

    # Step 1: Store the values from the DAQ bridge, if no values insert the string 0x0F

    if not StrainCh9MqttSubscribeQueue.empty():
        StrainCh9Value = StrainCh9MqttSubscribeQueue.get()
    else:
        StrainCh9Value = "0x0F"
    if StrainCh9Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainCh9Value", StrainCh9Value)        
        
    if not StrainCh10MqttSubscribeQueue.empty():
        StrainCh10Value = StrainCh10MqttSubscribeQueue.get()
    else:
        StrainCh10Value = "0x0F"
    if StrainCh10Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainCh10Value", StrainCh10Value)        
        
    if not StrainM2AI3MqttSubscribeQueue.empty():
        StrainM2AI3Value = StrainM2AI3MqttSubscribeQueue.get()
    else:
        StrainM2AI3Value = "0x0F"
    if StrainM2AI3Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM2AI3Value", StrainM2AI3Value)
    
    if not StrainM2AI4MqttSubscribeQueue.empty():
        StrainM2AI4Value = StrainM2AI4MqttSubscribeQueue.get()
    else:
        StrainM2AI4Value = "0x0F"
    if StrainM2AI4Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM2AI4Value", StrainM2AI4Value)
        
    if not StrainM1AI2MqttSubscribeQueue.empty():
        StrainM1AI2Value = StrainM1AI2MqttSubscribeQueue.get()
    else:
        StrainM1AI2Value = "0x0F"
    if StrainM1AI2Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM1AI2Value", StrainM1AI2Value)
        
    if not StrainM1AI3MqttSubscribeQueue.empty():
        StrainM1AI3Value = StrainM1AI3MqttSubscribeQueue.get()
    else:
        StrainM1AI3Value = "0x0F"
    if StrainM1AI3Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM1AI3Value", StrainM1AI3Value)
        
    if not StrainM1AI4MqttSubscribeQueue.empty():
        StrainM1AI4Value = StrainM1AI4MqttSubscribeQueue.get()
    else:
        StrainM1AI4Value = "0x0F"
    if StrainM1AI4Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM1AI4Value", StrainM1AI4Value)
        
    if not StrainM1AI5MqttSubscribeQueue.empty():
        StrainM1AI5Value = StrainM1AI5MqttSubscribeQueue.get()
    else:
        StrainM1AI5Value = "0x0F"
    if StrainM1AI5Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM1AI5Value", StrainM1AI5Value)
        
    if not StrainM1AI6MqttSubscribeQueue.empty():
        StrainM1AI6Value = StrainM1AI6MqttSubscribeQueue.get()
    else:
        StrainM1AI6Value = "0x0F"  
    if StrainM1AI6Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM1AI6Value", StrainM1AI6Value)
        
    if not StrainM1AI7MqttSubscribeQueue.empty():
        StrainM1AI7Value = StrainM1AI7MqttSubscribeQueue.get()
    else:
        StrainM1AI7Value = "0x0F"
    if StrainM1AI7Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM1AI7Value", StrainM1AI7Value)
        
    if not StrainM2AI6MqttSubscribeQueue.empty():
        StrainM2AI6Value = StrainM2AI6MqttSubscribeQueue.get()
    else:
        StrainM2AI6Value = "0x0F"   
    if StrainM2AI6Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM2AI6Value", StrainM2AI6Value)
        
    if not StrainM2AI5MqttSubscribeQueue.empty():
        StrainM2AI5Value = StrainM2AI5MqttSubscribeQueue.get()
    else:
        StrainM2AI5Value = "0x0F"
    if StrainM2AI5Value == '0x0F':
        pass
    else:
        MqttClient.publish("UI/Smol/StrainM2AI5Value", StrainM2AI5Value)
            
    # Step 2: read flow from MFC and get the timestamp (computer time)

    H2FlowRate = Mfc.read_flow()
    H2RxTimestamp = datetime.datetime.now()
    
    H2FlowDelta = H2FlowRate - H2FlowRatePrev
    H2RxTimestampDeltaDt = H2RxTimestamp - H2RxTimestampPrev
    H2RxTimestampDeltaMins = (H2RxTimestampDeltaDt.seconds)/60

    H2TransferredInLitres = 0.5*(H2FlowDelta * H2RxTimestampDelta) # Volume from trapezoid method
    H2TransferredInLitresTotal = H2TransferredInLitresTotal + H2TransferredInLitres

    H2RxTimestampPrev = H2RxTimestamp
    H2FlowRatePrev = H2FlowRate

    # Sends "R" to the HyCycle PCB

    ArdSerial.write("R".encode())

    # Read the line of temperature data from thermocouples and pressure transducer
    try:
        TempsAndPressure = ArdSerial.readline().decode() 
        strs = TempsAndPressure.split()
        Pressure = strs[0].strip(", ")
        Temp1 = strs[1].strip(", ")
        Temp2 = strs[2].strip(", ")
        Temp3 = strs[3].strip(", ")
        Temp4 = strs[4].strip(", ")
        #Temp1 = strs[1]
        #Temp2 = strs[2]
        #Temp3 = strs[3]
        #Temp4 = strs[4]
        
        #Temp1 = TempsAndPressure[TempsAndPressure.index(", ")+2:TempsAndPressure.rindex(", ")]
        #Temp2 = TempsAndPressure[TempsAndPressure.index(", ")+2:TempsAndPressure.rindex(", ")]
        #Temp3 = TempsAndPressure[TempsAndPressure.index(", ")+2:TempsAndPressure.rindex(", ")]
        #Temp4 = TempsAndPressure[TempsAndPressure.rindex(", ")+2:].replace("\r\n","")
        #Pressure = TempsAndPressure[:TempsAndPressure.index(", ")]
        
    except:
        Temp1 = '0xFF'
        Temp2 = '0xFF'
        Temp3 = '0xFF'
        Temp4 = '0xFF'
        Pressure = '0xFF'

    
    # All the other data are parsed to the UI

    MqttClient.publish("UI/Smol/H2flowrate", H2FlowRate)
    MqttClient.publish("UI/Smol/Temp1", Temp1)
    MqttClient.publish("UI/Smol/Temp2", Temp2)
    MqttClient.publish("UI/Smol/Temp3", Temp3)
    MqttClient.publish("UI/Smol/Temp4", Temp4)
    MqttClient.publish("UI/Smol/Pressure", Pressure)
    MqttClient.publish("UI/Smol/H2TransferredInLitresTotal", H2TransferredInLitresTotal)

    # Generate the string containing the data

    #CliString = str(Timestamp) + "," + str(StrainCh9Value) + "," + str(StrainCh10Value) + "," + str(H2FlowRate)  + "," + str(Temp1)  + "," + str(Temp2) + "," + str(Pressure) + "," + str(H2TransferredInLitresTotal)
    CliString = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(Timestamp, StrainCh9Value, StrainCh10Value, H2FlowRate, Temp1, Temp2, Temp3, Temp4, Pressure, H2TransferredInLitresTotal, StrainM2AI3Value, StrainM2AI4Value,
        StrainM1AI2Value, StrainM1AI3Value, StrainM1AI4Value, StrainM1AI5Value, StrainM1AI6Value, StrainM1AI7Value, StrainM2AI6Value, StrainM2AI5Value
    )

    # If there is a local log file, write the string in the file
    
    if(LogFileInstance_local != None and not LogFileInstance_local.closed):
        try:
            LogFileInstance_local.write(CliString + "\n")
        except:
            print("##### FAILED TO WRITE TO LOCAL FILE #####")
        #try:
        #    LogFileInstance.flush()
        #except:
        #    print("Flush failed, continuing...")
    
    # If there is a glocal log file, write the string in the file
        
    if(GlobalLogFileInstance_local != None and not GlobalLogFileInstance_local.closed):
        try:
            GlobalLogFileInstance_local.write(CliString + "\n")
        except:
            print("##### FAILED TO WRITE TO GLOBAL FILE #####")
        
    print(CliString.strip())
    return True

#MQTT setup
MqttClient = mqtt.Client()
MqttClient.on_connect = MqttOnConnect
MqttClient.on_message = MqttOnMessage
MqttClient.connect("localhost", 1883, 60)

i = 0
j = 0
AbsMode = True
CurrentCycle = 1
H2FlowRate = 0
H2FlowRatePrev = 0
H2FlowDelta = 0
H2TransferredInLitres = 0
H2TransferredInLitresPrev = 0
H2RxTimestamp = 0
H2RxTimestampPrev = datetime.datetime.now()
H2RxTimestampDelta = 0
H2TransferredInLitresTotal = 0
H2RxTimestampDeltaSecs = 1
H2TransferredInLitresTotal = 0

print("H2GO Power (C)")
print("Reactor Rig Controller 2")
print("Deployed 01/07/2022 - M CHANA")
print("Modified 11/10/2022 - H SHALLCROSS")
print("Updated COM Port 12/04/23 - HS")
print("Updated cycles between saves 11/05/23 - HS")
print("Modified 11/07/204 - S GADOLINI - Strain Limit\n\n")

PumpRate = int(input("Please enter pump power level (0-9):  "))
AbsFlowRate = int(input("Please enter absorption test hydrogen flow rate in L/min:  "))
DesFlowRate = int(input("Please enter desorption test hydrogen flow rate in L/min:  "))
AbsTestTime = int(input("Please enter absorption test time in seconds:  "))
DesTestTime = int(input("Please enter desorption test time in seconds:  "))
TotalCyclesReq = int(input("Please enter number of abs/des test cycles to complete:  "))
input("Please hit Enter to begin automated cycling")

Mfc = bronkhorst.Bronkhorst("COM20", 15)
ArdSerial = serial.Serial(port="COM16", baudrate=115200) # To communicate with HyCycle PCB
ArdSerial.timeout = 1

time.sleep(0.5)
ArdSerial.write("5".encode()) #Prestart pump
time.sleep(1)
ArdSerial.write(str(PumpRate).encode()) #Send pump rate to arduino

DateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Logging initialisation 

GlobalLogFilename = str(DateTime).replace("-","").replace(":","") + "_RRC2-AllLogs.txt"
GlobalLogFilename_local = "C:\\RRC2_Dbg\\" + GlobalLogFilename
GlobalLogFilename2 = "G:\\.shortcut-targets-by-id\\1YKzDTeDe8DL8RND2abr3A394QVlBfy8V\\H2GO Power Product Development\\HySTOR\\HySTOR Alpha\\Chemical\\HyCYCLE\\Testing\\HyCYCLE Raw Data\\" + GlobalLogFilename
GlobalLogFileInstance = open(GlobalLogFilename2, "at")
GlobalLogFileInstance_local = open(GlobalLogFilename_local, "at")

StartHeader = "RRC2 log start" + "\nPump Flow Rate: " + str(PumpRate) + "\n"
TestHeader = "Absorption flow rate: " + str(AbsFlowRate) + "L/min, Desorption flow rate: "  + str(DesFlowRate) + "L/min, Absorption test time: " + str(AbsTestTime) + "sec, Desorption test time: " + str(DesTestTime) + "sec, Total cycles: " + str(TotalCyclesReq)
DataHeader = "t, Strain9, Strain10, H2flowrate, Temp1, Temp2, Temp3, Temp4, Pressure, H2_transferred_cumulative, StrainM2AI3, StrainM2AI4, StrainM1AI2, StrainM1AI3, StrainM1AI4, StrainM1AI5, StrainM1AI6, StrainM1AI7, StrainM2AI6, StrainM2AI5" 


GlobalLogFileInstance_local.write(StartHeader + "\n")
GlobalLogFileInstance_local.write(TestHeader + "\n")
GlobalLogFileInstance_local.write(DataHeader + "\n")


CommHeartbeatStartTime = datetime.datetime.now().replace(microsecond=0)
CommHeartbeatEndTime = CommHeartbeatStartTime + timedelta(seconds=10)
CommHeartbeatEndTime = CommHeartbeatEndTime.replace(microsecond=0)

# while datetime.datetime.now().replace(microsecond=0) <= CommHeartbeatEndTime:
#     MqttClient.publish("UI/Smol/GuiHeartbeat", j)
#     print("Gui Heartbeat " + str(j))

#     time.sleep(0.5)
#     j = j + 1

# Write the user input values

MqttClient.publish("UI/Smol/AbsFlowRate", AbsFlowRate)
MqttClient.publish("UI/Smol/DesFlowRate", DesFlowRate)
MqttClient.publish("UI/Smol/AbsTestTime", AbsTestTime)
MqttClient.publish("UI/Smol/DesTestTime", DesTestTime)
MqttClient.publish("UI/Smol/TotalCyclesReq", TotalCyclesReq)

SessionStartTime = datetime.datetime.now().replace(microsecond=0)
SessionDuration = TotalCyclesReq * (AbsTestTime + DesTestTime)
SessionEndTime = datetime.datetime.now().replace(microsecond=0) + timedelta(seconds=SessionDuration)

MqttClient.publish("UI/Smol/SessionStartTime", SessionStartTime.__str__())
MqttClient.publish("UI/Smol/SessionEndTime", SessionEndTime.__str__())


LogFileInstance = None
LogFileInstance_local = None

filecycle = 0
#Cycle until current cycle exceeds user req number
while CurrentCycle <= TotalCyclesReq:

    MqttClient.publish("UI/Smol/CurrentCycle", CurrentCycle) # Tell UI which cycle we are running
    
    if(filecycle == 0):
        DateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        LogFilename = str(DateTime).replace("-","").replace(":","") + "_RRC2.txt"
        LogFilename2_local = "C:\\RRC2_Dbg\\" + LogFilename
        LogFilename2 = "G:\\.shortcut-targets-by-id\\1YKzDTeDe8DL8RND2abr3A394QVlBfy8V\\H2GO Power Product Development\\HySTOR\\HySTOR Alpha\\Chemical\\HyCYCLE\\Testing\\HyCYCLE Raw Data\\" + LogFilename

        LogFileInstance_local = open(LogFilename2_local, "at")
        StartHeader = "RRC2 log start" + "\nPump Flow Rate: " + str(PumpRate) + "\n"
        TestHeader = "Absorption flow rate: " + str(AbsFlowRate) + "L/min, Desorption flow rate: "  + str(DesFlowRate) + "L/min, Absorption test time: " + str(AbsTestTime) + "sec, Desorption test time: " + str(DesTestTime) + "sec, Total cycles: " + str(TotalCyclesReq)
        DataHeader = "t, Strain9, Strain10, H2flowrate, Temp1, Temp2, Temp3, Temp4, Pressure, H2_transferred_cumulative, StrainM2AI3, StrainM2AI4, StrainM1AI2, StrainM1AI3, StrainM1AI4, StrainM1AI5, StrainM1AI6, StrainM1AI7, StrainM2AI6, StrainM2AI5" 

        
        LogFileInstance_local.write(StartHeader + "\n")
        LogFileInstance_local.write(TestHeader + "\n")
        LogFileInstance_local.write(DataHeader + "\n")

    #First cycle is absorption mode
    if AbsMode == True:
        XxsStartTime = datetime.datetime.now()
        MqttClient.publish("UI/Smol/TestMode", "Absorption")
        MqttClient.publish("UI/Smol/AbsStartTime", XxsStartTime.replace(microsecond=0).__str__())
        AbsHeader = "***Start absorption " + str(CurrentCycle) + "***"
        print(AbsHeader)
        LogFileInstance_local.write(AbsHeader + "\n")
        GlobalLogFileInstance_local.write(AbsHeader + "\n")
        ArdSerial.write("A".encode())
        time.sleep(1)
        Mfc.set_flow(AbsFlowRate)
        TimeElapsed = 0

        CycleStartTime = datetime.datetime.now().replace(microsecond=0)
        CycleEndTime = CycleStartTime + timedelta(seconds=AbsTestTime)
        CycleEndTime = CycleEndTime.replace(microsecond=0)

        while datetime.datetime.now().replace(microsecond=0) <= CycleEndTime:
            MqttClient.loop_start()
            SampleAndPrint()

            if StrainCh9Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainCh9Value", StrainCh9Value)                            
                if float(StrainCh9Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai0 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainCh9Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break
                    
            if StrainCh10Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainCh10Value", StrainCh10Value)                            
                if float(StrainCh10Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai1 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainCh10Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break

            if StrainM1AI2Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM1AI2Value", StrainM1AI2Value)        
                if float(StrainM1AI2Value) > UPPER_LIMIT:
                    print("Strain gauge m1ai2 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI2Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break     

            if StrainM1AI3Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM1AI3Value", StrainM1AI3Value)       
                if float(StrainM1AI3Value) > UPPER_LIMIT:
                    print("Strain gauge m1ai3 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI3Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break        
            
            if StrainM1AI4Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM1AI4Value", StrainM1AI4Value)        
                if float(StrainM1AI4Value) > UPPER_LIMIT:
                    print("Strain gauge m1ai4 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI4Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break
                   
            if StrainM1AI5Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM1AI5Value", StrainM1AI5Value)                            
                if float(StrainM1AI5Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai5 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI5Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break  
                  
            if StrainM1AI6Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM1AI6Value", StrainM1AI6Value)                            
                if float(StrainM1AI6Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai6 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI6Value), UPPER_LIMIT))                 
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break   
                  
            if StrainM1AI7Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM1AI7Value", StrainM1AI7Value)                            
                if float(StrainM1AI7Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai7 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI7Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break    
                
            if StrainM2AI3Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM2AI3Value", StrainM2AI3Value)                           
                if float(StrainM2AI3Value) > UPPER_LIMIT:                    
                    print("Strain gauge m2ai3 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI3Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break          

            if StrainM2AI4Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM2AI4Value", StrainM2AI4Value)        
                if float(StrainM2AI4Value) > UPPER_LIMIT:
                    print("Strain gauge m2ai4 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI4Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break
                 
            if StrainM2AI5Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM2AI5Value", StrainM2AI5Value)                            
                if float(StrainM2AI5Value) > UPPER_LIMIT:                    
                    print("Strain gauge m2ai5 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI5Value), UPPER_LIMIT))                   
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break 
           
            if StrainM2AI6Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM2AI6Value", StrainM2AI6Value)                            
                if float(StrainM2AI6Value) > UPPER_LIMIT:                    
                    print("Strain gauge m2ai6 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI6Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break    

            TimeElapsed = datetime.datetime.now() - XxsStartTime
            MqttClient.publish("UI/Smol/TimeElapsed", int(TimeElapsed.total_seconds()))
            MqttClient.loop_stop()

        #Stop procedure
        AbsFooter = "***Complete absorption " + str(CurrentCycle) + "***"
        MqttClient.publish("UI/Smol/AbsStartTime", "-")
        print("\n" + AbsFooter)
        LogFileInstance_local.write(AbsFooter + "\n")
        GlobalLogFileInstance_local.write(AbsFooter + "\n")
        StopAndTransitionMode(Mfc, ArdSerial)
        AbsMode = not AbsMode

    #Alternate cycle is always desorption mode
    if AbsMode == False:
        XxsStartTime = datetime.datetime.now()
        MqttClient.publish("UI/Smol/TestMode", "Desorption")
        MqttClient.publish("UI/Smol/DesStartTime", XxsStartTime.replace(microsecond=0).__str__())
        DesHeader = "***Start desorption " + str(CurrentCycle) + "***"
        print(DesHeader)
        LogFileInstance_local.write(DesHeader + "\n")
        GlobalLogFileInstance_local.write(DesHeader + "\n")
        ArdSerial.write("D".encode())
        time.sleep(1)
        Mfc.set_flow(DesFlowRate)
        TimeElapsed = 0

        CycleStartTime = datetime.datetime.now().replace(microsecond=0)
        CycleEndTime = CycleStartTime + timedelta(seconds=DesTestTime)
        CycleEndTime = CycleEndTime.replace(microsecond=0)

        while datetime.datetime.now().replace(microsecond=0) <= CycleEndTime:
            MqttClient.loop_start()
            SampleAndPrint()
            
            if StrainCh9Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainCh9Value", StrainCh9Value)                            
                if float(StrainCh9Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai0 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainCh9Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break
                    
            if StrainCh10Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainCh10Value", StrainCh10Value)                            
                if float(StrainCh10Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai1 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainCh10Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break

            if StrainM1AI2Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM1AI2Value", StrainM1AI2Value)        
                if float(StrainM1AI2Value) > UPPER_LIMIT:
                    print("Strain gauge m1ai2 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI2Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break     

            if StrainM1AI3Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM1AI3Value", StrainM1AI3Value)       
                if float(StrainM1AI3Value) > UPPER_LIMIT:
                    print("Strain gauge m1ai3 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI3Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break        
            
            if StrainM1AI4Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM1AI4Value", StrainM1AI4Value)        
                if float(StrainM1AI4Value) > UPPER_LIMIT:
                    print("Strain gauge m1ai4 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI4Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break
                   
            if StrainM1AI5Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM1AI5Value", StrainM1AI5Value)                            
                if float(StrainM1AI5Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai5 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI5Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break  
                  
            if StrainM1AI6Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM1AI6Value", StrainM1AI6Value)                            
                if float(StrainM1AI6Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai6 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI6Value), UPPER_LIMIT))                 
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break   
                  
            if StrainM1AI7Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM1AI7Value", StrainM1AI7Value)                            
                if float(StrainM1AI7Value) > UPPER_LIMIT:                    
                    print("Strain gauge m1ai7 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM1AI7Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break    
                
            if StrainM2AI3Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM2AI3Value", StrainM2AI3Value)                           
                if float(StrainM2AI3Value) > UPPER_LIMIT:                    
                    print("Strain gauge m2ai3 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI3Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break          

            if StrainM2AI4Value != "0x0F":
                MqttClient.publish("UI/Smol/StrainM2AI4Value", StrainM2AI4Value)        
                if float(StrainM2AI4Value) > UPPER_LIMIT:
                    print("Strain gauge m2ai4 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI4Value), UPPER_LIMIT))
                    StopAndTransitionMode(Mfc, ArdSerial)
                    break
                 
            if StrainM2AI5Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM2AI5Value", StrainM2AI5Value)                            
                if float(StrainM2AI5Value) > UPPER_LIMIT:                    
                    print("Strain gauge m2ai5 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI5Value), UPPER_LIMIT))                   
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break 
           
            if StrainM2AI6Value != "0x0F":                    
                MqttClient.publish("UI/Smol/StrainM2AI6Value", StrainM2AI6Value)                            
                if float(StrainM2AI6Value) > UPPER_LIMIT:                    
                    print("Strain gauge m2ai6 value {} exceeds upper limit of {}. Stopping cycle.".format(float(StrainM2AI6Value), UPPER_LIMIT))                    
                    StopAndTransitionMode(Mfc, ArdSerial)                    
                    break  
            
            TimeElapsed = datetime.datetime.now() - XxsStartTime
            MqttClient.publish("UI/Smol/TimeElapsed", int(TimeElapsed.total_seconds()))
            MqttClient.loop_stop()

        #Stop procedure
        DesFooter = "***Complete desorption " + str(CurrentCycle) + "***"
        MqttClient.publish("UI/Smol/DesStartTime", "-")
        print("\n" + DesFooter)
        LogFileInstance_local.write(DesFooter + "\n")
        GlobalLogFileInstance_local.write(DesFooter + "\n")
        StopAndTransitionMode(Mfc, ArdSerial)
        AbsMode = not AbsMode

    CurrentCycle = CurrentCycle + 1
    filecycle += 1;
    
    if(filecycle == 24):
        CompleteFooter = "RRC2 log complete"
        LogFileInstance_local.write(CompleteFooter)
        LogFileInstance_local.close()
        filecycle = 0;


#Non multiple of 12
if filecycle != 0:
    CompleteFooter = "RRC2 log complete"
    LogFileInstance_local.write(CompleteFooter)
    LogFileInstance_local.close()

ArdSerial.write("S".encode())

CompleteFooter = "RRC2 log complete"

GlobalLogFileInstance_local.write(CompleteFooter)
GlobalLogFileInstance_local.close()