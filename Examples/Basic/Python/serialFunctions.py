#serial Message EBNF:
# SerialMessage = "s", type, length, data ;
# type = ascii-character
# length = number_as_byte
# data = length * byte
# byte = a c++ byte

def byte_to_int(byte):
	return int.from_bytes(byte, byteorder = 'big')

class ArduinoSerial:
	def __init__(self, arduino):
		self.arduino = arduino
		self.badmessage = SerialMessage('_', 0, []) #is always returned if an error occured while reading.
	def readMessage(self):
		if arduino.read() != b's': #if the firs letter is not start character.
			return self.badmessage
		type = arduino.read().decode('utf-8')
		length = byte_to_int(arduino.read())
		bytearray = arduino.read(length)
		return SerialMessage(type, length, bytearray)

class SerialMessage:
	def __init__(self, type, length, data):
		self.type = type
		self.length = length
		self.data = data
	