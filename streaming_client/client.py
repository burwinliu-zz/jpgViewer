import pickle
import struct
import time

import cv2

import socket


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000        # The port used by the server


def init_client():
    frame_rate = 10
    prev = 0

    cap = cv2.VideoCapture(0)
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))

    while True:
        time_elapsed = time.time() - prev
        if time_elapsed > 1. / frame_rate:
            prev = time.time()

            ret, frame = cap.read()
            # Serialize frame
            data = pickle.dumps(frame)

            # Send message length first
            message_size = struct.pack("L", len(data))

            # Then data
            clientsocket.sendall(message_size + data)


if __name__ == "__main__":
    init_client()