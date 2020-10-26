// Required libraries
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi Configs
const char *ssid = "Orange 24G";
const char *pass = "9827845700";
const char *device_name = "Room0";
IPAddress staticIP(192, 168, 29, 89);
IPAddress gateway(192, 168, 29, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress dns(8, 8, 4, 4);

// MQTT Server configs
const char *mqttServer = "192.168.29.148";
const int mqttPort = 1883;
const char *mqttUser = "root_system0";
const char *mqttPassword = "random.random()";

WiFiClient espClient;
PubSubClient client(espClient);

int reed_pin = 4;
int reed_state = 0;
int thermal_pin = 5;
int thermal_state = 0;
int reed_power = 14;
int thermal_on = 0;
long double timer = 25000;


void reconnect_device()
{
    WiFi.begin(ssid, pass);


    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
    }


    while (true)
    {
        if (client.connect(device_name, mqttUser, mqttPassword)) break;
        else 
        delay(5000);  
    }
    String message = "Room0," + WiFi.localIP().toString();
    client.publish("attendance", message.c_str());

}


void setup() {

    pinMode(reed_pin, INPUT);
    pinMode(thermal_pin, INPUT);
    pinMode(reed_power, OUTPUT);
    digitalWrite(reed_power, HIGH);

    Serial.begin(115200);

    // WiFi configs 2
    WiFi.mode(WIFI_STA);
    WiFi.hostname(device_name);
    WiFi.config(staticIP, dns, gateway, subnet);

    // MQTT configs 2
    client.setServer(mqttServer, mqttPort);


}

void loop() {
    // put your main code here, to run repeatedly:
    if (WiFi.status() != WL_CONNECTED || !client.connected()) reconnect_device();
    client.loop();


    digitalWrite(reed_power, HIGH);
    int reed_reading = digitalRead(reed_pin);
    digitalWrite(reed_power, LOW);
    int thermal_reeding = digitalRead(thermal_pin);


    if (!reed_reading) {
        if (reed_state) 
        {
            client.publish("test/0", "0");
            reed_state = 0;
        }
    }
    else {
        if (!reed_state)
        {
            client.publish("test/0", "1");
            reed_state = 1;
        }

    }
    Serial.println(thermal_reeding);
    client.publish("test/1", String(thermal_reeding).c_str());
    if (millis() - timer > 5000.0)
    {
        client.publish("test/2", "1");
        if (thermal_reeding != thermal_state)
        {
            thermal_state = thermal_reeding;
            if (!thermal_reeding)
            {
                timer = millis();
            }
        }
    }
    else
    {
        client.publish("test/2", "0");
    }
    
}
