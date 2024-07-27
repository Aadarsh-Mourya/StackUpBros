#include <ESP8266WiFi.h>
#include <ThingSpeak.h>

// WiFi credentials
const char* ssid     = "SSID";
const char* password = "PAssword";

// ThingSpeak credentials
unsigned long myChannelNumber = YOUR_CHANNEL_NUMBER;
const char * myWriteAPIKey = "api_key";

WiFiClient  client;

// GPIO pin connected to the water meter sensor
int sensorPin = D2; 
volatile int pulseCount;

// Interrupt service routine for counting pulses from the water meter
void ICACHE_RAM_ATTR pulseCounter() {
  pulseCount++;
}

// Function to reconnect to WiFi if connection is lost
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
// You'll need to calibrate this function according to your specific water meter sensor
int calculateWaterVolume(int pulses) {
  float volumePerPulse = 0.1; // Example: 0.1 liters per pulse
  return int(pulses * volumePerPulse);
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
  delay(86400000); // Collect data once every 24 hours
  detachInterrupt(sensorPin);

  if (WiFi.status() != WL_CONNECTED) {
    reconnectWifi();
  }

  int waterSupplied = calculateWaterVolume(pulseCount);
  
  ThingSpeak.setField(1, String(waterSupplied));
  ThingSpeak.setField(2, String(millis()/86400000));  // Assuming the ESP8266 has been running continuously; otherwise use a real-time clock
  
  // Send the data to ThingSpeak
  if (ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey)) {
    Serial.println("Data sent to ThingSpeak");
  } else {
    Serial.println("Failed to send data");
    // Implement retry logic or error handling
  }
  
  pulseCount = 0;
  attachInterrupt(digitalPinToInterrupt(sensorPin), pulseCounter, FALLING);
}