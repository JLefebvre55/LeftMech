/*
    Controlling a servo position using a potentiometer (variable resistor)
    by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

    modified on 8 Nov 2013
    by Scott Fitzgerald
    http://www.arduino.cc/en/Tutorial/Knob
*/

#include <Servo.h>

Servo myservo;  

//Pins for our objects
const int potpin = A0;  
const int servopin = 9;

//Minimum and maximum values for our objects
const int potmax = 1023;
const int potmin = 0;
const int servomin = 180;
const int servomax = 0;

int val = -1;    // variable to read the value from the analog pin

void setup() {
    myservo.attach(servopin);  // attaches the servo on pin 9 to the servo object
    Serial.begin(9600);
}

void loop() {
    // reads the value of the potentiometer (value between 0 and 1023)
    val = analogRead(potpin);
    Serial.print("Potentiometer = ");
    Serial.println(val);

    // scale it to use it with the servo (value between 0 and 180)
    val = map(val, potmin, potmax, servomin, servomax);     
    myservo.write(val);                  // sets the servo position according to the scaled value
    delay(15);                           // waits for the servo to get there
}
