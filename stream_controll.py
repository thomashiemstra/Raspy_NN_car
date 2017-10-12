import socket
import cv2
import numpy as np
import struct
from PIL import Image
import io
import serial
import pickle
from threading import Thread
from time import sleep

#constanly updates the member variable "frame" and returns it when read() is called
class WebcamVideoStream:
    def __init__(self):
        self.stopped = False
        self.loop = True
        self.ready = False
        self.new = False # signals if the frame is updated
    
    def start(self, connection):
        Thread(target=self.update, args=(connection,)).start()
        return self
    
    #recieve the video stream and turn it into a cv2 object
    def update(self, connection):
        print(connection)
        try:
            while True:
                if self.stopped:
                    break
                
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                pil_image = Image.open(image_stream)
                self.frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                self.ready = True
                self.new = True
        except:
            pass
            
        self.loop = False
        connection.close()
        cv2.destroyAllWindows() 
        print("closed")
    
    def read(self):
        return self.frame


def host_connections():
    serial_connection = serial.Serial("COM8",115200)
    
    host = '192.168.2.10' #ip of computer
    port = 8000
    
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    
    # start the video streaming connection and start the video streaming processing thread
    video_connection = server_socket.accept()[0].makefile('rb')
    
    # start the connection that sends controlls to the car
    controll_connection, addr = server_socket.accept()
    print("got connection from",addr)
    return video_connection, controll_connection, serial_connection

def send_commands(connection, ser):
    data = [0,0]
    
    ser.flushInput()
    tempX = ser.read(2)
    tempY = ser.read(2)
    data[0] = struct.unpack('h',tempX)[0]
    data[1] = struct.unpack('h',tempY)[0]
    data_string = pickle.dumps(data)
    connection.send(data_string)


if __name__ == "__main__":	

    video_connection, controll_connection, serial_connection = host_connections()
    
    stream = WebcamVideoStream().start(video_connection)
    
    try:
        while stream.loop:
            if(stream.ready):
                image = stream.read()
                cv2.imshow('image',image)
                cv2.waitKey(1)     
                stream.new = False
                
            send_commands(controll_connection, serial_connection)
            sleep(0.01)
            
    except KeyboardInterrupt:
        pass
    
    finally:
        stream.stopped = True
        cv2.destroyAllWindows() 
        controll_connection.close()
        video_connection.close()
        serial_connection.close()

