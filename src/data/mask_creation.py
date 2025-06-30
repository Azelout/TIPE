import json
from PIL import Image, ImageDraw
import os


def generate_masks_from_json(json_path, output_dir, mask_name):
    """
    Génère des masques à partir d'un fichier JSON contenant des annotations de polygones.

    :param json_path: Chemin vers le fichier JSON.
    :param output_dir: Dossier où les masques seront sauvegardés.
    """
    # Chargement du fichier JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for shape in data['shapes']:
        mask_path = os.path.join(output_dir, mask_name)

        # Créer une image vide (noire)
        mask = Image.new("L", (data["imageWidth"], data["imageHeight"]), 0)

        # Dessiner le polygone
        polygon = [(x, y) for x, y in shape['points']] # Récupération des points du polygone
        draw = ImageDraw.Draw(mask)
        draw.polygon(polygon, outline=255, fill=255)  # Création du masque blanc à partir du polygone

        # Sauvegarde
        mask.save(mask_path)
        print(f"Mask {mask_name} saved")


def generate_all_masks_from_json_folder(json_folder, output_folder):
    mask_list = os.listdir(output_folder)
    for nom_fichier in os.listdir(json_folder):
        name = nom_fichier[0:len(nom_fichier) - 4] + ".png"
        if not name in mask_list:
            print(json_folder+nom_fichier)
            generate_masks_from_json(json_folder + nom_fichier, output_folder, name)
        else:
            print("Skipped " + nom_fichier + ": The mask already exist")

if __name__ == "__main__":
    generate_all_masks_from_json_folder("../data/json_data/", "../data/train/") # /!\ Il faut mettre un "/" à la fin des chemins
    