import base64
import time

import cv2
import zmq

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')

camera = cv2.VideoCapture(0)  # init the camera

frame_rate = 15
prev = 0

while True:
    time_elapsed = time.time() - prev
    res, image = camera.read()

    if time_elapsed > 1. / frame_rate:
        try:
            grabbed, frame = camera.read()  # grab the current frame
            frame = cv2.resize(frame, (640, 480))  # resize the frame
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)

        except KeyboardInterrupt:
            camera.release()
            cv2.destroyAllWindows()
            break
