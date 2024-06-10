"""
<h3> Ce fichier contient les differentes mouvements possibles qu'on peut effectuer avec la
vehecule afin de la lie avec la camera ainsi toutes les signales de la vehecule.</h3>


<h3>Auteurs : EL-MANANI Fatima & ABDOU Ali & SAFRANI Fatima Ezzahra & AIT ALI MHAMED SAADIA</h3>


<h3>Version : 3.0</h3>

"""

import RPi.GPIO as GPIO
import time
from time import sleep
import picamera
import io
import methods 
import threading
import ultrasonic

# Define GPIO pins
in1 = 24
in2 = 23
en = 5
in3 = 22
in4 = 27
en_a = 18

# Global variables
iwtssb = 0 
stop_thread = False
remaining_time = 0
start_time = time.time()
elapsed_time = 0
stop = True
i = 1
direction  = "l"
condition = threading.Condition()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Ensure all pins are low at startup
pins = [in1, in2, in3, in4, en, en_a, 3, 19, 9, 21]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# PWM setup
try:
    p = GPIO.PWM(en, 1000)
    p_a = GPIO.PWM(en_a, 1000)
    q = GPIO.PWM(21, 50)  # Ensure pin 21 is not already in use
except RuntimeError as e:
    print(f"PWM setup error: {e}")
else:
    p.start(25)
    p_a.start(25)
    q.start(0)

def monter_bras():
    """
    Cette fonction permet de monter le bras du microservo
    """
    q.ChangeDutyCycle(3)  # Position pour monter le bras
    sleep(1)  # Attendre 1 seconde
    q.ChangeDutyCycle(0)  # Arrêter le servo après le mouvement
    sleep(1)  # Attendre 1 seconde

def descendre_bras():
    """
    Cette fonction permet de descendre le bras du microservo
    """
    q.ChangeDutyCycle(12)  # Position pour descendre le bras
    sleep(1)  # Attendre 1 seconde
    q.ChangeDutyCycle(0)  # Arrêter le servo après le mouvement
    sleep(1)  # Attendre 1 seconde

# Control functions
def backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def stopCar():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    signalStop()

def turnRight():
    signalRight()
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def turnLeft():
    signalLeft()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def signalRight():
    for _ in range(4):
        GPIO.output(3, GPIO.HIGH)  # Allumer le signal de droite
        time.sleep(0.5)            # Attendre 0.5 seconde
        GPIO.output(3, GPIO.LOW)   # Éteindre le signal de droite
        time.sleep(0.5)            # Attendre 0.5 seconde

def signalLeft():
    for _ in range(4):
        GPIO.output(19, GPIO.HIGH)  # Allumer le signal de gauche
        time.sleep(0.5)             # Attendre 0.5 seconde
        GPIO.output(19, GPIO.LOW)   # Éteindre le signal de gauche
        time.sleep(0.5)             # Attendre 0.5 seconde

def signalStop():
    for _ in range(4):
        GPIO.output(9, GPIO.HIGH)  # Allumer le signal de stop
        time.sleep(0.5)            # Attendre 0.5 seconde
        GPIO.output(9, GPIO.LOW)   # Éteindre le signal de stop
        time.sleep(0.5) 

def slowDownCar():
    """
    Cette fonction permet de faire ralentir le tracteur
    """
    print("low")
    p.ChangeDutyCycle(25)
    p_a.ChangeDutyCycle(25)

def speedUpCar():
    """
    Cette fonction permet de faire avancer la vitesse du tracteur
    """
    print("high")
    p.ChangeDutyCycle(75)
    p_a.ChangeDutyCycle(75)

def mediumUpCar():
    print("medium")
    p.ChangeDutyCycle(50)
    p_a.ChangeDutyCycle(50)

def turnLeft90(t):
    """
    Cette fonction permet de tourner a gauche de 90 degree 
    """
    GPIO.output(in1, GPIO.HIGH)  # Reculer moteur gauche
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)  # Avancer moteur droit 
    GPIO.output(in4, GPIO.HIGH)
    #used to be 0.28
    time.sleep(t)
    stopCar()

def turnRight90():
    """
    Cette fonction permet de tourner a droite de 90 degree 
    """
    GPIO.output(in1, GPIO.LOW)  # Avancer moteur gauche
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)  # Reculer moteur droit
    GPIO.output(in4, GPIO.LOW)
    time.sleep(0.82)
    stopCar()

def continuous_measure():
    """
    Cette methode permet de recuper la valeurs retourner par les capteurs :
    -Si un obstacle est detecte :
        1-Voiture en train de rouler : 'notify' la voiture pour arreter et met a jour le temps restant pour arriver
        a la destination qui va etre utiliser pour reprendre une fois l'obstacle 'is cleared '?
        2-Sinon , le programme continue a tester les valeurs recues
    -Une fois l'obstacle n'est plus present, la fonction 'notify' la voiture pour reprendre son chemin
    """
    global stop, remaining_time, start_time, elapsed_time
    while not stop_thread:
        distance = ultrasonic.mesure_distance_thread()
        if distance < 20:
            if not stop:
                elapsed_time = time.time() - start_time
                remaining_time = remaining_time - elapsed_time
                stopCar()
                with condition:
                    stop = True
                    condition.notify_all()
        else:
            with condition:
                stop = False

distance_thread = threading.Thread(target=continuous_measure)
distance_thread.start()

def right():
    turnRight90()
    forward()
    sleep(0.25)
    stopCar()
    sleep(0.5)
    turnRight90()
    stopCar()

def left():
    turnLeft90(0.56)
    forward()
    sleep(0.25)
    stopCar()
    sleep(0.5)
    turnLeft90(0.56)
    stopCar()

def lsb():
    """
    Cette methode controle les mouvements de la voiture selon la presence d'un obstacle  
    """
    global stop, remaining_time, start_time, direction, iwtssb, i
    while not stop_thread:
        with condition:
            while stop:
                condition.wait(1)
            if remaining_time > 0:
                cover()
                if remaining_time <= 0:
                    if direction == "l":
                        left()
                        direction = "l"
                    else:
                        right()
                        direction = "l"

move_thread = threading.Thread(target=lsb)
move_thread.start()

def move_forward_distance(total_time):
    """
    Cette fonction permet de faire une mauvement a partir d une distance donnee
    """
    global remaining_time, iwtssb
    iwtssb = total_time
    remaining_time = total_time

def cover():
    global remaining_time, start_time
    start_time = time.time()
    forward()
    condition.wait(remaining_time)
    stopCar()
    elapsed_time = time.time() - start_time
    remaining_time -= elapsed_time
    sleep(0.5)

def cover_rectangle(length, width):
    """
    Cette fonction permet de faire couvrir un rectangle en donnant ces dimensions
    """
    pass_width = 1  # Width of each pass, adjust based on your tractor's effective width
    number_of_passes = int(width / pass_width)

    for pass_num in range(number_of_passes):
        # Move forward the full length of the rectangle
        move_forward_distance(length)
        # Turn around 180 degrees to come back
        turnRight()
        sleep(1)  # Short delay to stabilize after turn
        turnRight()
        sleep(1)  # Short delay to stabilize after turn

        # Move forward the full length of the rectangle
        move_forward_distance(length)

        # Prepare for the next pass, if there's more area to cover
        if pass_num < number_of_passes - 1:
            # Turn 90 degrees to the right to move over for the next pass
            turnRight()
            sleep(1)  # Short delay to stabilize after turn
            # Move forward the width of one pass
            move_forward_distance(pass_width)
            # Turn 90 degrees to the left to align with the next pass
            turnLeft()
            sleep(1)  # Short delay to stabilize after turn

