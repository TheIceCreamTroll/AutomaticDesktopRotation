#include <Arduino_LSM9DS1.h>

float x, y, z;

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

  y = 100 * y;
  Serial.print(displayID);
  Serial.print(" ");
  Serial.println(y);

  delay(700);
}
