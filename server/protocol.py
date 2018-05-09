import socket
from enum import Enum

message_type = {
        'REGISTER': 1,
        'CONFIG': 2,
        'DATA': 3,
        'ERROR': 4,
        'ACK': 5}

def send_message(m_type, data, socket):
    socket.sendall(encode_message(m_type,data))
    received = sock.recv(1024)
    return decode_message(received)


def encode_message(m_type, in_data):
    data = bytearray()
    data.extend(m_type.to_bytes(1, byteorder='big'))
    if m_type == message_type['CONFIG'] or m_type == message_type['DATA'] or m_type == message_type['REGISTER'] :
        data.extend(in_data.toBytes())
    return data

def decode_message(raw_data):
    message = {}
    if raw_data[0] < 6 and raw_data[0] > 0:
        message['type'] = raw_data[0]
    else:
        return None

    if message['type'] == message_type['REGISTER']:
        message['deviceID'] = int.from_bytes(raw_data[1:5], byteorder='big')

    if message['type'] == message_type['CONFIG']:
        c = Config()
        message['config'] = c.fromBytes(raw_data[1:])

    if message['type'] == message_type['DATA'] :
        d = SensorData()
        message['data'] = d.fromBytes(raw_data[1:])

    return message

class Sensor:
    def __init__(self, sensorID=None, pin=None, sensorType=None):
        self.sensorID = sensorID
        self.pin = pin
        self.sensorType = sensorType

    def fromBytes(self, data):
        self.sensorID = int.from_bytes(data[0:4], byteorder='big')
        self.sensorType = data[4]
        self.pin = data[5]
        return self

    def toBytes(self):
        data = bytearray()
        data.extend(self.sensorID.to_bytes(4, byteorder='big'))
        data.extend(self.sensorType.to_bytes(1, byteorder='big'))
        data.extend(self.pin.to_bytes(1, byteorder='big'))
        return data

    def __str__(self):
        ret = "Id: " + str(self.sensorID) + ", "
        ret += "Pin: " + str(self.pin) + ", "
        ret += "Type: " + str(self.sensorType)
        return ret


class Config:
    def __init__(self, numSensors=None, sensors=None):
        self.numSensors = numSensors
        self.sensors = sensors

    def fromBytes(self, data):
        self.numSensors = data[0]
        self.sensors = []
        for i in range(0, self.numSensors):
            offset = (i*6) + 1
            s = Sensor()
            self.sensors.append(s.fromBytes(data[offset:offset+6]))
        return self

    def toBytes(self):
        data = bytearray()
        data.extend(self.numSensors.to_bytes(1, byteorder='big'))
        for sensor in self.sensors:
            data.extend(sensor.toBytes())
        return data

    def __str__(self):
        ret =  "Number of sensors: " + str(self.numSensors) + "\n"
        for s in self.sensors:
            ret += str(s) + "\n"
        return ret

class SensorData:
    def __init__(self, deviceID=None, numSensors=None, dataPoints=None):
        self.deviceID = deviceID
        self.numSensors = numSensors
        self.dataPoints = dataPoints

    def fromBytes(self, data):
        self.deviceID = int.from_bytes(data[0:4], byteorder='big')
        self.numSensors = data[4]
        self.dataPoints = []
        for i in range(0, self.numSensors):
            offset = (i*8) + 5
            dp = {}
            dp['sensorID'] = int.from_bytes(data[offset:offset+4], byteorder='big')
            dp['sensorData'] = int.from_bytes(data[offset+4:offset+8], byteorder='big')
            self.dataPoints.append(dp)
        return self

    def toBytes(self):
        data = bytearray()
        data.extend(self.deviceID.to_bytes(4, byteorder='big'))
        data.extend(self.numSensors.to_bytes(1, byteorder='big'))
        for dp in self.dataPoints:
            data.extend(dp['sensorID'].to_bytes(4, byteorder='big'))
            data.extend(dp['sensorData'].to_bytes(4, byteorder='big'))
        return data

class Register:
    def __init__(self, deviceID = None):
        self.deviceID = deviceID

    def fromBytes(self, data):
        self.deviceID = int.from_bytes(data[0:4], byteorder='big')
        return self

    def toBytes(self):
        data = bytearray()
        data.extend(self.deviceID.to_bytes(4, byteorder='big'))
        return data



