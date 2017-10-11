import socket
import cv2
import numpy as np
import struct
from PIL import Image
import io
from threading import Thread
from time import sleep
import os

class WebcamVideoStream:
    def __init__(self):
        self.stopped = False
        self.loop = True
        self.ready = False
        self.new = False # signals if frame is updated
    
    def start(self, connection):

        Thread(target=self.update, args=(connection,)).start()
        return self
    
    def update(self, connection):
        print(connection)
        try:
            while True:
                if self.stopped:
                    return
                
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
            print("error")
            
        self.loop = False
        connection.close()
        cv2.destroyAllWindows() 
        print("closed")
    
    def read(self):
        return self.frame

    

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.2.10', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')


stream = WebcamVideoStream().start(connection)
i=0

f = open("test.txt","a")

try:
    while stream.loop:
        if(stream.ready and stream.new):
            image = stream.read()
            
            cv2.imshow('image',image)
            cv2.imwrite("IMG/test%d.jpg" %i,image)
            i +=1
            path = os.path.abspath("IMG/test%d.jpg, %d \n" %(i,2*i))
            f.write(path)
            
            cv2.waitKey(1)     
            stream.new = False
        
except KeyboardInterrupt:
    pass

finally:
    cv2.destroyAllWindows() 
    connection.close()
    f.close()
