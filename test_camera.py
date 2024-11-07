import cv2

# Test with video0
camera_index = 0  # Change this to 1 if 0 doesn't work
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print(f"Error: Could not open camera {camera_index}")
else:
    print(f"Camera {camera_index} opened successfully.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break
        cv2.imshow(f'Camera {camera_index}', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

