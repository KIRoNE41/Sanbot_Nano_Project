#include "MotorMove.h"
#include <Arduino.h>
#include "Hand_robot.h"

Hand_robot handLeft = Hand_robot(30, 31, 32, 5, LEFT);
Hand_robot handRight = Hand_robot(34, 35, 39, 6, RIGHT);

MotorMove motor = MotorMove();

int chan1 = 3;
int chan2 = 2;
int Channel1;
int Channel2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
  motor.Begin();

  pinMode(chan1, INPUT);
  pinMode(chan2, INPUT);

  handLeft.begin();
  handRight.begin();
}

void FSI6(int x){
  int joyspeed = x;
  Channel1 = (pulseIn(chan1,HIGH));
  Channel2 = (pulseIn(chan2,HIGH));
        
        if (Channel2 > 1000 && Channel2 < 1900){
          motor.MoveStop();
        }
        if (Channel1 > 1000 && Channel1 < 1900){
          motor.MoveStop();
        }

        if (Channel1 > 1900 ){
          motor.MoveForward(joyspeed);
          delay(100);
        }

        if (Channel1 < 1000){
          motor.MoveBackward(joyspeed);
          delay(100);
        }

        if (Channel2 < 1000){
          motor.TurnLeft(joyspeed);
        }

        if (Channel2 > 1900){
         motor.TurnRight(joyspeed);
        }

}

void py(){
  static String value1;
  static int value2;
  static char SerialBuffer[10];
  static char SerialData;
  static byte SerialState = 0;
  static byte SerialIndex = 0;
  
  if(Serial.available()){

    SerialData = Serial.read();  
    switch(SerialState){    
    
      case 0: if(SerialData=='#'){
                SerialState = 1; 
                SerialIndex = 0;
              }
              break;
              
      case 1: if(SerialData==':'){
                SerialBuffer[SerialIndex] = '\0';
                value1 = String(SerialBuffer);
                SerialIndex = 0;
                SerialState = 2;  
                
              }else{
                SerialBuffer[SerialIndex] = SerialData;
                if(++SerialIndex==10){
                  SerialState = 0;
                }
              }
              break;
              
      case 2: if(SerialData==';'){
                SerialBuffer[SerialIndex] = '\0';
                value2 = atoi(SerialBuffer);
                control(value1,value2);
                Serial.print("Rx receive direction: ");
                Serial.print(value1);
                Serial.print(" speed: ");
                Serial.println(value2);
                SerialState = 0;
              }else{
                SerialBuffer[SerialIndex] = SerialData;
                if(++SerialIndex==10){
                  SerialState = 0;
                }  
              }
              break;
    }  
  }
}
void control(String value_input1,int value_input2){

  String direction = value_input1;
  int speed = value_input2;

  if(direction=="Forward"){

    Serial.print("Forward Action!!");
    motor.MoveForward(speed);

  }

  else if(direction=="Backward"){
    
    Serial.print("Backward Action!!"); 
    motor.MoveBackward(speed);
    
  }

  else if(direction=="Stop"){
    motor.MoveStop();
    Serial.print("Stop Action!!");
  }

  else if(direction=="TrunRight"){
    motor.TurnRight(speed);
    Serial.print("TrunRight Action!!");
  }

  else if(direction=="TrunLeft"){
    motor.TurnLeft(speed);
    Serial.print("TrunLeft Action!!");
  }

  else if(direction=="Joystick"){
    FSI6(speed);
    Serial.print("Joystick Action!!");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
py();
}
