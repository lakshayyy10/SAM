import json
import cv2
from flask import Flask, jsonify, render_template, Response
from datetime import datetime
import os
import time
import RPi.GPIO as GPIO
import dht11
from flask_socketio import SocketIO, emit
app = Flask(__name__)

socketio = SocketIO(app)

@socketio.on('update_event')
def handle_update(data):
    emit('update_event', data, broadcast=True)

# Directories for saving data and images
IMAGE_DIR = "captured_images"
DATA_DIR = "test_results"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

cam_1 = cv2.VideoCapture(0)  # Camera 1 for images
cam_2 = cv2.VideoCapture(1)  # Camera 2 for live feed

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GAS_SENSOR_PIN = 17 # GPIO pin connected to MQ4 sensor's data output
DHT_PIN = 4  # GPIO pin connected to DHT11 data pin
sensor = dht11.DHT11(pin=DHT_PIN)

STEPPER_DIR_PIN = 2
STEPPER_STEP_PIN = 5
SERVO_PINS = [22, 26, 23, 24,25]  # Define pins for each servo

# Initialize stepper motor pins
GPIO.setup(STEPPER_DIR_PIN, GPIO.OUT)
GPIO.setup(STEPPER_STEP_PIN, GPIO.OUT)
GPIO.setup(GAS_SENSOR_PIN, GPIO.IN)

# Initialize servo motors
servo_pwms = []
for pin in SERVO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50 Hz for servo
    pwm.start(0)  # Start with 0 duty cycle
    servo_pwms.append(pwm)

current = 0

# Helper functions
def rotate_stepper(target):
    
    global current
    degrees = target - current
    steps = int(degrees / 1.8)  # Adjust based on step angle
    if degrees > 0:
        GPIO.output(STEPPER_DIR_PIN, GPIO.HIGH)
    else:
        GPIO.output(STEPPER_DIR_PIN, GPIO.LOW)
    for _ in range(steps):
        GPIO.output(STEPPER_STEP_PIN, GPIO.HIGH)
        time.sleep(0.001)  # Control speed of rotation
        GPIO.output(STEPPER_STEP_PIN, GPIO.LOW)
        time.sleep(0.001)
    current = target

def rotate_servo(servo_index, angle):
    duty_cycle = 2 + (angle / 18)  # Calculate duty cycle for angle
    servo_pwms[servo_index].ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # Hold for rotation
    servo_pwms[servo_index].ChangeDutyCycle(0)

def rotate_stepper_then_servo(stepper_degrees, servo_index, servo_angle):
    rotate_stepper(stepper_degrees)  # Rotate stepper motor
    time.sleep(0.5)  # Ensure stepper finishes before servo starts
    rotate_servo(servo_index, servo_angle)      # Rotate servo

def capture_image(test_name):
    ret, frame = cam_1.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(IMAGE_DIR, f"{test_name}_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        return image_path
    return None

def save_test_data(test_name, data):
    json_path = os.path.join(DATA_DIR, f"{test_name}.json")
    with open(json_path, "w") as f:
        json.dump(data, f)

# Routes for each test
@app.route('/ph')
def ph_test():
    rotate_stepper_then_servo(0, 0, 95)  # Stepper movement then servo rotationi
    rotate_servo(4,170)
    time.sleep(4)
    rotate_servo(4,2)
    image_path = capture_image("ph_test")
    data = {
        'test_name': 'pH',
        'timestamp': datetime.now().isoformat(),
        'image_path': image_path
    }
    save_test_data("ph_test", data)
    return render_template('video.html', test_name='pH Test', data=data)

@app.route('/texture')
def texture_test():
    rotate_stepper_then_servo(72, 1, 95)
    image_path = capture_image("texture_test")
    data = {
        'test_name': 'Texture',
        'timestamp': datetime.now().isoformat(),
        'image_path': image_path
    }
    save_test_data("texture_test", data)
    return render_template('video.html', test_name='Texture Test', data=data)

@app.route('/catalase')
def catalase_test():
    rotate_stepper_then_servo(144, 2, 95)
    image_path = capture_image("catalase_test")
    data = {
        'test_name': 'Catalase',
        'timestamp': datetime.now().isoformat(),
        'image_path': image_path
    }
    save_test_data("catalase_test", data)
    return render_template('video.html', test_name='Catalase Test', data=data)

@app.route('/carbonate')
def carbonate_test():
    rotate_stepper_then_servo(216, 3, 95)
    image_path = capture_image("carbonate_test")
    data = {
        'test_name': 'Carbonate',
        'timestamp': datetime.now().isoformat(),
        'image_path': image_path
    }
    save_test_data("carbonate_test", data)
    return render_template('video.html', test_name='Carbonate Test', data=data)

@app.route('/spectroscopy')
def spectroscopy_test():
    rotate_stepper_then_servo(288, 3, 95)
    image_path = capture_image("spectroscopy_test")
    data = {
        'test_name': 'LED Spectroscopy',
        'timestamp': datetime.now().isoformat(),
        'image_path': image_path
    }
    save_test_data("spectroscopy_test", data)
    return render_template('video.html', test_name='Spectroscopy Test', data=data)

# Route for live camera feed (Camera 2)
def gen():
    while True:
        success, frame = cam_2.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# HTML templates for rendering
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/database')
def database():
    return render_template('database.html')

@app.route('/experiment')
def experiment():
    return render_template('experiment.html')

@app.route('/video')
def video():
    return render_template('video.html')


@app.route('/humidity')
def humidity():
    # Read DHT11 sensor data
    result= sensor.read()
    

    if result.is_valid():
        sensor_data = {
            'temperature': result.temperature,
            'humidity': result.humidity
        }
    else:
        sensor_data = {
            'error': 'Failed to read from DHT11 sensor',
            'temperature': None,
            'humidity': None
        }

    return render_template('humidity.html', sensor_data=sensor_data)

@app.route('/gas')
def gas():
    # Read gas sensor digital threshold
    gas_detected = GPIO.input(GAS_SENSOR_PIN)

    if gas_detected is not None:
        gas_data = {
            'gas': "Detected" if gas_detected else "Not Detected"
        }
    else:
        gas_data = {
            'error': 'Failed to read from gas sensor',
            'gas': None
        }

    return render_template('gas.html', gas_data=gas_data)

@app.route('/collect_soil')
def collect_soil():
    return render_template('collect_soil.html')
    
@app.route('/results')
def results():
    # Load test results from JSON files for display
    results_data = {}
    for test_name in ["ph_test", "texture_test", "catalase_test", "carbonate_test", "spectroscopy_test"]:
        json_path = os.path.join(DATA_DIR, f"{test_name}.json")
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                results_data[test_name] = json.load(f)
    return render_template('results.html', data=results_data)

if __name__ == '__main__':
    try:
        socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    finally:
        GPIO.cleanup()  # Ensure GPIO pins are released after the app stops
