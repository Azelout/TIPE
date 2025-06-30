# Détection de Départ d'Incendie en Cuisine

![Bannière Lycée Raspail](https://i.imgur.com/HIUteQk.png)

## Présentation du Projet

Ce projet vise à développer une intelligence artificielle capable de détecter les débuts de départ d'incendie dans un environnement de cuisine. Le départ d'incendie est modélisé par un canard en plastique jaune. Le modèle utilisé est de type U-Net, connu pour sa performance dans les tâches de segmentation d'images.

## Contexte

Ce projet s'inscrit dans le cadre de mon épreuve de CPGE TIPE (Travaux d'Initiative Personnelle Encadrés). L'objectif est d'explorer les capacités de l'intelligence artificielle à identifier rapidement et précisément des situations potentiellement dangereuses, comme le début d'un incendie, afin de prévenir des accidents domestiques.

## Fonctionnalités

- **Détection Précoce** : Identifie les signes précoces d'un départ d'incendie.
- **Modèle U-Net** : Utilise un réseau de neurones convolutifs de type U-Net pour la segmentation d'images.
- **Interface Utilisateur** : Fournit une interface simple pour tester le modèle avec de nouvelles images.

## Installation

1. Clonez ce dépôt sur votre machine locale :
   ```bash
   git clone https://github.com/azelout/fuoco.git
   cd fuoco
