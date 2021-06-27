#include <ros.h>
#include <math.h>
#include <std_msgs/Float32.h>
#include "std_msgs/Int16MultiArray.h"
#include <Servo.h>

Servo Myservo;
int pos = 0;


const int Input1 = 10;
const int Input2 = 11;
const int Input3 = 9;
const int Input4 = 3;
const int Enable12 = 4;
const int Enable34 = 7;
const int servo = 5;
int c1=0,c2=0,c3=0,c4=0;

ros::NodeHandle nh;


void Motordriver( const std_msgs::Int16MultiArray &Md)
{
  c1=Md.data[0];
  c3=Md.data[1];
  c2=Md.data[2];
  c4=Md.data[3];

  if(c4==1)
  {
    if(c1 == 0)
    {
      digitalWrite(Input2,HIGH);
      digitalWrite(Input1,HIGH);
      digitalWrite(Input3,HIGH);
      digitalWrite(Input4,HIGH);
      if(c3 == -1)
        {
          digitalWrite(Input2,LOW);
          digitalWrite(Input1,HIGH);
          digitalWrite(Input3,HIGH);
          digitalWrite(Input4,LOW); 
       
        }
      else if (c3 == 1)
        {
          digitalWrite(Input2,HIGH);
          digitalWrite(Input1,LOW);
          digitalWrite(Input3,LOW);
          digitalWrite(Input4,HIGH);  
        }
      else
      {
          if(c2 == 1)
          {
            Myservo.write(pos);
            pos+=5;
          }
          else
          {
           Myservo.write(pos);
           pos-=5;
          }
          
      }
    
    }
    else if(c1 == 1)
    {
      digitalWrite(Input2,HIGH);
      digitalWrite(Input1,LOW);
      digitalWrite(Input3,HIGH);
      digitalWrite(Input4,LOW); 
    } 
    else if(c1 == -1)
    {
      digitalWrite(Input2,LOW);
      digitalWrite(Input1,HIGH);
      digitalWrite(Input3,LOW);
      digitalWrite(Input4,HIGH);  
    }
  
   
  }
}

ros::Subscriber <std_msgs::Int16MultiArray> NodeXY("TopicArr",&Motordriver);


void setup() {
  
  nh.initNode();

  Myservo.attach(servo);
  pinMode(Enable12,OUTPUT);
  pinMode(Enable34,OUTPUT);
  digitalWrite(Enable12,HIGH);
  digitalWrite(Enable34,HIGH);
  pinMode(Input1, OUTPUT);
  pinMode(Input2, OUTPUT);
  pinMode(Input3, OUTPUT);
  pinMode(Input4, OUTPUT); 

  nh.subscribe(NodeXY);
  
}

void loop() 
{

 nh.spinOnce();

 delay(1000);
}
