from config import config
import os
from PIL import Image, ImageOps

def resize_images(input_folder, output_folder, size=(528, 528)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        # Vérification si le fichier est une image
        if filename.endswith(('.png', '.jpg', '.jpg', '.bmp', '.gif')):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                img_resized = img.resize(size, Image.LANCZOS) # Redimension de l'image

                output_path = os.path.join(output_folder, filename)
                img_resized.save(output_path)
                print(f"Image {filename} redimensionnée et sauvegardée dans {output_folder}")


def convert_to_grayscale(input_folder):
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    # Parcourir tous les fichiers dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        # Vérifier si le fichier est une image
        if filename.endswith(('.png', '.jpg', '.bmp', '.gif')):
            # Ouvrir l'image
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # Convertir l'image en nuances de gris
                img_grayscale = img.convert('L')
                img_grayscale = ImageOps.autocontrast(img_grayscale)
                # Sauvegarder l'image en nuances de gris dans le dossier de sortie
                output_path = os.path.join(input_folder, filename.replace(".", "_bw."))
                img_grayscale.save(output_path)
                print(f"Image {filename} convertie en nuances de gris et sauvegardée dans {input_folder}")


if __name__ == "__name__":
    ## Utilisation de la redimension
    input_folder = '../data/train/'
    output_folder = '../data/train/'


    ## Utilisation de la couleur
    input_folder = '../data/gris/'
    # convert_to_grayscale(input_folder)