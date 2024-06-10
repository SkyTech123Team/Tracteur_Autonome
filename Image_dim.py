from flask import Flask, request
from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

"""
<h3> Ce fichier contient la partie de liaison de l'application mobile avec la vehicule.</h3>


<h3>Auteurs : SAFRANI Fatima Ezzahra & EL-MANANI Fatima </h3>


<h3>Version : 1.0</h3>

"""
app = Flask(__name__)

# Fonction pour recevoir et enregistrer l'image depuis l'application Android
@app.route('/uploadImage', methods=['POST'])
def upload_image():
    """
    Cette fonction permet de faire telecharger une image envoyee avec une application mobile
    """
    if request.method == 'POST':
        if 'image' in request.files:
            image_file = request.files['image']
            image_path = "/home/pi/Desktop/enregistree.jpg"
            image_file.save(image_path)
            process_image(image_path)  # Appeler la fonction de traitement d'image
            return "Image received and processed successfully."
        else:
            return "No image file received."

# Fonction pour traiter l'image
def process_image(image_path):
    """
    Cette fonction permet de faire extraire les dimensions a partir d une image envoyee avec une application mobile
    """
    # Read image and preprocess
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    edged = cv2.Canny(blur, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Sort contours from left to right as leftmost contour is reference object
    (cnts, _) = contours.sort_contours(cnts)

    # Remove contours which are not large enough
    cnts = [x for x in cnts if cv2.contourArea(x) > 500]

    # Reference object dimensions
    # Here for reference I have used a 17cm x 17cm square
    ref_object = cnts[0]
    box = cv2.minAreaRect(ref_object)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    (tl, tr, br, bl) = box
    dist_in_pixel = euclidean(tl, tr)
    dist_in_cm = 17
    pixel_per_cm = dist_in_pixel/dist_in_cm

    # Calculate the dimensions of the entire image in centimeters
    image_width_cm = image.shape[1] / pixel_per_cm
    image_height_cm = image.shape[0] / pixel_per_cm

    # Print the dimensions of the entire image
    print("Image dimensions (width x height): {:.2f}cm x {:.2f}cm".format(image_width_cm, image_height_cm))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)