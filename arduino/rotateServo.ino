#include <Servo.h>

const int servoPin1 = 2;
const int servoPin2 = 3;

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
}

void loop() {
  if (Serial.available() > 0)
  {
    char str[30];
    int amount = Serial.readBytesUntil(';', str, 30);
    str[amount] = NULL;

    int servoRotate1, servoRotate2;
    sscanf(str, "%d,%d", &servoRotate1, &servoRotate2);

    servo1.write(servoRotate1);

    servo2.write(servoRotate2);
  }
}