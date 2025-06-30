from time import sleep
from src.control.servo_control import current_angle, go_left, go_right, go_up, go_down, init_servos, inverser, laser
from src.utils.utils import get_centroid_from_mask
from src.camera.camera import take_picture
from src.models.prediction import prediction
from config import config

IMAGE_SCALE = config["model"]["input_shape"]
center = (IMAGE_SCALE // 2, IMAGE_SCALE // 2)
center_range = 10  # en pixels
init_servos()

while True:
    img = take_picture()
    if img:  # Vérifie qu'une photo est prise
        img = img.rotate(angle=90, expand=True)
        predicted_mask = prediction(image=img)
        if config["debug"]:
            img.save("img.jpg")

        inverser(1)

        if current_angle[1] > 140:
            inverser(-1)

        if predicted_mask.max() >= 0.3:
            centroid = get_centroid_from_mask(predicted_mask)

            if centroid:
                duck_found = [False, False]
                ## Coordonnée X
                if centroid[0] < center[0] - center_range:
                    go_right(10)
                elif centroid[0] > center[0] + center_range:
                    go_left(10)
                else:
                    print("Tu es centré pour les X")
                    duck_found[0] = True

                ## Coordonnée Y
                if centroid[1] < center[1] - center_range:
                    go_down(10)
                elif centroid[1] > center[1] + center_range:
                    go_up(10)
                else:
                    print("Tu es centré pour les Y")
                    duck_found[1] = True

                if duck_found == (True, True):
                    laser(True)
                    sleep(1)
                    laser(False)
    sleep(0.5)