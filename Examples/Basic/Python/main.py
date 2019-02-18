import krpc
import serial
import time
from select_port import select_port

running = True
server = None
arduino = None
while server is None or arduino is None:
	#We do not know if the server is online, so we want python to try to connect.
	try: 
		#The next line starts the connection with the server. It describes itself to the game as controller.
		server = krpc.connect(name ='Controller')
		#Now let's connect to the Arduino
		arduino = serial.Serial(port = select_port(), baudrate = 112500)
	except ConnectionRefusedError: #error raised whe failing to connect to the server.
		print("Server offline")
		time.sleep(5) #sleep 5 seconds
		server = None
		arduino = None
	except serial.SerialException: #error raised when failling to connect to an arduino
		#TIPP: check if the Arduino serial monitor is off! or any other program using the arduino
		print("Arduino Connection Error.")	
		time.sleep(5)
		server = None
		arduino = None
		
time.sleep(2)
print("Started")
#The program has sucessfully started
while running:
	#PROBLEM: If the vessel is destroyed, or we switch to the hangar or anything, we can no longer controll it
	#  The Program will then fail.
	#SOLUTION: the "try:" statement
	#  If anything goes wrong inside a "try" block, 
	#  we can continue the program if we "catch" the error in the except clauses.	
	try: 
		if scene != ksp_server.space_center.current_game_scene.flight:
			time.sleep(1) #KSP is not in flight mode. Wait one second and check again.
			continue #skip the rest of the loop and check again.

		#We now tell the server what stuff we want streamed.
		
			
		#And at last we can start sending the data from the Arduino.
		while running:
			pass
		
	except krpc.error.RPCError as e:
		print("KSP Scene Changed!")
		time.sleep(1)
	except ConnectionAbortedError:
		print("KSP has Disconnected.")
		running = False #we can now end the program.