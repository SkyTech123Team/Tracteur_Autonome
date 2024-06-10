"""
<h3> Ce fichier contient le code qui permet de faire controler le mauvement de la charrue</h3>


<h3>Auteurs : SAFRANI Fatima Ezzahra</h3>


<h3>Version : 1.1</h3>

"""

import RPi.GPIO as GPIO
from time import sleep

# Donner le pins avec lesquels le microservo est lie

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)# donner un pin a partir du board du raspberry pi
GPIO.setup(21, GPIO.OUT)  
p = GPIO.PWM(21, 50)# le pin 12 c est lui qui est responssable sur le signal
p.start(0)


def monter_bras():
    """
    Cette fonction permet de monter la bras du microservo
    """
    p.ChangeDutyCycle(3)  # Position pour monter le bras
    sleep(1)  # Attendre 1 seconde
    p.ChangeDutyCycle(0)  # Arreter le servo après le mouvement
    sleep(1)  # Attendre 1 seconde

def descendre_bras():
    """
    Cette fonction permet de descendre la bras du microservo
    """
    p.ChangeDutyCycle(12)  # Position pour descendre le bras
    sleep(1)  # Attendre 1 seconde
    p.ChangeDutyCycle(0)  # Arrêter le servo après le mouvement
    sleep(1)  # Attendre 1 seconde

try:
    while True:
        commande = input("Entrez la commande (monter ou descendre): ")
        if commande == "m":
            monter_bras()
        elif commande == "d":
            descendre_bras()
        else:
            print("Commande invalide. Entrez monter ou descendre.")

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()