import socket
import numpy as np
import pyautogui
import cv2
import pickle
import struct
import mss

def send_screen():
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    print(socket.gethostbyname(socket.gethostname()))

    # Accept connection
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")

    # Initialize mss
    sct = mss.mss()
    monitor = sct.monitors[1]

    # Continuous screen sharing
    while True:
        # Capture screen
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)

        # Get cursor position
        cursor_x, cursor_y = pyautogui.position()
        cursor_color = (0, 0, 255)  # Red color for the cursor
        cursor_radius = 7  # Radius of the red dot

        # Draw red dot at the cursor position
        cv2.circle(img, (cursor_x, cursor_y), cursor_radius, cursor_color, -1)

        # Convert image to BGR format
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Compress the image
        _, compressed_frame = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

        # Serialize frame
        data = pickle.dumps(compressed_frame)

        # Send frame size
        client_socket.sendall(struct.pack("L", len(data)) + data)

        # Control frame rate
        cv2.waitKey(30)

# Run the server
send_screen()