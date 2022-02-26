#include <Arduino_LSM9DS1.h>

float x, y, z;
int degreesX = 0;
int degreesY = 0;

// See the readme on assigning this value. If you have just one monitor, leave it at 1.
int displayID = 1;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
  }

  if (x > 0.1) {
    x = 100 * x;
  }
  if (x < -0.1) {
    x = 100 * x;
  }
  if (y > 0.1) {
    y = 100 * y;
    Serial.print(displayID);
    Serial.print(" ");
    Serial.println(y);
  }
  if (y < -0.1) {
    y = 100 * y;
    Serial.print(displayID);
    Serial.print(" ");
    Serial.println(y);
  }
  delay(700);
}
