#include <stdint.h>
#include <Arduino.h>
#include <WiFi.h>
#include <SPI.h>

#define MAXMESSAGE 255
#define INTERVAL 5000

struct sensor {
  uint32_t id;
  uint8_t type;
  uint8_t pin;
};

struct config {
  uint8_t numSensors;
  struct sensor* sensors;
};

struct data_package {
  uint32_t deviceID;
  uint8_t numSensors;
  struct sensor_data* sensor_datas;
};

struct sensor_data {
  uint32_t id;
  uint32_t data;
};

enum MESSAGE_TYPE {reg, config, sensor_data, error, ack};

void ensure_connection();
MESSAGE_TYPE decode_message(void* buffer);
void sendReg();
void sendData();
void sendAck();
void sendInt(uint32_t data);
void init_config();
struct sensor_data* read_data();

uint32_t combine_int(uint8_t* in);
