import pickle
import struct

import cv2
import base64
import numpy as np
import socket
from threading import Thread


HOST = "127.0.0.1"
PORT = 8000

CASCPATH = "../opencv-4.3.0/data/haarcascades/haarcascade_frontalface_alt.xml"
FILE_WRITE_PATH = "../connections.json"
FACE_CASC = cv2.CascadeClassifier(CASCPATH)
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCKET.bind((HOST, PORT))

THREADS = []


class ClientWorker(Thread):
    def __init__(self, host, port, conn):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = SOCKET
        self.conn = conn

    def run(self):
        # Retrieve message size
        data = b''
        payload_size = struct.calcsize("L")

        while True:
            data += self.conn.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += self.conn.recv(4096)

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


def init_server():

    while True:
        SOCKET.listen(10)
        print('Socket now listening')

        conn, (ip, port) = SOCKET.accept()
        new_thread = ClientWorker(ip, port, conn)
        new_thread.start()
        THREADS.append(new_thread)


if __name__ == '__main__':
    init_server()
