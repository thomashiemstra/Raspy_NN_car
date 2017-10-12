import serial
from time import sleep
import struct
import socket
import pickle
import cv2
import numpy as np
from PIL import Image

import io

ser = serial.Serial("COM8",115200)
sleep(2)
data = [0,0]


def host():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	host = '192.168.2.10' #ip of computer
	port = 12345
	s.bind((host, port))

	s.listen(2)
	return s

#server_socket = host()
#c, addr = server_socket.accept()
#print("got connection from",addr)


try:
    while( True):
        ser.flushInput()
        tempX = ser.read(2)
        tempY = ser.read(2)
        data[0] = struct.unpack('h',tempX)[0]
        data[1] = struct.unpack('h',tempY)[0]
        print(data)
#        data_string = pickle.dumps(data)
#        c.send(data_string)r
        sleep(0.01)
        
except KeyboardInterrupt:
    ser.close()   

finally:
    ser.close()       
 



