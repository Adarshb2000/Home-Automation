// Required libraries
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>

// WiFi Configs
const char *ssid = "WIFI SSID";
const char *pass = "WIFI Password";
const char *device_name = "Room0";
IPAddress staticIP(192, 168, 29, 89);
IPAddress gateway(192, 168, 29, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress dns(8, 8, 4, 4);

// MQTT Server configs
const char *mqttServer = "mqtt server ip";
const int mqttPort = 1883;
const char *mqttUser = "userid";
const char *mqttPassword = "password";

WiFiClient espClient;
PubSubClient client(espClient);

// AC configs
IRsend irsend(4);
const unsigned int kAc_Type  = 1;
unsigned int ac_heat = 1;
unsigned int ac_power_on = 0;
unsigned int ac_light_on = 0;
unsigned int ac_air_clean_state = 0;
unsigned int ac_temperature = 20;
unsigned int ac_flow = 0;
const uint8_t kAc_Flow_Wall[4] = {0, 2, 4, 5};
uint32_t ac_code_to_sent;
bool timer_present = false;
long timer_time;
long start_time;

// temprature configs
int gpios[] = {4, 5, 12, 13, 14};
float temp_const = 5.0 / 10.24;
float temp_threshold_max = 35.0;
float temp_threshold_min = 20.0;
int temp_delay = 2000;
unsigned long last_calculated = millis();

void Ac_Send_Code(uint32_t code) {
  irsend.sendLG(code, 28);
}

void Ac_Activate(unsigned int temperature, unsigned int air_flow,
                 unsigned int heat) {
  ac_heat = 0;
  unsigned int ac_msbits1 = 8;
  unsigned int ac_msbits2 = 8;
  unsigned int ac_msbits3 = 0;
  unsigned int ac_msbits4;
  if (ac_heat == 1)
    ac_msbits4 = 4;  // heating
  else
    ac_msbits4 = 0;  // cooling
  unsigned int ac_msbits5 =  (temperature < 15) ? 0 : temperature - 15;
  unsigned int ac_msbits6 = 0;

  if (air_flow <= 2) {
      ac_msbits6 = kAc_Flow_Wall[air_flow];
  }

  // calculating using other values
  unsigned int ac_msbits7 = (ac_msbits3 + ac_msbits4 + ac_msbits5 +
                             ac_msbits6) & B00001111;
  ac_code_to_sent = ac_msbits1 << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits2) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits3) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits4) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits5) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits6) << 4;
  ac_code_to_sent = (ac_code_to_sent + ac_msbits7);

  Ac_Send_Code(ac_code_to_sent);

  ac_power_on = 1;
  ac_light_on = 1;
  ac_temperature = temperature;
  ac_flow = air_flow;
}

void Ac_light()
{
  ac_code_to_sent = 0x88C00A6;
  Ac_Send_Code(ac_code_to_sent);
  if (ac_light_on)
    ac_light_on = 1;
   else 
    ac_light_on = 0;
}

void Ac_Change_Air_Swing(int air_swing, int swing_type) {
  if (swing_type) {
    if (air_swing == 1)
      ac_code_to_sent = 0x881316B;
    else
      ac_code_to_sent = 0x881317C;
  } else {
    if (air_swing == 1)
      ac_code_to_sent = 0x8813149;
    else
      ac_code_to_sent = 0x881315A;
  }
  Ac_Send_Code(ac_code_to_sent);
}

void Ac_Air_Clean(int air_clean) {
  if (air_clean == '1')
    ac_code_to_sent = 0x88C00B7;
  else
    ac_code_to_sent = 0x88C00C8;

  Ac_Send_Code(ac_code_to_sent);

  ac_air_clean_state = air_clean;
}

void Ac_Power_Down() {
  ac_code_to_sent = 0x88C0051;

  Ac_Send_Code(ac_code_to_sent);

  ac_power_on = 0;
  ac_light_on = 0;
}


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
  client.subscribe("room0/#");
}

void callback(char* topic, byte* payload, unsigned int len)
{
  // payload for intensity topic for on or off
  String topic1 = topic;
  if (!strcmp(topic1.substring(6).c_str(), "set_threshold"))
  {
    int which = payload[0] - '0';
    char temperature[3];
    for (int i = 0; i < len - 1; i += 1)
      temperature[i] = payload[i + 1];
    temperature[len - 1] = '\0'; 
    String temp0 = temperature;
    if (which)
    {
      temp_threshold_max = temp0.toFloat();
    }
    else
    {
      temp_threshold_min = temp0.toFloat();
    }
    return;
  }
  int pin = topic1.substring(6).toInt();
  if (pin == 4)
  {
    char a = payload[0];
    char b = payload[1];
    switch (a) {
      case '0':  // off
        Ac_Power_Down();
        break;
      case '1':  // on
        Ac_Activate(ac_temperature, ac_flow, ac_heat);
        break;
      case '2':
      {
      char c = payload[2];
      int swing_type = c - '0';
        if (b == '0')
          Ac_Change_Air_Swing(0, swing_type);
        else
          Ac_Change_Air_Swing(1, swing_type);
        break;
      }
      case '3':  // 1  : clean on, power on
        if (b == '0' || b == '1')
          Ac_Air_Clean(b);
        break;
      case '4':
        switch (b) {
          case '1':
            Ac_Activate(ac_temperature, 1, ac_heat);
            break;
          case '2':
            Ac_Activate(ac_temperature, 2, ac_heat);
            break;
          case '3':
            Ac_Activate(ac_temperature, 3, ac_heat);
            break;
          default:
            Ac_Activate(ac_temperature, 0, ac_heat);
        }
        break;
      case '+':
        if (18 <= ac_temperature && ac_temperature <= 29)
          Ac_Activate((ac_temperature + 1), ac_flow, ac_heat);
        break;
      case '-':
        if (19 <= ac_temperature && ac_temperature <= 30)
          Ac_Activate((ac_temperature - 1), ac_flow, ac_heat);
        break;
      case 'l':
        Ac_light();
        break;
      case 'm':
        /*
            if ac is on,  1) turn off, 2) turn on Ac_Air_Clean(1)
            if ac is off, 1) turn on,  2) turn off Ac_Air_Clean(0)
        */
        if (ac_power_on == 1) {
          Ac_Power_Down();
          delay(100);
          Ac_Air_Clean(1);
        } else {
          if (ac_air_clean_state == 1) {
            Ac_Air_Clean(0);
            delay(100);
          }
          Ac_Activate(ac_temperature, ac_flow, ac_heat);
        }
        break;
      case 't':
      {
        char temp[50];
        for (int i = 0; i < len - 2; i += 1)
        {
          temp[i] = payload[i + 2];
        }
        temp[len - 1] = '\0';
        String temp2 = temp;
        timer_time = temp2.toInt();
        timer_time = timer_time * 60 * 1000;
        start_time = millis();
        timer_present = true;
      }
    }
  }
  else
  {
    digitalWrite(pin, !digitalRead(pin));
    String message = device_name + String(pin) + digitalRead(pin);
    client.publish("manager", message.c_str());
  }
}


void setup() {
  pinMode(A0, INPUT);
  for (int i = 0; i < 5; i += 1)
  {
    pinMode(gpios[i], OUTPUT);
  }
  for (int i = 0; i < 5; i += 1)
  {
    digitalWrite(gpios[i], HIGH);
  }

  // WiFi configs 2
  WiFi.mode(WIFI_STA);
  WiFi.hostname(device_name);
  WiFi.config(staticIP, dns, gateway, subnet);

  // MQTT configs 2
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  // AC configs 2
  irsend.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
  if (WiFi.status() != WL_CONNECTED || !client.connected()) reconnect_device();
  client.loop();
  if (timer_present)
  {
    if (millis() - start_time > timer_time)
    {
      Ac_Power_Down();
      timer_present = false;
    }
  }
  
  if (millis() - last_calculated > temp_delay)
  {
    float temp = temp_const * analogRead(A0);
    client.publish("test", String(temp).c_str());
    if (temp > temp_threshold_max && ac_power_on)
      Ac_Activate(ac_temperature, ac_flow, ac_heat);
    else if (temp_threshold_min && !ac_power_on)
      Ac_Power_Down();
      last_calculated = millis();
  }
  
}
