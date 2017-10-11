import socket
import pickle
import RPi.GPIO as GPIO
from time import sleep
import struct
import picamera
import io


GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.OUT)
left = GPIO.PWM(18,100)
left.start(0)
GPIO.setup(16,GPIO.OUT)
right = GPIO.PWM(16,100)
right.start(0)

GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)	
GPIO.setup(27,GPIO.OUT)	

def set_motors(arr):
    xVal = int(arr[0]) 
    yVal = int(arr[1]) - 492

    
    if(xVal>1000):
        speed = 100
    elif(xVal<1000):
        speed = 0;

    #print(xVal,speed)

    fac = (map(yVal,-492,531,-400,400))/400
    #print(speed,fac)

    if(speed > 0):
        GPIO.output(23, 1)
        GPIO.output(24, 0)
        GPIO.output(17, 1)
        GPIO.output(27, 0)

    if(fac > 0):
        right.ChangeDutyCycle(speed*(1-fac))  
        left.ChangeDutyCycle(speed)    

    if(fac < 0):
        right.ChangeDutyCycle(speed)  
        left.ChangeDutyCycle(speed*(1+fac))    

    if(speed < 0):
        speed = abs(speed)

        GPIO.output(23, 0)
        GPIO.output(24, 1)
        GPIO.output(17, 0)
        GPIO.output(27, 1)

        right.ChangeDutyCycle(speed)  
        left.ChangeDutyCycle(speed)     
		

	
def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
	
if __name__ == "__main__":	
    host = '192.168.2.10' #ip of computer
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    #connection = s.makefile("rb")
    print("hoi")
    try:
        while(True):
            data = s.recv(1024)
            if data:
                L = pickle.loads(data)
                set_motors(L)

                #connection.write(struct.pack('<L', stream.tell()))
                #connection.flush()
                #stream.seek(0)
                #connection.write(stream.read())
                #stream.seek(0)
                #stream.truncate()

                #sleep(0.01)
                #print(L) 

    except KeyboardInterrupt:
        s.close()
        connection.close()
        print("closed")
        GPIO.cleanup()  

    finally:
        s.close()
        connection.close()
        print("closed")
        GPIO.cleanup()  