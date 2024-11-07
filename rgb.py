import cv2

# Function to display RGB values and the coordinates of the pixel clicked
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the BGR values from the image
        b, g, r = img[y, x]
        # Convert to RGB format (since OpenCV uses BGR)
        print(f"Coordinates: ({x}, {y}), RGB Values: ({r}, {g}, {b})")

        # Display the coordinates and RGB values on the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"RGB: ({r}, {g}, {b})"
        cv2.putText(img, text, (x, y), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Captured Image', img)

# Open the webcam (0 is usually the default webcam, use 1 or higher for external cameras)
cap = cv2.VideoCapture(1)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Capture a single frame from the webcam
ret, img = cap.read()

# Release the webcam
cap.release()

# Check if frame was captured
if not ret:
    print("Error: Failed to capture image")
    exit()

x, y = 315, 222  # Replace with your target coordinates

# Get the BGR values at the specified coordinates
(b, g, r) = img[y, x]

# Convert to RGB format
rgb = (r, g, b)
print(f"RGB at ({x}, {y}): {rgb}")
font = cv2.FONT_HERSHEY_SIMPLEX
text = f"RGB: ({r}, {g}, {b})"
cv2.putText(img, text, (x, y), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#cv2.imshow('Captured Image', img)

# Create a window and bind the click event to it
cv2.imshow('Captured Image', img)
cv2.setMouseCallback('Captured Image', click_event)

# Display the image until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()
