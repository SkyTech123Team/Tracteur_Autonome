from flask import Flask, request, jsonify
from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import os

"""
<h3> Ce fichier contient la partie de liaison de l'application mobile avec le véhicule.</h3>

<h3>Auteurs : SAFRANI Fatima Ezzahra & EL-MANANI Fatima </h3>

<h3>Version : 1.0</h3>
"""

app = Flask(__name__)

# Fonction pour recevoir et enregistrer l'image depuis l'application Android

@app.route('/uploadImage', methods=['POST'])
def upload_image():
    """
    Cette fonction permet de télécharger une image envoyée par une application mobile
    """
    if request.method == 'POST':
        if 'image' in request.files:
            image_file = request.files['image']
            process_image(image_file)  # Appeler la fonction de traitement d'image directement
            return "Image received and processed successfully."
        else:
            return "No image file received."

# Fonction pour traiter l'image
def process_image(image_path):
    """
    Cette fonction permet d'extraire les dimensions à partir d'une image envoyée par une application mobile
    """
    # Lire l'image et prétraiter
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image.")
        return {"error": "Failed to load image."}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    edged = cv2.Canny(blur, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # Trouver les contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Trier les contours de gauche à droite car le contour le plus à gauche est l'objet de référence
    (cnts, _) = contours.sort_contours(cnts)

    # Supprimer les contours qui ne sont pas assez grands
    cnts = [x for x in cnts if cv2.contourArea(x) > 500]

    if len(cnts) == 0:
        print("Aucun contour suffisant trouvé.")
        return {"error": "Aucun contour suffisant trouvé."}

    # Dimensions de l'objet de référence (par exemple, un carré de 2cm x 2cm)
    ref_object = cnts[0]
    box = cv2.minAreaRect(ref_object)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    (tl, tr, br, bl) = box
    dist_in_pixel = euclidean(tl, tr)
    dist_in_cm = 17  # Ajustez cette valeur selon les dimensions de votre objet de référence
    pixel_per_cm = dist_in_pixel / dist_in_cm

    # Calculer les dimensions de l'image entière en centimètres
    image_width_cm = image.shape[1] / pixel_per_cm
    image_height_cm = image.shape[0] / pixel_per_cm

    # Afficher les dimensions de l'image entière
    print("Dimensions de l'image (largeur x hauteur) : {:.2f}cm x {:.2f}cm".format(image_width_cm, image_height_cm))

    # Retourner les dimensions
    return {
        "image_width_cm": image_width_cm,
        "image_height_cm": image_height_cm
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
