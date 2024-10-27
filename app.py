import serial
import json
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Serial connection setup
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Update with your serial port if needed
except serial.SerialException as e:
    ser = None
    print(f"Error opening serial port: {e}")

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

# Serve gas sensor page and read sensor data
@app.route('/gas')
def gas_test():
    return render_template('gas.html')

# Retrieve sensor data
@app.route('/sensor-data')
def get_sensor_data():
    if ser and ser.in_waiting > 0:
        sensor_value = ser.readline().decode('utf-8').strip()  # Read data from Arduino
        sensor_values.append(float(sensor_value))  # Store the value
        return jsonify({'sensor_value': sensor_value, 'sensor_values': sensor_values})
    else:
        return jsonify({'error': 'No data available'}), 503

# Serve the results page
@app.route('/results')
def results():
    return render_template('results.html', data=sensor_values)  # Pass data to results page

if __name__ == '__main__':
    app.run(debug=True)
