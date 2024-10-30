import json
import time
from flask import Flask, jsonify, render_template
try:
    import RPi.GPIO as GPIO
    import Adafruit_DHT
except (ImportError, RuntimeError):
    print("RPi.GPIO or Adafruit_DHT not found. Using Mock GPIO for testing.")
    from unittest import mock
    GPIO = mock.Mock()
    Adafruit_DHT = mock.Mock()

app = Flask(__name__)

# Configure the GPIO pin for MQ4 sensor and DHT11 sensor
MQ4_SENSOR_PIN = 17  # GPIO pin connected to MQ4 sensor's data output
DHT_SENSOR_PIN = 4   # GPIO pin connected to DHT11 sensor's data output
DHT_SENSOR_TYPE = Adafruit_DHT.DHT11  # Specify DHT11 sensor type

GPIO.setmode(GPIO.BCM)
GPIO.setup(MQ4_SENSOR_PIN, GPIO.IN)

# Store sensor values globally
sensor_values = []

# Serve the main page (index)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/database')
def database():
    return render_template('database.html')

# Serve experiment page
@app.route('/experiment')
def experiment():
    return render_template('experiment.html')

# Serve gas sensor page
@app.route('/gas')
def gas_test():
    return render_template('gas.html')

@app.route('/humidity')
def humidity():
    return render_template('humidity.html')

# Retrieve sensor data for both MQ4 and DHT11
@app.route('/sensor-data')
def get_sensor_data():
    try:
        # Read methane data from MQ4 sensor
        mq4_value = GPIO.input(MQ4_SENSOR_PIN)
        
        # Read humidity and temperature data from DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR_TYPE, DHT_SENSOR_PIN)

        # Check if the reading from the DHT11 sensor was successful
        if humidity is not None and temperature is not None:
            sensor_values.append({
                'mq4_value': mq4_value,
                'humidity': humidity,
                'temperature': temperature
            })
            return jsonify({
                'mq4_value': mq4_value,
                'humidity': humidity,
                'temperature': temperature,
                'sensor_values': sensor_values
            })
        else:
            return jsonify({'error': 'Failed to retrieve data from DHT11 sensor'}), 503

    except Exception as e:
        return jsonify({'error': f'Error reading sensor data: {e}'}), 503

# Serve the results page
@app.route('/results')
def results():
    return render_template('results.html', data=sensor_values)  # Pass data to results page

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        GPIO.cleanup()  # Clean up GPIO settings on exit

