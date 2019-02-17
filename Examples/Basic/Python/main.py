import krpc
import serial
import time
from select_port import select_port
	

#The next line starts the connection with the server, so that the server is available under "kRPC",
#And it makes connection with the Ardiuno.
with krpc.connect(name ='Arduino') as kRPC, serial.Serial(port = select_port(), baudrate = 112500) as arduino:
	print("Started")
	running = True
	#The program has sucessfully started
	#We now tell the server what stuff we want streamed.
	while running:
		pass