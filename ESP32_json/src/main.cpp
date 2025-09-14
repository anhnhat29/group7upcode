#include <Arduino.h>
#include "DHT.h"
#include <ArduinoJson.h>

#define DHTPIN 4       // GPIO4 cho DHT11
#define DHTTYPE DHT11  // Loại cảm biến DHT

#define RAIN_ANALOG_PIN 2   // Analog input (A2)
#define RAIN_DIGITAL_PIN 5  // Digital output pin từ module cảm biến mưa

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32-S3 đọc DHT11 + cảm biến mưa JSON...");
  dht.begin();

  pinMode(RAIN_DIGITAL_PIN, INPUT);
}

void loop() {
  // Đọc cảm biến DHT11
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Đọc cảm biến mưa
  int rainAnalog = analogRead(RAIN_ANALOG_PIN);  // giá trị 0 - 4095
  int rainDigital = digitalRead(RAIN_DIGITAL_PIN); // 0 hoặc 1

  // Kiểm tra lỗi DHT
  if (isnan(h) || isnan(t)) {
    Serial.println("{\"error\":\"DHT11 không đọc được dữ liệu\"}");
    delay(2000);
    return;
  }

  // Tạo JSON
  StaticJsonDocument<200> doc;
  doc["temperature"] = t;
  doc["humidity"] = h;
  doc["rainAnalog"] = rainAnalog;
  doc["rainDigital"] = rainDigital;

  // In JSON ra Serial
  serializeJson(doc, Serial);
  Serial.println();

  delay(2000);
}
