import requests
from os import remove
from config import config

def image_to_discord(image_path, model):
    if image_path.endswith(".png"):
        with open(image_path, 'rb') as f:
            files = {
                'file': (image_path, f)
            }
            requests.post(config["results"]["webhook"], files=files, data={"content": model})

        remove(image_path)