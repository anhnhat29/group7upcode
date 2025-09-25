#include <WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>



//----Thông tin Wifi----------------------
const char* ssid = "Xiaomi 11T Pro";      
const char* password = "nhan2004";   

//----Thông tin MQTT Broker---------------
const char* mqtt_server = "9c36c11f80b147c09427b67db165c3b7.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_username = "anhnhat"; 
const char* mqtt_password = "Sn29022004";

// ---------------------------------------




//----------------------------------------

WiFiClientSecure espClient;
PubSubClient client(espClient);

//----------------------------------------
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

//-----Call back khi có tin nhắn về---------
void callback(char* topic, byte* payload, unsigned int length) {
  String incommingMessage = "";
  for (int i = 0; i < length; i++) {
    incommingMessage += (char)payload[i];
  }
  Serial.println("Message arrived [" + String(topic) + "]: " + incommingMessage);

  // Kiểm tra nếu nhận được "hello"
  if (incommingMessage == "hello") {
    Serial.println("✅ Nhận được lệnh HELLO từ HiveMQ!");
  }
}

//------------Reconnect MQTT----------------
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientID = "ESPClient-";
    clientID += String(random(0xffff), HEX);

    if (client.connect(clientID.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("connected");

      // Subscribe vào topic test/esp
      client.subscribe("test/esp");
      Serial.println("Subscribed to topic: test/esp");

    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" -> try again in 5 seconds");
      delay(5000);
    }
  }
}

//----------------------------------------
void setup() {
  Serial.begin(152000);
  setup_wifi();

  // ⚠️ Tạm bỏ qua xác thực chứng chỉ (chỉ test)
  espClient.setInsecure();

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

//----------------------------------------
void fakevalue(float &temp, float &hum, int &rainAnalog, int &rainDigital) {
  temp = random(200, 400) / 10.0;   // 20.0 – 40.0 °C
  hum = random(300, 900) / 10.0;    // 30.0 – 90.0 %
  rainAnalog = random(0, 4096);     // 0 – 4095 (giả lập analog)
  rainDigital = random(0, 2);       // 0 hoặc 1
}

//----------------------------------------
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  static unsigned long lastMsg = 0;
  if (millis() - lastMsg >2000) {  // publish mỗi 2 giây
    lastMsg = millis();

    float temperature, humidity;
    int rainAnalog, rainDigital;
    fakevalue(temperature, humidity, rainAnalog, rainDigital);

    // Tạo JSON
    JsonDocument doc;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["rainAnalog"] = rainAnalog;
    doc["rainDigital"] = rainDigital;

    char buffer[200];
    serializeJson(doc, buffer);

    client.publish("test/esp", buffer);
    Serial.print("Published: ");
    Serial.println(buffer);
  }
}
