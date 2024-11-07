import cv2
import socket

# Socket setup
server_ip = '0.0.0.0'  # Listen on all interfaces
server_port = 5000
buffer_size = 1024

# Initialize the socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)
print(f"Server listening on {server_ip}:{server_port}")

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

streaming = False  # To control the streaming state

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        # Control streaming based on commands
        while True:
            data = client_socket.recv(buffer_size).decode('utf-8')
            if not data:
                break
            
            # Start streaming
            if data.strip().lower() == 'start':
                streaming = True
                print("Starting video stream")

            # Stop streaming
            elif data.strip().lower() == 'stop':
                streaming = False
                print("Stopping video stream")
            
            # Process the streaming state
            if streaming:
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                cv2.imshow('frame', frame)

                # Exit the video stream display
                if cv2.waitKey(1) == ord('q'):
                    break

        client_socket.close()

finally:
    cap.release()
    cv2.destroyAllWindows()
    server_socket.close()

