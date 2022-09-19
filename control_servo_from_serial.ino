
#include <Servo.h>
#include <SoftwareSerial.h>

#define sample_size 10
#define num_servo 5

Servo myservo_1;  // create servo object to control a servo
Servo myservo_2;  // create servo object to control a servo
Servo myservo_3;  // create servo object to control a servo

int INDEX[num_servo];
int VALUE[num_servo];
int SUM[num_servo];
int Reading[num_servo];
int READINGS[sample_size];
int AVERAGED[num_servo];

int val_1 = 0;
String incomingByte[6];
float a,b,c,d,e,f;
int servo_val[num_servo];
  
void setup() {
  myservo_1.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo_2.attach(10);
  myservo_3.attach(11);
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(LED_BUILTIN, OUTPUT);
}


void loop() {

  if (Serial.available() > 0) {
    // read the incoming byte:
    //Serial.print("recieved data: ");
    for (int i = 0; i <= num_servo ; i++)
    {
      incomingByte[i] = Serial.readStringUntil(',');
      //Serial.print(incomingByte[i]);
      //Serial.print(", ");
      delay(100);
    }
    delay(45);
    myservo_1.write(incomingByte[0].toInt());
    delay(45);
    myservo_2.write(incomingByte[1].toInt()); // sets the servo position according to the scaled value
    delay(45);
    myservo_3.write(incomingByte[2].toInt()); // sets the servo position according to the scaled value
    delay(45);                           // waits for the servo to get there
  }
}
