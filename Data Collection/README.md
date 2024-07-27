# Water Meter Sensor with ThingSpeak

This project uses an ESP8266 to monitor water usage with a water meter sensor and send data to ThingSpeak (a cloud platform by MathWorks).

## Components

- ESP8266 microcontroller
- Water meter sensor
- WiFi network
- ThingSpeak account

![alt text](https://github.com/Aadarsh-Mourya/StackUpBros/blob/7303c59e9d2b1a07949c8ab715c6a71ff71c2881/Data%20Collection/WhatsApp%20Image%202024-07-27%20at%2018.03.25_5331fda8.jpg)

## Setup

1. **Install Libraries:**
   - In the Arduino IDE, go to **Sketch** > **Include Library** > **Manage Libraries**.
   - Install `ESP8266WiFi`, `ThingSpeak`, and `TimeLib`.

2. **Configure:**
   - Update the `ssid`, `password`, `myChannelNumber`, and `myWriteAPIKey` in the code with your credentials.

## Code Overview

- **`sensorPin`**: GPIO pin for the water meter.
- **`interval`**: Upload interval (currently 24 hours).
- **`calculateWaterVolume`**: Converts pulse count to water volume.
- **`pulseCounter`**: Interrupt routine to count pulses.
- **`reconnectWifi`**: Reconnects to WiFi if needed.
- **`setup`**: Initializes WiFi and sensor.
- **`loop`**: Sends data to ThingSpeak every 24 hours.

## Usage

1. **Upload Code:**
   - Connect ESP8266 and upload the sketch.

2. **Monitor Data:**
   - Check the Serial Monitor for status.
   - View data on your ThingSpeak channel.

## Troubleshooting

- **WiFi Issues:** Check credentials and connection.
- **Data Upload Issues:** Verify API key and channel number.
