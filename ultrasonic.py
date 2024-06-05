"""
<h3>Ce fichier contient une methode qui mesure la distance entre la vehicule et un obstacle.</h3>

<h3>Auteur :  EL-MANANI Fatima </h3>

<h3>Version : 4.0</h3>
"""

import RPi.GPIO as GPIO
import time
import threading

"""
Cette fonction mesure la distance entre le véhicule et un obstacle en utilisant un capteur ultrasonique.
Elle configure les broches TRIG et ECHO du capteur, envoie une impulsion, puis calcule et affiche la distance mesurée en centimètres.
"""

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG1, ECHO1 = 14, 17
TRIG2, ECHO2 = 16, 26
TRIG3, ECHO3 = 12, 6
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

def mesure_distance(TRIG, ECHO):
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def mesure_distance_thread():
    distances = [None, None, None]
    
    def measure_and_store(index, TRIG, ECHO):
        distances[index] = mesure_distance(TRIG, ECHO)

    threads = [
        threading.Thread(target=measure_and_store, args=(0, TRIG1, ECHO1)),
        threading.Thread(target=measure_and_store, args=(1, TRIG2, ECHO2)),
        threading.Thread(target=measure_and_store, args=(2, TRIG3, ECHO3)),
    ]
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return min(distances)

