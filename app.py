import json
import time
from flask import Flask, jsonify, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configure the GPIO pin for MQ4 sensor
SENSOR_PIN = 17  # GPIO pin connected to MQ4 sensor's data output
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Store sensor values globally
sensor_values = []

# Serve the main page (index)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/database')
def database():
    return render_template('database.html')  # Ensure you have this template

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

# Retrieve sensor data
@app.route('/sensor-data')
def get_sensor_data():
    try:
        sensor_value = GPIO.input(SENSOR_PIN)  # Read data from MQ4 sensor
        sensor_values.append(sensor_value)  # Store the value
        return jsonify({'sensor_value': sensor_value, 'sensor_values': sensor_values})
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
