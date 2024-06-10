"""
<h3> Ce fichier contient la partie de liaison de l'application mobile avec la vehicule.</h3>


<h3>Auteurs : AIT ALI MHAMED SAADIA & SAFRANI Fatima Ezzahra & EL-MANANI Fatima </h3>


<h3>Version : 2.1</h3>

"""
from flask import Flask, render_template,Response ,request, jsonify

import io
import picamera
from time import sleep
import methods 

app = Flask(__name__)

@app.route('/up')
def bras_up():
    """
    Cette fonction permet de faire monter la charrue
    """
    methods.monter_bras()
    return 'Charrue monter'

@app.route('/down')
def bras_down():
    """
    Cette fonction permet de faire decsendre la charrue
    """
    methods.descendre_bras()
    return 'Charrue decsender'



@app.route('/move_forward')
def move_backward():
    """
    Cette fonction permet de faire une mauvement vers l'arrier
    """
    methods.backward()
    return 'Moving backward'





@app.route('/move_backward')
def move_forward():
    """
    Cette fonction permet de faire une mauvement vers l'avant
    """
    #forward()
    methods.forward()
    return 'Moving forward'



@app.route('/move_right')
def move_right():
    """
    Cette fonction permet de tourner a droite de 180 degree 
    """
    methods.turnRight()
    return 'Turning right'


@app.route('/move_left')
def move_left():
    """
    Cette fonction permet de tourner a gauche de 180 degree 
    """
    methods.turnLeft()
    return 'Turning left'


@app.route('/video_feed')
def video_feed():
    """
    Cette fonction permet au user de suivre les mauvements du tracteur a l qide du camera 
    """
    return Response(methods.generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/stop')
def stop():
    """
    Cette fonction permet de faire stopper la vehicule
    """
    methods.stopCar()
    methods.monter_bras()
    return 'Stopping'



@app.route('/sendInfo', methods=['POST'])
def cover_rectangle():
    """
    Cette fonction permet de couvrir un rectangle en donnant les dimensions recus a partir de l application mobile
    """
    if request.method == 'POST':
        data = request.json
        if data is None:
            return abort(400, description="No data provided.")

        length = data.get('height')
        width = data.get('width')

        # Check if necessary parameters are present and are of correct type
        if length is None or width is None:
            return abort(400, description="Missing 'height' or 'width' parameters.")

        try:
            length = float(length)  # Ensure length is a float (in case it's a decimal)
            width = float(width)  # Ensure width is a float (in case it's a decimal)
            pass_width = 10  # Width of each pass, adjust based on your tractor's effective width

            number_of_passes = int(width / pass_width)
        except ValueError:
            return abort(400, description="Invalid 'height' or 'width'. Must be a number.")

        for pass_num in range(number_of_passes):
            # Move forward the full length of the rectangle
            methods.move_forward_distance(length)
            # Turn around 180 degrees to come back
            methods.turnRight()
            sleep(1)  # Short delay to stabilize after turn
            methods.turnRight()
            sleep(1)  # Short delay to stabilize after turn

            # Move forward the full length of the rectangle
            methods.move_forward_distance(length)

            # Prepare for the next pass, if there's more area to cover
            if pass_num < number_of_passes - 1:
                # Turn 90 degrees to the right to align for the next pass
                methods.turnRight()
                sleep(1)  # Short delay to stabilize after turn
                # Move forward the width of one pass
                methods.move_forward_distance(pass_width)
                # Turn 90 degrees to the right again to realign for the next length pass
                methods.turnRight()
                sleep(1)  # Short delay to stabilize after turn

        # Return a response to the client
        return jsonify({'message': 'Operation successful'})

if __name__ == '__main__' :
    app.run(host='0.0.0.0' , port=5001,threaded=True)
