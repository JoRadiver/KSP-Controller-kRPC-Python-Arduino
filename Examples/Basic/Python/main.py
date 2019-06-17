import krpc
import serial
import time
from select_port import select_port

running = True
server = None
arduino = None
while server is None or arduino is None:
	# We do not know if the server is online, so we want python to try to connect.
	try: 
		# The next line starts the connection with the server. It describes itself to the game as controller.
		server = krpc.connect(name='Controller')
		# Now let's connect to the Arduino
		arduino = serial.Serial(port=select_port(), baudrate=112500)
	except ConnectionRefusedError:  # error raised whe failing to connect to the server.
		print("Server offline")
		time.sleep(5)  # sleep 5 seconds
		server = None
		arduino = None
	except serial.SerialException:  # error raised when failing to connect to an Arduino
		# TIP: check if the Arduino serial monitor is off! or any other program using the Arduino
		print("Arduino Connection Error.")	
		time.sleep(5)
		server = None
		arduino = None
		
time.sleep(2)
print("Started")
# The program has sucessfully started
while running:
	# PROBLEM: If the vessel is destroyed, or we switch to the hangar or anything, we can no longer controll it
	#  The Program will then fail.
	# SOLUTION: the "try:" statement
	#  If anything goes wrong inside a "try" block, 
	#  we can continue the program if we "catch" the error in the except clauses.	
	try: 
		if scene != server.space_center.current_game_scene.flight:
			time.sleep(1) # KSP is not in flight mode. Wait one second and check again.
			continue # skip the rest of the loop and check again.

		vessel = server.space_center.active_vessel # the vessel we are using
		
		# We now tell the server what stuff we want streamed.
		
		# lets say we want to know the status of the solar panels and the oxidizer level.
		
		# there are two types of streams, you have to set them up differently for attributes and functions
		# first for attributes:
		solar_panels = server.con.add_stream(getattr, vessel.control, "solar_panels")
		'''solar panels are an attribute of the class Control.
		you can find it here in the docs: https://krpc.github.io/krpc/python/api/space-center/control.html
		you will see under solar_panels, that it is an Attribute. 
		because of that the add_stream function has to have gettatr as its first argument. 
		The second argument is the class where our attribute is located.
		Its in the control attribute of our vessel.
		The last argument is the name of the argument, as it is in the docs.'''
		# Just as s a further example apoapsis_altitude looks like this:
		apoapsis_height = server.con.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
		
		# now for functions:
		has_oxidizer = server.con.add_stream(vessel.resources.has_resource, "Oxidizer")
		# gives us a stream where we can check if the vessel can store a certain ressource.
		# to know this is important because if the oxidizer tank blows up, it will become false.
		# and then our oxidizer_max is zero, and if we divide to get the percentage, we divide by zero and our porgram aborts.
		'''For functions, as a first argument we give the function. 
		So on the ressources page (https://krpc.github.io/krpc/python/api/space-center/resources.html)
		we see at the top that is is of course part of our vessel, because we want the ressources of our vessel.
		the function we want is called has_resource(name) and it needs a name.
		to get the names of the ressources you can do
		for res in resources.all:
			print (res.name)
		To give a function the attributes it needs, we can just add them as further arguments of add_stream.
		if we wanted to stream a function randomFunc(a, b, c) of our vessel, we would do
		self.con.add_stream(vessel.randomFunc, a, b, c)'''
		oxidizer_level = server.con.add_stream(vessel.resources.has_resource, "Oxidizer")
		oxidizer_max = server.con.add_stream(vessel.resources.max, "Oxidizer")
		oxidizer_current = server.con.add_stream(vessel.resources.amount, "Oxidizer")
			
		# And at last we can start sending the data from the Arduino.
		while running:
			# To get the data from the streams, we have to call our streams:
			solar_panel_led = solar_panels()

			# now lets find out if we have below 5% fuel left:
			fuel_low_led = 0
			if has_oxidizer():
				if oxidizer_level()/oxidizer_max() < 0.05:
					fuel_low_led = 1
					
			# now we have the data we want to give the arduino, so we send it:
			pass # not done yet
			input_throttle = 211
			
			# next we need to receive data from the arduino.
			pass #not done yet

	except krpc.error.RPCError as e:
		print("KSP Scene Changed!")
		time.sleep(1)
	except ConnectionAbortedError:
		print("KSP has Disconnected.")
		running = False # we can now end the program.


