#include <Servo.h>

Servo servoPan;
Servo servoTilt;

int anglePan = 140;   // Valeurs initiales
int angleTilt = 90;

const int laserPin = 6; // Broche pour le laser
void setup() {
  Serial.begin(9600);

  // Servomoteurs
  servoPan.attach(9);
  servoTilt.attach(10);

  servoPan.write(anglePan);
  servoTilt.write(angleTilt);

  // Laser
  pinMode(laserPin, OUTPUT); // Définit la broche comme sortie
  digitalWrite(laserPin, LOW); // Commence avec le laser éteint
}

void loop() {
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == 'L') {
      digitalWrite(laserPin, HIGH); // Allume le laser
    }
    else if (msg == 'l') {
      digitalWrite(laserPin, LOW);  // Éteint le laser
    }

    // Recherche des positions P et T (s'il y en a)
    int pIndex = msg.indexOf('P');
    int tIndex = msg.indexOf('T');

    if (pIndex != -1) {
      int end = (tIndex != -1 && tIndex > pIndex) ? tIndex : msg.length();
      String valStr = msg.substring(pIndex + 1, end);
      anglePan = constrain(valStr.toInt(), 0, 180);
      servoPan.write(anglePan);
    }

    if (tIndex != -1) {
      String valStr = msg.substring(tIndex + 1);
      angleTilt = constrain(valStr.toInt(), 0, 180);
      servoTilt.write(angleTilt);
    }

    // Nettoyage du buffer série
    while (Serial.available()) Serial.read();
  }
}
