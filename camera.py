import cv2

cap = cv2.VideoCapture(1)  # Using index 2, since the device is /dev/video2

if not cap.isOpened():
    print("Error: Could not open Pi Camera on /dev/video0`.")
else:
    print("Pi Camera opened successfully on /dev/video0.")
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Pi Camera Feed", frame)
        cv2.waitKey(0)
    else:
        print("Failed to capture image from Pi Camera.")
    
    cap.release()
    cv2.destroyAllWindows()

