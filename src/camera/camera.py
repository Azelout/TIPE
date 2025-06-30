from PIL import Image
import cv2

def take_picture(dimension=None):
    camera = cv2.VideoCapture(0) # Changer le numéro si pas la bonne caméra
    ret, frame = camera.read() # Prise de la photo
    camera.release()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convertion numpy array → Image PIL
        image = Image.fromarray(frame)

        if dimension:
            image = image.resize(dimension)

        return image

    return False


if __name__ == "__main__":
    img = take_picture()
    img.save("image.jpg")