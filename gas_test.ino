const int sensor = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(sensor);
  Serial.println(value);
  delay(500);
}
