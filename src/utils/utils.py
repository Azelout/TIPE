import numpy as np
from os import listdir
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import matplotlib.pyplot as plt
from config import config
import cv2

from os.path import dirname, abspath
path = dirname(abspath(__file__))

size = (config["model"]["input_shape"], config["model"]["input_shape"])

# Charger et redimensionner une image et son masque
def load_image_mask(image_path, mask_path, target_size=size):
    # Charger l'image et le masque
    image = load_img(image_path, target_size=target_size)
    mask = load_img(mask_path, target_size=target_size, color_mode="grayscale")

    # Convertir en tableaux NumPy
    image = img_to_array(image) / 255.0  # Normaliser les pixels avec des valeurs entre 0 et 1 pour chaque pixel
    mask = img_to_array(mask) / 255.0  # Masque binaire

    # Appliquer un seuil pour binariser le masque
    mask = (mask > 0.5).astype(np.uint8)  # Masque binaire avec des valeurs 0 ou 1

    return image, mask


# Charger le dataset
def load_images(target_size=(size, size)):
    images = []
    masks = []

    # Boucle sur tous les fichiers de masque
    print("Chargement des images")
    i = 0
    for nom_fichier in listdir(f"{path}/../../{config['data']['train']}/"):
        if nom_fichier.endswith(".png"):  # Vérifier l'extension du fichier. Si c'est un png alors c'est un masque
            i += 1
            # Charger l'image et son masque correspondant
            image_path = f"{path}/../../{config['data']['train']}/" + nom_fichier.replace(".png", ".jpg")
            mask_path = f"{path}/../../{config['data']['train']}/" + nom_fichier

            image, mask = load_image_mask(image_path, mask_path, target_size)

            images.append(image)
            masks.append(mask)
    print(i, " images chargées avec masque")

    # Convertir les listes en tableaux NumPy
    images = np.array(images)
    masks = np.array(masks)

    return images, masks

def show_model_stats(history):
    # Tracer la courbe de la perte
    plt.plot(history.history['loss'], label='Perte d\'entraînement')
    plt.plot(history.history['val_loss'], label='Perte de validation')
    plt.xlabel('Époques')
    plt.ylabel('Perte')
    plt.legend()
    plt.show()

    # Tracer la courbe de la précision (si elle est calculée)
    if 'accuracy' in history.history:
        plt.plot(history.history['accuracy'], label='Précision sur le dataset d\'entraînement')
        plt.plot(history.history['val_accuracy'], label='Précision sur le dataset de validation')
        plt.xlabel('Époques')
        plt.ylabel('Précision')
        plt.legend()
        plt.show()

def get_centroid_from_mask(mask):
    """
    Calcule le centre du masque binaire (zone détectée).

    :param mask: ndarray 2D (hauteur x largeur) binaire (0 ou 1)
    :return: (x_centre, y_centre) en pixels
    """
    if len(mask.shape) == 4:
        mask = mask[0, :, :, 0]  # shape: (128, 128)
    mask = (mask > 0.1).astype(np.uint8)

    moments = cv2.moments(mask.astype(np.uint8))

    if moments["m00"] != 0 and mask.max() >= 0.1:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        return cx, cy
    else:
        # Pas de zone détectée
        return None