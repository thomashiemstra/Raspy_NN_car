import socket



def host():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	host = '192.168.2.10' #ip of computer
	port = 12345
	s.bind((host, port))

	s.listen(2)
	return s

server_socket = host()

connection1 = server_socket.accept()[0].makefile('rb')


connection2 = server_socket.accept()



