"""
<h3> Ce fichier contient les differentes mouvements possibles qu'on peut effectuer avec la
vehecule afin de la lie avec la camera .</h3>


<h3>Auteurs : EL-MANANI Fatima </h3>


<h3>Version : 2.0</h3>

"""

import RPi.GPIO as GPIO
from time import sleep
import io
import picamera
import microservo


# Define GPIO pins
in1 = 24
in2 = 23
en = 5
in3 = 22
in4 = 27
en_a = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)

# Ensure all pins are low at startup
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

# PWM setup
p = GPIO.PWM(en, 1000)
p_a = GPIO.PWM(en_a, 1000)
p.start(25)
p_a.start(25)

# Control functions
def forward():
    """
    Cette fonction permet de faire une mauvement vers l'avant
    """
    print("forward")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
def backward():
    """
    Cette fonction permet de faire une mauvement vers l'arrier
    """
    print("backward")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def stopCar():
    """
    Cette fonction permet de faire stopper le tracteur
    """
    print("stop")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    microservo.monter_bras()

def turnRight():
    """
    Cette fonction permet de faire un tour a droite
    """
    print("right")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def generate_frames():
    try :
        with picamera.PiCamera() as camera :
            camera.resolution = (640,480)
            camera.framerate = 24
            stream = io.BytesIO()
            
            for _ in camera.capture_continuous(stream,'jpeg',use_video_port=True):
                stream.seek(0)
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
                stream.seek(0)
                stream.truncate()
    except Exception as e:
        print(f"An error occurred: {e}")

def turnLeft():
    """
    Cette fonction permet de faire un tour a gauche
    """
    print("left")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def move_forward_distance(distance_cm):
    """
    Cette fonction permet de faire une mauvement vers l'avant avec certaine distance
    """
    # Constants
    wheel_circumference = 18.85  # calculated circumference
    time_per_cm = 0.2  # This needs calibration: measure time for known distance

    # Calculate total time to move the requested distance
    total_time = distance_cm * time_per_cm

    # Start moving forward
    forward()

    # Sleep while moving
    sleep(total_time)

    # Stop the car
    stopCar()