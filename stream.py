import socket
import cv2
import numpy as np
import struct
from PIL import Image
import io

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.2.10', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

start,stop = 0,0

print("hoi")
try:
    while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
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
            opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            cv2.imshow('image',opencvImage)
            cv2.waitKey(1)
            
        
        
except KeyboardInterrupt:
    pass

except:
    print("error")
    pass

finally:
    connection.close()
    server_socket.close()
    cv2.destroyAllWindows() 
    print("closed")