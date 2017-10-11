int x,y;

uint8_t bytesX[2];
uint8_t bytesY[2];

void setup(){
  Serial.begin(115200); 
}

void loop(){

    x = analogRead(A0);
    y = analogRead(A1);
//    Serial.print(x); Serial.print("\t"); Serial.println(y);

    bytesX[1] = (x >> 8) &0xff;
    bytesX[0] = x & 0xff;    

    bytesY[1] = (y >> 8) &0xff;
    bytesY[0] = y & 0xff;    

    Serial.write(bytesX,2);
    Serial.write(bytesY,2);
}
