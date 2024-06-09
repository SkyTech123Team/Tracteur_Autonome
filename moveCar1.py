"""
<h3>Ce fichier contient les differentes mouvements possibles qu'on peut effectuer avec la vehicule.</h3>


<h3>Auteurs : SAFRANI Fatima Ezzahra & EL-MANANI Fatima & ABDOU Ali.</h3>


<h3>Version : 3.0</h3>
"""


import RPi.GPIO as GPIO
import time
from time import sleep


GPIO.setwarnings(False)
# Configuration des broches GPIO pour les moteurs
in1 = 24
in2 = 23
en = 5
in3 = 22
in4 = 27
en_a = 18
temp1=1

#Initialisation de la bibliothèque GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(en_a,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(in3,GPIO.LOW)
GPIO.setup(in4,GPIO.LOW)

p=GPIO.PWM(en,1000)
p_a=GPIO.PWM(en_a,1000)
p.start(25)
p_a.start(18)

p.ChangeDutyCycle(10)
p_a.ChangeDutyCycle(10)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")
print("ggh")



def forward():
    """
    Cette fonction permet de faire une mauvement vers l'avant
    """
    print("forward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    temp1=1
    x='z'



def backward():
    """
    Cette fonction permet de faire une mauvement vers l'arrier
    """
    print("backward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    temp1=0
    x='z'
    
    

def stopCar():
    """
    Cette fonction permet de faire stopper la vehicule
    """
    print("stop")
    
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    signalStop()
    x='z'
    


def slowDownCar():
    """
    Cette fonction permet de faire reduire la vitesse de la vehicule
    """
    print("low")
    p.ChangeDutyCycle(25)
    x='z'
    
    

def speedUpCar():
    """
    Cette fonction permet de faire augmenter la vitesse de la vehicule
    """
    print("high")
    p.ChangeDutyCycle(75)
    p_a.ChangeDutyCycle(75)
    x='z'
    
    

def mediumUpCar():
    """
    Cette fonction permet de faire mettre la vitesse de la vehicule en medium
    """
    print("medium")
    p.ChangeDutyCycle(50)
    x='z'

def signalRight():
    for _ in range(3):
        GPIO.output(3, GPIO.HIGH)  # Allumer le signal de droite
        time.sleep(0.5)            # Attendre 0.5 seconde
        GPIO.output(3, GPIO.LOW)   # Éteindre le signal de droite
        time.sleep(0.5)            # Attendre 0.5 seconde

def signalLeft():
    for _ in range(3):
        GPIO.output(19, GPIO.HIGH)  # Allumer le signal de gauche
        time.sleep(0.5)             # Attendre 0.5 seconde
        GPIO.output(19, GPIO.LOW)   # Éteindre le signal de gauche
        time.sleep(0.5)             # Attendre 0.5 seconde

def signalStop():
    for _ in range(3):
        GPIO.output(9, GPIO.HIGH)  # Allumer le signal de stop
        time.sleep(0.5)            # Attendre 0.5 seconde
        GPIO.output(9, GPIO.LOW)   # Éteindre le signal de stop
        time.sleep(0.5) 

def turnRight180():
    """
    Cette fonction permet de tourner a droite de 180 degree 
    """
    print("right 180")
    GPIO.output(in1, GPIO.LOW)  # Avancer moteur gauche
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)  # Reculer moteur droit
    GPIO.output(in4, GPIO.LOW)
    signalRight()
    time.sleep(0.642)
    stopCar()
    forward()
    
    

def turnLeft180():
    """
    Cette fonction permet de tourner a gauche de 180 degree 
    """
    print("Left 180")
    
    GPIO.output(in1, GPIO.HIGH)  # Reculer moteur gauche
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)  # Avancer moteur droit 
    GPIO.output(in4, GPIO.HIGH)
    signalLeft()
    #temp1 = 1
    #x = 'z'
    time.sleep(0.642)
    #temp1 = 1
    stopCar()
    forward()
    
#cette boucle permet de tester toutes les methodes definies en haut en se basant sur la valeur entree par utilisateur.   
while(1):

    x=input()
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
         print("backward")
         x='z'
    elif x=='s':
        stopCar()
    elif x=='f':
        forward()
    elif x=='rt':
        turnRight()
    elif x=='tf':
        turnLetf()
    elif x=='b':
        backward()
    elif x=='l':
        slowDownCar()
    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'
    elif x=='h':
        speedUpCar()
    elif x=='t':
        testMove()
    elif x=='tur':
        turnRight180()
    elif x=='tul':
        turnLeft180()
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
        
        
        
        
"""
def testMove():
    print("test")
    forward()
    sleep(5)
    turnLetf()
    sleep(6)
    stopCar()"""
"""#this function allows to turn the car right
def turnRight():
    print("right")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    temp1=1
    x='z'
#this function allows to turn the car left
def turnLetf():
    print("left")
    #GPIO.output(in1,GPIO.LOW)
    #GPIO.output(in2,GPIO.HIGH)
    #GPIO.output(in3,GPIO.LOW)
    #GPIO.output(in4,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    temp1=1
    x='z'"""