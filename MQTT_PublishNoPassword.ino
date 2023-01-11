/*
 * Code taken from: Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
 */
#include "Adafruit_AM2320.h"
#include <ESP8266WiFi.h> // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker
#include "Wire.h"

#define TCAADDR 0x70

// WiFi
// Make sure to update this for your own WiFi network!
const char* ssid = "RedRover";
// const char* wifi_password = "";

// MQTT
// Make sure to update this for your own MQTT Broker!
const char* mqtt_server = "10.49.246.173";
char* mqtt_topic = "sensor1";
char* mqtt_topic2 = "sensor2";
char* mqtt_topic3 = "sensor3";
char* topic;
// The client id identifies the ESP8266 device. Think of it a bit like a hostname (Or just a name, like Greg).
const char* clientID = "Client";

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker

Adafruit_AM2320 am2320 = Adafruit_AM2320();

float currentTemp = 0.0;

void tcaselect(uint8_t i) {
  if (i > 7) return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void setup() {
  Serial.begin(115200);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  if (client.connect(clientID)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.print(client.state());
    Serial.println(" Connection to MQTT Broker failed...");
  }

  am2320.begin();

  delay(500);
  
}

void loop() {
  for (uint8_t t=0; t<=2; t++) {  
    currentTemp = am2320.readTemperature();
    tcaselect(t);
    Wire.beginTransmission(0x5c);
    if (t == 0) {
      topic = mqtt_topic;
    }
    else if (t == 1) {
      topic = mqtt_topic2;
    }
    else if (t == 2) {
      topic = mqtt_topic3;
    }
    Serial.print(topic); Serial.print(" ");
    Serial.println(String(currentTemp).c_str());
    if (client.publish(topic, String(currentTemp).c_str(), true)) {
      Serial.print(String(currentTemp).c_str());
      Serial.println(" message sent!");
    }
    // Again, client.publish will return a boolean value depending on whether it succeded or not.
    // If the message failed to send, we will try again, as the connection may have broken.
    else {
      Serial.print(client.state());
      Serial.println(" Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(clientID);
      delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
      client.publish(mqtt_topic, String(currentTemp).c_str(), true);
    }
    delay(10);
  }
  Serial.println("exit");

  delay(100);
}
