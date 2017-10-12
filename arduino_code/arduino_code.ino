int steering, forward, backward;
int direction;

uint8_t bytesX[2];
uint8_t bytesY[2];

void setup(){
  Serial.begin(115200); 
}

void loop(){

    steering = analogRead(A0);
    forward = analogRead(A1);
    backward = analogRead(A2);
     
    direction = 0;  
    if(forward > 1000 && backward < 1000){
        direction = 100;
    }

    if(backward > 1000 && forward < 1000){
        direction = -100;
    }
    
    bytesX[1] = (direction >> 8) &0xff;
    bytesX[0] = direction & 0xff;    

    bytesY[1] = (steering >> 8) &0xff;
    bytesY[0] = steering & 0xff;    

    Serial.write(bytesX,2);
    Serial.write(bytesY,2);
}
