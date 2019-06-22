

# =============================================== #
# ============== Bytes -> Normal ================ #
# =============================================== #

# gets a c++ uint8 from a byte(8bit unsigned integer)
def uint8_from_byte(thebyte):
	return int.from_byte(thebyte, byteorder="big")


# gets the c++ char stored in a byte.
# special letters are replaced by "-"
def letter_from_byte(thebyte):
	try


# gets a float stored in 4 bytes.
def float_from_4bytes(bytelist):
	pass


# gets a float stored in 8 bytes.
def float_from_8bytes(bytelist):
	pass


# sometimes numbers get sent in a format 298.142
# this functions reads ints and floats like that.
def number_from_bytes_written(bytelist):
	number = 0
	decimal = 0
	for b in bytelist:
		letter = uint8_from_byte(b) - 0
		if letter < 0:
			break
		else:
			if b == b'.':
				decimal = 1
			elif decimal == 0:
				number *= 10
				number += letter
			else:
				number += letter/10
				decimal += 1
	return number


# makes a normal string from a bytestring
# special letters are replaced by "-"
def string_from_bytestring(bytelist):
	stringstore = ""
	for b in bytelist:
		stringstore.append(letter_from_byte(b))
	return stringstore


# =============================================== #
# ============== Normal -> Bytes ================ #
# =============================================== #

# Encodes a string as bytes to be sent to the arduino.
def bytelist_from_string(thestring):
	pass


# Encodes a number as a c++ byte
def byte_from_uint8(number):
	if number > 255 or number < 0:
		raise ValueError("number must fit to uint8 0<x<255")
	else:
		pass


# Encodes a larger number as an c++ int
def bytes_from_unint16(number):
	pass


# Etc..
def bytes_from_float32(number):
	pass


def bytes_from_float64(number):
	pass
