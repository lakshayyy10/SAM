import RPi.GPIO as GPIO
import time

# Pin setup
relay_pin = 4 # GPIO pin connected to Relay 4

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin-numbering
GPIO.setup(relay_pin, GPIO.OUT)  # Set relay pin as output

try:
    # Turn the motor ON
    GPIO.output(relay_pin, GPIO.LOW)  # Activate the relay (turn on the motor)
    print("Motor is ON")
    time.sleep(5)  # Run for 5 seconds

    # Turn the motor OFF
    GPIO.output(relay_pin, GPIO.HIGH)   # Deactivate the relay (turn off the motor)
    print("Motor is OFF")
    time.sleep(2)  # Wait for 2 seconds

finally:
    GPIO.cleanup()  # Clean up GPIO settings

