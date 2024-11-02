from picamera import PiCamera
from time import sleep

camera = PiCamera()

try:
    camera.start_preview()
    sleep(5)  # Preview for 5 seconds
    camera.capture('/home/pi/image.jpg')  # Capture an image
    print("Image captured!")
finally:
    camera.stop_preview()

