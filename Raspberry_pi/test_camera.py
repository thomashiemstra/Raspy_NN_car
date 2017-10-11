import io
import socket
import struct
import time
import picamera
import threading

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.2.10', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')

def send_image(connection):
    with picamera.PiCamera() as camera:
        #camera.resolution = (640, 480)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        camera.vflip = True
        camera.hflip = True
        camera.framerate = 10
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
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

run_event = threading.Event()
run_event.set()

t = threading.Thread(target=send_image, args=(connection,))
t.start()

time.sleep(10)
run_event.clear()

t.join()
print("done")
