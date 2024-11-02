import RPi.GPIO as GPIO
import dht11
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
DHT_PIN = 4             # Pin where the DHT11 sensor is connected

# Initialize the DHT11 instance
sensor = dht11.DHT11(pin=DHT_PIN)

try:
    # Reading from DHT11 sensor
    result = sensor.read()
    if result.is_valid():
        print(f'Temperature: {result.temperature} °C, Humidity: {result.humidity} %')
    else:
        print('Failed to retrieve data from humidity sensor')
finally:
    GPIO.cleanup()

