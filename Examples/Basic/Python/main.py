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
		arduino = serial.Serial(port=select_port(), baudrate=115200, timeout=1)
		#  careful: if u get the baud number wrong, you will only receive garbage.
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
# The program has successfully started
while running:
	# PROBLEM: If the vessel is destroyed, or we switch to the hangar or anything, we can no longer control it
	#  The Program will then fail.
	# SOLUTION: the "try:" statement
	#  If anything goes wrong inside a "try" block, 
	#  we can continue the program if we "catch" the error in the except clauses.	
	try: 
		if server.krpc.current_game_scene != server.krpc.current_game_scene.flight:
			print("Not in flight scene. Current scene: ", server.krpc.current_game_scene)
			i = 0
			while i < 20 and server.krpc.current_game_scene != server.krpc.current_game_scene.flight:
				i += 1
				time.sleep(1) # KSP is not in flight mode. Wait one second and check again.
			continue  # skip the rest of the loop and check again.

		vessel = server.space_center.active_vessel  # the vessel we are using
		
		# We now tell the server what stuff we want streamed.
		
		# lets say we want to know the status of the solar panels and the oxidizer level.
		
		# there are two types of streams, you have to set them up differently for attributes and functions
		# first for attributes:
		solar_panels = server.add_stream(getattr, vessel.control, "solar_panels")
		'''solar panels are an attribute of the class Control.
		you can find it here in the docs: https://krpc.github.io/krpc/python/api/space-center/control.html
		you will see under solar_panels, that it is an Attribute. 
		because of that the add_stream function has to have gettatr as its first argument. 
		The second argument is the class where our attribute is located.
		Its in the control attribute of our vessel.
		The last argument is the name of the argument, as it is in the docs.'''
		# Just as s a further example apoapsis_altitude looks like this:
		apoapsis_height = server.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
		
		# now for functions:
		has_oxidizer = server.add_stream(vessel.resources.has_resource, "Oxidizer")
		# gives us a stream where we can check if the vessel can store a certain resource.
		# to know this is important because if the oxidizer tank blows up, it will become false.
		# and then our oxidizer_max is zero, and if we divide to get the percentage, we divide by zero and our program aborts.
		'''For functions, as a first argument we give the function. 
		So on the resources page (https://krpc.github.io/krpc/python/api/space-center/resources.html)
		we see at the top that is is of course part of our vessel, because we want the resources of our vessel.
		the function we want is called has_resource(name) and it needs a name.
		to get the names of the resources you can do
		for res in resources.all:
			print (res.name)
		To give a function the attributes it needs, we can just add them as further arguments of add_stream.
		if we wanted to stream a function randomFunc(a, b, c) of our vessel, we would do
		self.con.add_stream(vessel.randomFunc, a, b, c)'''
		oxidizer_level = server.add_stream(vessel.resources.has_resource, "Oxidizer")
		oxidizer_max = server.add_stream(vessel.resources.max, "Oxidizer")
		oxidizer_current = server.add_stream(vessel.resources.amount, "Oxidizer")
			
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
			arduino.write(b's')  # here you can see the weird b before the string.
			arduino.write(str(solar_panel_led).encode(encoding='utf-8', errors='ignore'))
			arduino.write(str(fuel_low_led).encode(encoding='utf-8', errors='ignore'))
			arduino.write(b'\n')
			# This b is because the arduino speaks a different language than python.
			# The Arduino wants "bytes". If we write a string b'Hello World!',
			# Then python encodes it as bytes.
			# we could also do arduino.write('s'.encode('utf-8'))
			# which is the same thing. This is what we are doing with the numbers. We convert them to string first,
			# then we encode them in utf-8. errors='ignore' means just that letters, which are not specified
			# in utf-8 like ä, é, etc. won't abort the program but just be ignored. you can also set it to 'replace'
			# next we need to receive data from the arduino.
			response = arduino.readline()  # now this received is again in the bytes format.
			decoded = response.decode(encoding='utf-8', errors='ignore')  # and we need to translate it for python
			decoded.strip('\n\r')  # we remove special chars which we do not need
			start_location = decoded.find('s')  # we now look where the 's' in the string is.
			if start_location == -1:
				print("not found")
				continue  # if its not there, we have to retry, e.g. just skip the decoding.
			decoded = decoded[(start_location+1):]  # now we delete everything until after the s because we do not need it.
			numbers = decoded.split(';')  # numbers is now a list of 3 numbers as strings example: ['1','0','135','127']
			# if anything went wong, we might not get 3 elements in the list.
			# so we must make sure we have initialised all variables anyway.
			button2_state = 0
			analog1_state = 0
			analog2_state = 0
			button1_state = int(numbers[0])  # we use this as brakes
			if len(numbers) > 1:
				button2_state = int(numbers[1])  # and this for light
			if len(numbers) > 2:
				analog1_state = int(numbers[2])  # this for yaw
			if len(numbers) > 3:
				analog2_state = int(numbers[3])  # and this for pitch
			print(button1_state, '  ', button2_state, '  ', analog1_state, '  ', analog2_state)

			# now we need to send this data to ksp
			control = server.space_center.active_vessel.control  # this is where we write to to change things in ksp
			control.brakes = bool(button1_state)
			control.lights = bool(button2_state)
			control.yaw = analog1_state/1024 - 0.5
			control.pitch = analog2_state/1024 - 0.5

	except krpc.error.RPCError as e:
		print("KSP Scene Changed!")
		time.sleep(1)
	except ConnectionAbortedError:
		print("KSP has Disconnected")
		running = False  # we can now end the program.


