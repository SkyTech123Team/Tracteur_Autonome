import RPi.GPIO as GPIO
import time
"""
<h3>Ce fichier contient les differentes mouvements possibles qu'on peut effectuer avec la vehicule.</h3>


<h3>Auteur : ABDOU Ali </h3>


<h3>Version : 1.0</h3>
"""

from time import sleep
import methods 
import threading
import ultrasonic

speed = 1

# Main loop
try:
    print("Ready for commands (d-move, e-exit):")
    while True:
        command = input()
        if command == 'd':
            distance = float(input("Type distance to go (cm): "))
            total_time = distance / speed
            methods.move_forward_distance(total_time)
        elif command == 'e':
            print("Exiting")
            stop_thread = True
            break
        elif  command == 'm':
            methods.monter_bras()
        elif  command == 'l':
            methods.descendre_bras()
        else:
            print("Invalid command. Try again.")
except KeyboardInterrupt:
    print("Program stopped by User")
finally:
    GPIO.cleanup()
    stop_thread = True
    print("GPIO Clean up")
    

