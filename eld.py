import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)

try:
    GPIO.output(27,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(27,GPIO.LOW)
    time.sleep(2)
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()