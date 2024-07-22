import struct
import fileinput

def CanDecode4ByteIntelLittleEnd(InputVal, ScalerVal):
	InputValToHex = hex(int(InputVal))
	CorrectedFirstByte = InputValToHex[4:6]
	CorrectedSecondByte = InputValToHex[2:4]
	CorrectedByteSequence = CorrectedFirstByte + CorrectedSecondByte
	CorrectedByteSequenceToInt = int(CorrectedByteSequence,16)
	
	ScaledOutput = CorrectedByteSequenceToInt * ScalerVal
	ScaledOutputStr = str(ScaledOutput)
	
	return ScaledOutput, ScaledOutputStr

def CanDecode4ByteMotorolaBigEnd(InputVal, ScalerVal):
	InputValToHex = hex(int(InputVal))
	CorrectedFirstByte = InputValToHex[2:4]
	CorrectedSecondByte = InputValToHex[4:6]
	CorrectedByteSequence = CorrectedFirstByte + CorrectedSecondByte
	CorrectedByteSequenceToInt = int(CorrectedByteSequence,16)
	
	ScaledOutput = CorrectedByteSequenceToInt * ScalerVal
	ScaledOutputStr = str(ScaledOutput)
	
	return ScaledOutput, ScaledOutputStr

def CanRxHexRecompile(InputVal):
	Output = hex(int(InputVal))
	
	return Output

def ExtractRawHexDataFromCanFrame(RawHexData, startbytepos, endbytepos):
	Output = RawHexData[startbytepos:endbytepos]
	
	return Output

def IeeeFloatManualReassembleFromCan(Byte1, Byte2, Byte3,Byte4):
	ByteList = [int(Byte1), int(Byte2), int(Byte3), int(Byte4)]
	ByteArray = bytearray(ByteList)
	ReassembledFloat = struct.unpack('<f', ByteArray)
	
	return ReassembledFloat[0]

def CanTx32BitHexAssemble(InputVal):
	Output = bytearray(struct.pack('<f', InputVal))
	#print(["0x%02x" % bytes for bytes in Output])
	return Output

def EnapterEl20ModbusRx(ModbusDevice, MbReg, Sz, CovnLsb):
	if Sz == 32:
		RegRead = ModbusDevice.read_input_registers(MbReg, 2)

		Byte1 = RegRead.getRegister(1)
		Byte2 = RegRead.getRegister(0)
		
		Byte1h = hex(Byte1)
		Byte2h = hex(Byte2)
		
		RegValue = Byte1h + Byte2h
		RegValue = RegValue.replace('0x', '')
		
		if len(RegValue) == 7:
			RegValue = '0' + RegValue
		
		VariableValue = float(CovnLsb) * float(int(RegValue,16))
	
		return VariableValue
	
	if Sz == 16:
		
		RegRead = ModbusDevice.read_input_registers(MbReg, 1)
		Byte1 = RegRead.getRegister(0)
		Byte1h = hex(Byte1)
		RegValue = Byte1h
		
		if len(RegValue) == 3:
			RegValue = '0' + RegValue
			
		return RegValue
	
	else:
		print("Invalid size - Refer to online Enapter Handbook")

def EnapterEl20ModbusTx(ModbusDevice, MbCoil, WriteVal):
	ModbusDevice.write_coil(MbCoil, WriteVal)

def EnapterEl21ModbusRx(ModbusDevice, MbReg, typ):
	
	if typ == "bool":
		RegLen = 1
	if typ == "uint16":
		RegLen = 1
	if typ == "uint32":
		RegLen = 2
	if typ == "uint64":
		RegLen = 4
	if typ == "float32":
		RegLen = 2
		
	RegRead = ModbusDevice.read_input_registers(MbReg, RegLen)
	IncomingData = []
	HexPrefixStrippedIncomingData = []
	
	for reg in range(RegLen):
		IncomingData.append(hex(RegRead.getRegister(reg)))
		
	for pkt in IncomingData:
		pkt = pkt.replace("0x","")
		HexPrefixStrippedIncomingData.append(pkt)
	
	if typ == "bool":
		pass
	if typ == "uint16":
		RxVal = HexPrefixStrippedIncomingData
	if typ == "uint32":
		pass
	if typ == "uint64":
		pass
	if typ == "float32":
		ByteArray = "".join(HexPrefixStrippedIncomingData)

		B1 = int(ByteArray[:2],16)
		B2 = int(ByteArray[2:4],16)
		B3 = int(ByteArray[4:6],16)
		try:
			B4 = int(ByteArray[6:],16)
		except ValueError:
			B4 = int("0",16)
	
		

		ByteList = [B1, B2, B3, B4]
		ByteArray = bytearray(ByteList)
		ReassembledFloat = struct.unpack('>f', ByteArray)
		RxVal = ReassembledFloat[0]
		

	return RxVal

def LegacyFormatGetLineVal(filehandle, optiontag):

	file = open(filehandle, "r")
	lines = file.readlines()

	for line in lines:
		if line.startswith(optiontag):
			try:
				return line[line.index('"')+1:line.index('";')]
			finally:
				file.close()

def LegacyFormatSetLineVal(filehandle, optiontag, newval):

	for line in fileinput.input(filehandle, inplace=True):
		if line.startswith(optiontag):
			CommentFlag = 0
			try:
				CommentBeginIndex = line.find("//")
				CommentFlag = 1
			except Exception as e:
				print(e)

			if CommentFlag == 0:
				NewLine = optiontag + '="' + newval + '";'
			if CommentFlag == 1:
				NewLine = optiontag + '="' + newval + '"; ' + line[CommentBeginIndex:]

			print(line.replace(line, NewLine).rstrip())

		else:
			print(line.rstrip())

def ArduinoLikeMapFunction(ValToMap, InputMin, InputMax, OutputMin, OutputMax):
    return float((ValToMap - InputMin) * (OutputMax - OutputMin) / (InputMax - InputMin) + OutputMin)