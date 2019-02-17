#define button1_pin 4
#define button2_pin 5
#define led1_pin 6
#define led2_pin 7
#define analog1_pin A0
#define analog2_pin A1



void setup(){
  //Start serial communication
  Serial.begin(115200 );
  //setting pin Modes
  pinMode(button1_pin, INPUT);
  pinMode(button2_pin, INPUT);
  pinMode(led1_pin, OUTPUT);
  pinMode(led2_pin, OUTPUT);
  pinMode(analog1_pin, INPUT);
  pinMode(analog2_pin, INPUT);
}

void loop(){
  //
  if (Serial.available() > 0){ //we have input
  //incoming messages look like this: 
  //{'s', 'led1_state', led2_state'}
    if (Serial.read() == 's')
    { //we have detected the starting character
      if (Serial.read() == '1') // '1' represents on
      {
        digitalWrite(led1_pin, HIGH); //set the led state to on
      }
      else
      {
        digitalWrite(led1_pin, LOW); //set the led state to off
      }
      if (Serial.read() == '1'); //same for the second led
      {
        digitalWrite(led2_pin, HIGH); 
      }
      else
      {
        digitalWrite(led2_pin, LOW); 
      }
      //outgoing messages look like this
	  //{'s', 'button1_state', 'button2_state', 'a', 'analog1_state', 'a', 'analog2_state', '\n'}
      Serial.print('s'); //send the starting character
	  button1_state = digitalRead(button1_pin); //reading wether the button is pressed or not
	  //sending that value
      Serial.print(button1_state);
	  //same with the next
	  button2_state = digitalRead(button2_pin);
	  Serial.print(button2_state);
	  
	  //the analog inputs range from 0 to 255, so they are not always the same ammount of digits, 
	  //so we need to know where they start and end, therefore we send an a before and betwen, 
	  //and a newline char at the very end of the message
	  Serial.print('a');
	  analog1_state = analog_read(analog1_pin);
	  Serial.print(analog1_state);
	  Serial.print('a');
	  analog2_state = analog_read(analog2_pin);
	  Serial.println(analog2_state); //println also sends a newline char at the end of the message.  
    }
  }
}