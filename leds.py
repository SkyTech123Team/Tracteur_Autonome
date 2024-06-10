"""
<h3>Ce fichier contient les differentes signales  possibles que peut effectuer la véhicule à savoir celle de droite, gauche et de stop.</h3>


<h3>Auteurs : AIT ALI M'HAMED SAÂDIA </h3>


<h3>Version : 1.0</h3>
"""

import RPi.GPIO as GPIO
import time

# Numérotation des broches (pins) en mode BCM
GPIO.setmode(GPIO.BCM)

# Définir le pin 3 comme sortie
GPIO.cleanup()

GPIO.setup(19, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

try:
    while True:
        # Allumer la LED
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(9, GPIO.HIGH)
        time.sleep(1)  # Attendre 1 seconde
        # Éteindre la LED
        GPIO.output(19, GPIO.LOW)
        GPIO.output(3, GPIO.LOW)
        GPIO.output(9, GPIO.LOW)
        time.sleep(1)  # Attendre 1 seconde
except KeyboardInterrupt:
    pass

# Nettoyer les GPIO
GPIO.cleanup()


