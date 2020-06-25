import cv2
import zmq
import base64
import numpy as np
import sys

if __name__ == '__main__':
    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)
    footage_socket.bind('tcp://*:5555')
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    cascPath = "../opencv-4.3.0/data/haarcascades/haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    while True:
        try:
            frame = footage_socket.recv_string()
            img = base64.b64decode(frame)
            npimg = np.frombuffer(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(source, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Stream", source)
            cv2.waitKey(1)

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break
