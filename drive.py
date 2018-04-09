# -*- encoding: utf-8 -*-
import socket
import cv2
import numpy as np
import struct
from PIL import Image
import io
import pickle
import utils
from threading import Thread, Lock
from time import sleep
from keras.models import load_model

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

frame_lock = Lock()

#constanly updates the member variable "frame" and returns it when read() is called
class WebcamVideoStream:
    def __init__(self):
        self.stopped = False
        self.loop = True
        self.ready = False
    
    def start(self, connection):
        Thread(target=self.update, args=(connection,)).start()
        return self
    
    #recieve the video stream and turn it into a cv2 object
    def update(self, connection):
        print(connection)
        mtx, dist = utils.load_config()
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
                image = np.asarray(pil_image)
                
#                self.disp = utils.birds_eye(image, mtx, dist)
                
                image = utils.preprocess(image, mtx, dist)
                image = np.array([image])
                
                
                
                with frame_lock:
                    self.disp = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                    self.frame = image
                self.ready = True
                sleep(0.01)
        except:
            pass
            
        self.loop = False
        connection.close()
        cv2.destroyAllWindows() 
        print("closed")
    
    def read(self):
        with frame_lock:
            return self.frame, self.disp


def host_connections():
    host = '192.168.2.5' #ip of computer
    port = 8000
    
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    
    # start the video streaming connection 
    video_connection = server_socket.accept()[0].makefile('rb')
    
    # start the connection that sends controlls to the car
    controll_connection, addr = server_socket.accept()
    print("got connection from",addr)
    return video_connection, controll_connection

def send_commands(connection, speed, fac):
    data = [0,0]
    
    data[0] = speed
    data[1] = fac

    data_string = pickle.dumps(data)
    connection.send(data_string)
    

if __name__ == "__main__":	

    model = load_model("model-017.h5")
    print("ready")
    video_connection, controll_connection = host_connections()
    stream = WebcamVideoStream().start(video_connection)
    
    try:
        while stream.loop:
            if(stream.ready):

                image, disp = stream.read()
                steering_angle = float(model.predict(image, batch_size=1))
                send_commands(controll_connection, 100, steering_angle)                
                cv2.namedWindow('image',cv2.WINDOW_NORMAL)
                cv2.resizeWindow('image', 960,720)
                cv2.imshow('image',disp)
                cv2.waitKey(1)  
                
            sleep(0.01)
            
    except KeyboardInterrupt:
        pass
    
    finally:
        stream.stopped = True
        cv2.destroyAllWindows() 
        controll_connection.close()
        video_connection.close()
