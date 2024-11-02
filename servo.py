import RPi.GPIO as GPIO
import time

# Setup
servo_pin = 22 # Define the GPIO pin where the servo is connected
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(servo_pin, GPIO.OUT)  # Set the servo pin as an output

# Create a PWM instance
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency
pwm.start(0)  # Start PWM with a duty cycle of 0

def rotate_servo(angle):
    duty_cycle = angle / 18 + 2  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)  # Set the duty cycle to control the angle
    time.sleep(1)  # Wait for the servo to reach the position
    pwm.ChangeDutyCycle(0)  # Stop sending the signal

try:
    rotate_servo(170)
    time.sleep(2)
    rotate_servo(0)# Rotate the servo to 95 degrees
finally:
    pwm.stop()  # Stop PWM
    GPIO.cleanup()  # Clean up GPIO settings

