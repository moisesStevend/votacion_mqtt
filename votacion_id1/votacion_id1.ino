#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "HUAWEI-1605";
const char* password = "75985170";
const char* mqtt_server = "192.168.8.110";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50],data_payload[50];
int value = 0;

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  digitalWrite(BUILTIN_LED, HIGH);
  pinMode(0,INPUT_PULLUP);
  pinMode(14,INPUT_PULLUP);
  pinMode(13,INPUT_PULLUP);
  pinMode(12,INPUT_PULLUP);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
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
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("votacion/cliente/1")) {
      Serial.println("connected");
      digitalWrite(BUILTIN_LED, LOW);
      client.publish("votacion/cliente/1/publish", "conectado ID 1");
      //client.subscribe("$votacion/cliente/1/subscribe");
      client.subscribe("votacion/cliente/1/publish");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if(!digitalRead(13)){
      delay(200);
      snprintf (msg, 75, "{id: %s,favor: %d, contra: %d, abstencion: %d}", "id 1",false, true, false);
      client.publish("votacion/cliente/1/publish", msg);
      Serial.println(msg);
    }else {
        if(!digitalRead(14)){
          delay(200);
          snprintf (msg, 75, "{id: %s,favor: %d, contra: %d, abstencion: %d}", "id 1",true,false , false);
          client.publish("votacion/cliente/1/publish", msg);
          Serial.println(msg);
        }else{
            if(!digitalRead(12)){
              delay(200);
              snprintf (msg, 75, "{id: %s,favor: %d, contra: %d, abstencion: %d}", "id 1",false, false, true);
              client.publish("votacion/cliente/1/publish", msg);
              Serial.println(msg);
            }  
          }      
      }  
}
