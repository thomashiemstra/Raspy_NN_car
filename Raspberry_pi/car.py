import io
import socket
import struct
import time
import picamera
import threading
import pickle
import RPi.GPIO as GPIO
from time import sleep

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

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
    
def set_motors(arr):
    speed = int(arr[0]) 
    steering = int(arr[1]) - 492

    fac = (map(steering,-492,531,-400,400))/400
    if(fac>1):
        fac = 1
    if(fac<-1):
        fac = -1
    
    if(speed >= 0):
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

        if(fac > 0):
            right.ChangeDutyCycle(speed*(1-fac))  
            left.ChangeDutyCycle(speed)    

        if(fac < 0):
            right.ChangeDutyCycle(speed)  
            left.ChangeDutyCycle(speed*(1+fac))              

def image_stream(connection):
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        camera.vflip = True
        camera.hflip = True
        camera.framerate = 10
        time.sleep(2)

        # Note the start time and construct a stream to hold image data temporarily
        start = time.time()
        stream = io.BytesIO()
       
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()
            if(not run_event.is_set()):
                break
    # Write a length of zero to the stream to signal we're done and shut everything down
    connection.write(struct.pack('<L', 0))
    connection.close()
    client_socket.close()
    print("closed")

def setup_connections():
    host = '192.168.2.10' #ip of computer
    port = 8000
    
    #video stream
    client_socket = socket.socket()
    client_socket.connect((host, port))
    video_connection = client_socket.makefile('wb')

    sleep(1)
    #controll stream
    controll_connection = socket.socket()
    controll_connection.connect((host, port))
    print("we are connected!")
    return video_connection, controll_connection
    
if __name__ == "__main__":	
    #to gracefully exit the threads (AKA KILL THEM!)
    run_event = threading.Event()
    run_event.set()
    
    video_connection, controll_connection = setup_connections()
    
    #spawn a thread to send images
    t = threading.Thread(target=image_stream, args=(video_connection,))
    t.start()
   
    try:
        while(True):
            data = controll_connection.recv(1024)
            if data:
                L = pickle.loads(data)
                set_motors(L)
                #print(L) 
            sleep(0.001)

    except KeyboardInterrupt:
        pass

    finally:
        run_event.clear()
        t.join()
        video_connection.close()
        controll_connection.close()
        GPIO.cleanup()  
        print("He's dead Jim!")