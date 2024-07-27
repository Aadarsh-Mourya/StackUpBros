#include <ESP8266WiFi.h>
#include <ThingSpeak.h>
#include <TimeLib.h>


const char* ssid = "OMEN16 5213";
const char* password = "0000000000";


unsigned long myChannelNumber = 2610572;
const char* myWriteAPIKey = "WCQ61XWF45F3M7GV";

WiFiClient client;

// GPIO pin connected to the water meter sensor
int sensorPin = 4;
volatile int pulseCount = 0;
unsigned long previousMillis = 0;
const long interval = 8640000; // Interval
const int maxRetries = 3; // Maximum number of retries for data transmission

// Interrupt service routine for counting pulses from the water meter
void ICACHE_RAM_ATTR pulseCounter() {
  pulseCount++;
}

// Function to reconnect to WiFi if the connection is lost
void reconnectWifi() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Reconnecting to WiFi...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    delay(5000); // Wait 5 seconds before retrying
  }
  Serial.println("Connected to WiFi");
}

// Function to calculate water volume based on pulse count
int calculateWaterVolume(int pulses) {
  float pulsesPerLiter = 11.0; // Given F = 11 * Q, so pulses per liter is 11
  float volume = pulses / pulsesPerLiter; // Calculate volume in liters
  return int(volume);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Connect to WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  ThingSpeak.begin(client);

  // Set up the water meter sensor
  pinMode(sensorPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(sensorPin), pulseCounter, FALLING);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    detachInterrupt(sensorPin);

    if (WiFi.status() != WL_CONNECTED) {
      reconnectWifi();
    }

    int waterSupplied = calculateWaterVolume(pulseCount);

    ThingSpeak.setField(1, waterSupplied);
    long currentTime = (long)now();
    ThingSpeak.setField(2, currentTime); //  use a real-time clock

    // Retry logic for sending data to ThingSpeak
    bool success = false;
    for (int i = 0; i < maxRetries; i++) {
      if (ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey)) {
        Serial.println("Data sent to ThingSpeak");
        success = true;
        break;
      } else {
        Serial.println("Failed to send data, retrying...");
        delay(5000); // Wait 5 seconds before retrying
      }
    }

    if (!success) {
      Serial.println("Failed to send data after maximum retries");
      // Implement additional error handling if necessary
    }

    pulseCount = 0;
    attachInterrupt(digitalPinToInterrupt(sensorPin), pulseCounter, FALLING);
  }
}
