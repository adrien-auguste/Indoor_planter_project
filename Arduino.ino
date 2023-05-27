

#include <Wire.h>

int soil_moisture;
//Pins assignment
int red = 13;
int orange = 12;
int green = 11;
// s is used to read the communication from the Raspberry Pi
char s;
void setup() {
    Serial.begin(9600);
    Wire.begin(0x8);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
    pinMode(red,OUTPUT);
    pinMode(orange, OUTPUT);
    pinMode(green, OUTPUT);
    digitalWrite(red, LOW);
    digitalWrite(orange, LOW);
    digitalWrite(green, LOW);
}
void receiveEvent(int howMany){
//Reads the data sent from the Raspberry PI
    while (Wire.available()){
        s = Wire.read();  
    }
}

void loop() {
   

    initialise_values();
     if (s == 0){
       //RED LED
        digitalWrite(red, HIGH);
    
        digitalWrite(orange, LOW);
    
        digitalWrite(green, LOW); 
    }
    else if( s == 1){
      //GREN LED
        digitalWrite(red, LOW);
    
        digitalWrite(orange, LOW);
    
        digitalWrite(green, HIGH);
    }
    else if(s==2){
      //ORANGE LED
        digitalWrite(red, LOW);
    
        digitalWrite(orange, HIGH);
    
        digitalWrite(green, LOW);
    }
  


}
void initialise_values(){
  //reads soil moisture level lowest is 0 and highest is 500.
  delay(2000);
  soil_moisture = analogRead(1);
  //Reads the input value on the serial monitor
  Serial.println(soil_moisture);
}
void requestEvent() {
    //Data sent between 0 to 100
    //Data is a percentage of the soil moisture level 
    int data = 0.20 * soil_moisture;
    Serial.println(data);
    //Send out data value to the Raspberry Pi
    Wire.write(data);       
       
}
