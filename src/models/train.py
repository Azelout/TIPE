import numpy as np
from tensorflow.keras.saving import save_model
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from src.utils.utils import load_images, show_model_stats
from sys import getsizeof
from model import unet_model
from config import config
from os.path import dirname, abspath
path = dirname(abspath(__file__))

size = (config["model"]["input_shape"], config["model"]["input_shape"], 3)

def training():
    images, masks = load_images(size) # On récupère toutes les images

    # S'assurer que les masques ont la bonne forme (ajouter une dimension pour les canaux)
    masks = np.expand_dims(masks, axis=-1)  # Passer de (128, 128) à (128, 128, 1)

    # Vérifier les formes
    print(f"Images shape: {images.shape} Masks shape: {masks.shape}")
    print("Images: Mo", getsizeof(images) / (1024**2), "Masks: Mo", getsizeof(masks) / (1024**2))

    # Créer le modèle
    model = unet_model(size)

    # Paramètrage de l'apprentissage
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
    checkpoint = ModelCheckpoint(f'{path}/../../models/best_model.keras', monitor='val_loss', save_best_only=True, mode='min', verbose=1) # Définir le checkpoint pour sauvegarder le meilleur modèle basé sur la validation

    # Entrainer le modèle
    print("Début de l'entrainement:")
    history = model.fit(images, masks, epochs=config["training"]["epochs"], batch_size=config["training"]["batch_size"], validation_split=0.1, callbacks=[reduce_lr, checkpoint])

    # Sauvegarder le modèle
    save_model(model, f'{path}/../../{config["results"]["models"]}/new_{config["results"]["model_name"]}')

    show_model_stats(history)


if __name__ == "__main__":
    training()
