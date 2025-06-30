import yaml
from os.path import abspath, dirname, join

def load_config(config_path="config.yaml"):
    # Obtenir le répertoire du fichier config.py
    config_dir = dirname(abspath(__file__))

    # Construire le chemin absolu vers config.yaml
    config_path = join(config_dir, config_path)

    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

if __name__ == "__main__":
    print(config)