import socket
import numpy as np
import cv2
import pickle
import struct
import pyautogui


def receive_screen():
    host = input("host: ")
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((host, port))
    print("Connected to server")

    # Receiving loop
    data = b""
    payload_size = struct.calcsize("L")

    while True:
        # Retrieve message size
        while len(data) < payload_size:
            data += client_socket.recv(4096)
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize frame
        frame = pickle.loads(frame_data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Display frame
        cv2.imshow("Remote Screen", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Close connection
    cv2.destroyAllWindows()
    


# Run the client
receive_screen()