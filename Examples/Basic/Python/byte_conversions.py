

# =============================================== #
# ============== Bytes -> Normal ================ #
# =============================================== #


# gets strings stored in a bytestring.
# special letters are replaced by "?"
def string_from_byte(bytestring):
	return bytestring.decode(encoding='utf-8', errors='ignore')


# decodes numbers in a format like b'298.142'
# this functions reads ints and floats like that.
def number_from_bytes_literal(bytestring):
	number = bytestring.decode(encoding='utf-8', errors='ignore')
	return float(number)


# gets a c++ uint8 from a byte(8bit unsigned integer)
def uint8_from_byte(thebyte):
	return int.from_byte(thebyte, byteorder="big")


# gets a c float stored in 4 bytes.
def float_from_4bytes(bytestring):
	pass


# gets a c float stored in 8 bytes.
def float_from_8bytes(bytestring):
	pass

# =============================================== #
# ============== Normal -> Bytes ================ #
# =============================================== #


# Encodes a string as bytes to be sent to the arduino.
def bytestring_from_string(thestring):
	return thestring.encode(encoding='utf-8', errors='ignore')


# makes numbers like b'123.321' from floats or ints
def literal_number_from_number(thenumber):
	return str(thenumber).encode(encoding='utf-8', errors='ignore')


# Encodes a number as a c++ byte
def byte_from_uint8(number):
	if number > 255 or number < 0:
		raise ValueError("number must fit to uint8 0<x<255")
	else:
		pass


# Encodes a larger number as an c++ int
def bytes_from_uint16(number):
	pass


# Etc..
def bytes_from_float32(number):
	pass


def bytes_from_float64(number):
	pass
