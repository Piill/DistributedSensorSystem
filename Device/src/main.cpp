#include "main.h"
#include "info.h"

int status = WL_IDLE_STATUS;     // the Wifi radio's status
WiFiClient client;
struct config client_config;
bool configured = false;

// Generate random deviceID, based on the compile time.
// This means we should recompile fore every new device
const uint32_t deviceID = (((uint32_t)__TIME__[0]) + ((uint32_t)__TIME__[1]*10) + (__TIME__[6]*100)) * (((uint32_t)__TIME__[7])*1000);
// const uint32_t deviceID = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.print("DeviceID: ");
  Serial.println(deviceID);

}


bool loop_error;
void loop() {
  loop_error = false;
  ensure_connection();

  if(!configured) {
    Serial.println("Device unconfigured");
    Serial.println("Send reg");
    sendReg();
    uint8_t buffer[MAXMESSAGE];
    MESSAGE_TYPE ret = decode_message(buffer);
    switch (ret) {
      case ack:
      {
        Serial.println("Got Ack");
      }
      break;
      case config:
      {
        Serial.println("Got Config");
        configured = true;
        memcpy(&client_config, buffer, sizeof(struct config));
        sendAck();
        init_config();
      }
      break;
      default:
      {
        Serial.println("Error..");
        Serial.println(ret);
        loop_error = true;
      }
      break;
    }
  } else {
    Serial.println("Device configured");
    Serial.println("Send data");
    sendData();
    uint8_t buffer[MAXMESSAGE];
    switch (decode_message(buffer)) {
      case ack:
      /* Do nothing */
      Serial.println("Got ack");
      break;

      case config:
      {
        Serial.println("Got config");
        free(client_config.sensors);
        memcpy(&client_config, buffer, sizeof(struct config));
        sendAck();
        init_config();
      }
      break;

      default:
      loop_error = true;
      break;
    }
  }

  client.stop();
  delay(INTERVAL);
}

void init_config() {
  for(int i = 0; i < client_config.numSensors; i++) {
    if(client_config.sensors[i].type == TYPE_DIGITAL) {
      pinMode(client_config.sensors[i].pin, INPUT);
    }
  }
}

MESSAGE_TYPE decode_message(void* out_buffer) {
  while(client.available() == 0);
  uint8_t in_buffer[MAXMESSAGE];
  int i;
  for(i = 0; client.available() > 0; i++) {
    in_buffer[i] = client.read();
  }

  switch(in_buffer[0]) {
    case 0x1: /* Register */
    /* Should not occour, so we won't waste time actually decoding the message */
    return reg;
    break;
    case 0x2: /* Config */
    {
      struct config* c = (struct config*) out_buffer;
      c->numSensors = in_buffer[1];
      c->sensors = (struct sensor* )malloc(c->numSensors*sizeof(struct sensor));
      for(int j = 0; j < c->numSensors; j++) {
        int offset = 6*j + 2;
        c->sensors[j].id = combine_int(&in_buffer[offset]);
        c->sensors[j].type = in_buffer[offset+4];
        c->sensors[j].pin = in_buffer[offset+5];
      }
      return config;
    }
    break;
    case 0x3: /*Sensor Data */
    /* Should not occour, so we won't waste time actually decoding the message */
    return sensor_data;
    break;
    default:
    case 0x4: /* Error */
    return error;
    break;
    case 0x5: /* Ack */
    return ack;
    break;
  }

}

uint32_t combine_int(uint8_t* in) {
  return in[3] | (in[2] >> 8) | (in[1] >> 8*2) | (in[0] >> 8*3);
}

struct sensor_data* read_data() {
  struct sensor_data *sd = (struct sensor_data*)malloc(client_config.numSensors*sizeof(struct sensor_data));

  for(int i = 0; i < client_config.numSensors; i++) {
    sd[i].id = client_config.sensors[i].id;
    if(client_config.sensors[i].type == TYPE_DIGITAL) {
      sd[i].data = digitalRead(client_config.sensors[i].pin);
    } else {
      sd[i].data = analogRead(client_config.sensors[i].pin);
    }
  }

  return sd;
}


void sendReg() {
  client.write(0x1);
  sendInt(deviceID);
}


void sendData() {
  struct sensor_data* sd = read_data();
  client.write(0x3);
  sendInt(deviceID);
  client.write(client_config.numSensors);
  for(int i = 0; i < client_config.numSensors; i++) {
    Serial.print("Sending (id, data): ");
    Serial.print(sd[i].id);
    Serial.print(", ");
    Serial.print(sd[i].data);
    sendInt(sd[i].id);
    sendInt(sd[i].data);
  }
}

void ensure_connection() {
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);

    delay(5000);
  }
  while(!client.connected()) {
    Serial.println("Connecting to server");
    client.connect(server, 9001);
  }
  Serial.println("connected to server");
}


void sendInt(uint32_t data) {
  client.write((data >> 8*3) & 0xFF);
  client.write((data >> 8*2) & 0xFF);
  client.write((data >> 8*1) & 0xFF);
  client.write(data & 0xFF);
}

void sendAck() {
  client.write(0x5);
}
