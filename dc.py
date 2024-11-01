import RPi.GPIO as GPIO
import time

# Setup
relay_pin = 8  # GPIO pin connected to the relay

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(relay_pin, GPIO.OUT)  # Set the relay pin as output

def turn_motor_on():
    GPIO.output(relay_pin, GPIO.HIGH)  # Turn the relay on (motor ON)

def turn_motor_off():
    GPIO.output(relay_pin, GPIO.LOW)  # Turn the relay off (motor OFF)

try:
    # Turn the motor on
    turn_motor_on()
    print("Motor is ON")
    time.sleep(10)  # Run the motor for 10 seconds

    # Turn the motor off
    turn_motor_off()
    print("Motor is OFF")

finally:
    GPIO.cleanup()  # Clean up GPIO settings

