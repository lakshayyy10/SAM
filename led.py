import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

try:
    GPIO.output(17,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(17,GPIO.LOW)
    time.sleep(2)
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()