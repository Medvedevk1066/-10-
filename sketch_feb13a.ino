
#include <Stepper.h>
#include <Servo.h>
 
Servo servo1; 
Servo servo2;
Servo servo3;
Servo servo4;

Stepper Nema(stepsPerRevolution, motorPin1, motorPin2, motorPin3, motorPin4);

const int stepsPerRevolution = 200;
const int motorPin1 = 4;
const int motorPin2 = 5;
const int motorPin3 = 6;
const int motorPin4 = 7; 
const int h = 5;
const int a = 15;
String msg;
int Yprev = 0;

int calculateAngles(int x, int h, int a) { 
  int v = acos((2 * a * a - h * h - x * x) / (2 * a * a)) * 180 / PI;
  int w = atan(x / h) * 180 / PI;
  int g1 = 180 - (180 - v) / 2 - w;  
  int g2 = v - 90;
  int g3 = w - (180 - v) / 2;
 
  return g1, g2, g3; 
} 

int stepsToGo(int y){
  double len = PI * 1.2;
  double rev = y / len;
  int steps = rev * 200;
  return steps;
}
 
void setup(){
  servo1.attach(9);
  servo2.attach(10);
  servo3.attach(11);
  servo4.attach(12);
  Nema.setSpeed(60);
  Serial.begin(9600);
} 
 
void loop() { 
  String X = "", Y = "";
  int g1, g2, g3, steps, x, y, msgN = 0; 

  servo1.write(0); 
  servo2.write(90);
  servo3.write(0);
  
  if(Serial.available()){
    char in = Serial.read();
    while(in != ';'){
      if (!(in == '\n' || in == '\r')){
        if(in == ','){
          msgN ++;
        }
        else if(msgN == 1){
          Y = Y + String(in);
        }
        else if(msgN == 2){
          X = X + String(in);
        }
        else if(msgN == 3){
          if(in == '^'){
            servo4.write(45);
            msgN = 4;
          }
          else{
            servo4.write(0);
            msgN = 4;
          }
        }
      }
    in = Serial.read();
   }
 if(msgN == 4){
  x = X.toInt();
  y = Y.toInt();
  X = "";
  Y = "";
  
  steps = stepsToGo(y - Yprev);
  Nema.step(steps);

  Yprev = y;
   
  g1, g2, g3 = calculateAngles(x, h, a); 
    
  servo1.write(g1); 
  servo2.write(g2);
  servo3.write(g3); 

   msgN = 0;
 }
 } 
}
