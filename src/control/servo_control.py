from serial import Serial
from time import sleep, time
from config import config

from serial.tools.list_ports import comports

# ⚙️ Configuration globale
debug = config["debug"]
current_angle = [90, 140]  # [PAN, TILT]
inverser_gauche_droite = 1  # 1 ou -1 pour inverser sens gauche/droite
inverser_haut_bas = 1  # 1 ou -1 pour inverser sens haut/bas
servo_type = ["P", "T"]  # Index 0 = PAN, 1 = TILT
laser_on = False

def show_coms():
    # Affiche les ports disponibles
    ports = comports()
    for port in ports:
        print(f"Port COM : {port}")

if config["debug"]:
    show_coms()

# 🔌 Connexion série
arduino = Serial('COM4', 9600)

# Heartbeat
def heartbeat(arduino, timeout=2.0, debug=config["debug"]):
    try:
        arduino.reset_input_buffer()
        arduino.write(b"PING\n")
        start_time = time()

        while time() - start_time < timeout:
            if arduino.in_waiting > 0:
                response = arduino.readline().decode('utf-8').strip()
                if response == "PONG":
                    if debug:
                        print("✅ Heartbeat reçu")
                    return True
        print("❌ Aucun heartbeat reçu")
        return False
    except Exception as e:
        if debug:
            print(f"Erreur heartbeat : {e}")
        return False

# Mise à jour de l'angle
def set_servo_angle(angle, servo=0):  # servo = 0 → PAN, 1 → TILT
    if isinstance(angle, int):
        angle = max(0, min(180, angle))  # Clamp
        global current_angle
        current_angle[servo] = angle
        cmd = f"{servo_type[servo]}{angle}\n"
        arduino.write(cmd.encode('utf-8'))
        if debug:
            print(f"Angle envoyé : {cmd.strip()}")
        return True
    else:
        print("Angle invalide. Doit être un entier.")
        return False

# Incrémentation
def add_angle(delta, servo=0, droite=True):
    if isinstance(delta, int):
        direction = inverser_gauche_droite if droite else -1 * inverser_gauche_droite
        new_angle = current_angle[servo] + direction * delta
        new_angle = max(0, min(180, new_angle))
        if debug:
            print(f"{servo_type[servo]} déplacement : {direction * delta}° → {new_angle}°")
        return set_servo_angle(new_angle, servo=servo)
    else:
        print("Delta invalide. Doit être un entier.")
        return False

# Mouvements
def go_right(delta):
    """
    Tourne le servo spécifié d'un certain nombre de degrés vers la droite.

    :param delta: (int) Le nombre de degrés à tourner vers la droite (positif).
    :param servo: (int) Index du servo à contrôler (0 pour PAN, 1 pour TILT). Par défaut 0 (PAN).
    :return: (bool) True si l'angle a bien été mis à jour, False sinon.
    """
    return add_angle(abs(delta), servo=0, droite=True)


def go_left(delta):
    """
    Tourne le servo spécifié d'un certain nombre de degrés vers la gauche.

    :param delta: (int) Le nombre de degrés à tourner vers la gauche (positif).
    :param servo: (int) Index du servo à contrôler (0 pour PAN, 1 pour TILT). Par défaut 0 (PAN).
    :return: (bool) True si l'angle a bien été mis à jour, False sinon.
    """
    return add_angle(abs(delta), servo=0, droite=False)

def go_up(delta):
    """
    Incline le servo TILT vers le haut d'un certain nombre de degrés.

    :param delta: (int) Le nombre de degrés à incliner vers le haut (positif).
    :return: (bool) True si l'angle a bien été mis à jour, False sinon.
    """
    return add_angle(abs(delta), servo=1, droite=False)

def go_down(delta):
    """
    Incline le servo TILT vers le bas d'un certain nombre de degrés.

    :param delta: (int) Le nombre de degrés à incliner vers le bas (positif).
    :return: (bool) True si l'angle a bien été mis à jour, False sinon.
    """
    return add_angle(abs(delta), servo=1, droite=True)

def init_servos():
    print(current_angle)
    set_servo_angle(current_angle[0], servo=0)
    set_servo_angle(current_angle[1], servo=1)

    return True

def laser(state):
    if state:
        arduino.write("L\n".encode('utf-8'))
    else:
        arduino.write("l\n".encode('utf-8'))

def inverser(val):
    if abs(val) == 1:
        global inverser_gauche_droite
        inverser_gauche_droite = val

sleep(2) # Laisser le temps à Python d'initialiser la connexion
init_servos()

# 🔧 Programme principal de test
if __name__ == "__main__":
    print("Tapez un angle, ex: 'P120' ou 'T45' ou 'P90T60'")
    print("Tapez 'q' pour quitter")

    while True:
        try:
            val = input(f"Angle actuel [PAN={current_angle[0]}, TILT={current_angle[1]}] > ").strip().upper()

            if val == "Q":
                break

            # Envoie brut à l'Arduino (compatible avec sketch adapté)
            arduino.write(f"{val}\n".encode('utf-8'))

            # Affiche la réponse de l’Arduino
            if arduino.in_waiting:
                print("Arduino dit :", arduino.readline().decode('utf-8').strip())

        except Exception as e:
            print(f"Erreur : {e}")
