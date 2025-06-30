from config import config
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, array_to_img

i_max = config["preprocessing"]["augmentation_per_image"]


# Création du générateur d'images avec les transformations souhaitées
data_gen_args = dict(config["preprocessing"]["augmentation"])
datagen = ImageDataGenerator(**data_gen_args)


# Fonction pour augmenter les images et les masques associés
def augmenter_images_et_masques(path):
    # Parcourir toutes les images dans le dossier source
    for nom_fichier in os.listdir(path):
        print(nom_fichier)
        if nom_fichier.endswith(".jpg"):
            # Charger l'image et le masque
            chemin_image = path + nom_fichier
            chemin_masque = path + nom_fichier.replace(".jpg", ".png")

            img = load_img(chemin_image, keep_aspect_ratio=True)
            mask = load_img(chemin_masque, color_mode="grayscale", keep_aspect_ratio=True)

            # Convertir les images en tableaux NumPy
            x_img = img_to_array(img)
            x_mask = img_to_array(mask)

            # Reshape pour ajouter la dimension de batch << J'ai pas compris
            x_img = x_img.reshape((1,) + x_img.shape)
            x_mask = x_mask.reshape((1,) + x_mask.shape)

            # Création des générateurs synchronisés pour l'image et le masque << J'ai pas compris
            img_gen = datagen.flow(x_img, batch_size=1, seed=1)
            mask_gen = datagen.flow(x_mask, batch_size=1, seed=1)

            # Génération des images augmentées
            i = 0
            for (batch_img, batch_mask) in zip(img_gen, mask_gen):
                # Convertir les tableaux NumPy en images
                aug_img = array_to_img(batch_img[0])
                aug_mask = array_to_img(batch_mask[0], scale=False)

                # Enregistrer les images et les masques augmentés
                aug_img.save(path + f'aug_{i}_{nom_fichier}')
                aug_mask.save(path + f'aug_{i}_{nom_fichier.replace(".jpg", ".png")}')

                i += 1
                if i >= i_max:  # Limite le nombre d'augmentations par image
                    break

if __name__ == "__main__":

    augmenter_images_et_masques("A:/CHEMIN/DOSSIER_PHOTOS/")
    print("Augmentation des images et masques terminée.")