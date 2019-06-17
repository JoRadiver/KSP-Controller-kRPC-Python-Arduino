# Ask the user to select a serial port
from serial.tools import list_ports


def select_port():
	while True:
		print("Avaliable Serial Ports:")
		ports = []
		for n, (port, description, hwid) in enumerate(sorted(list_ports.comports())):
			print("--", n, ":     ", port, "     ", description)
			ports.append(port)
		port_index = input("Enter the number of the Port")
		try:
			if int(port_index) <= len(ports)-1:  # checking if port is valid
				port = ports[int(port_index)]
			else:
				raise ValueError
		except ValueError:
			print("Failed to select port. Retry.")
		else:
			return port
