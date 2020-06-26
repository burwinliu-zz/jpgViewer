import pickle
import struct

import cv2
import zmq
import base64
import numpy as np
import socket


HOST = "127.0.0.1"
PORT = 8000

CASCPATH = "../opencv-4.3.0/data/haarcascades/haarcascade_frontalface_alt.xml"
FILE_WRITE_PATH = "../connections.json"
FACE_CASC = cv2.CascadeClassifier(CASCPATH)


def recieve_connection(connection, buf_size):
    pass


def worker():
    pass


def init_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST, PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn, addr = s.accept()

    data = b''
    payload_size = struct.calcsize("L")

    while True:

        # Retrieve message size
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)

        # Display
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = FACE_CASC.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    init_server()
