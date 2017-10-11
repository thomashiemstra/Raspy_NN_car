import socket
from time import sleep

host = '192.168.2.10' #ip of computer
port = 12345


s1 = socket.socket()
s1.connect((host, port))
connection1 = s1.makefile('wb')


sleep(2)

s2 = socket.socket()
s2.connect((host, port))
connection2 = s2.makefile('wb')