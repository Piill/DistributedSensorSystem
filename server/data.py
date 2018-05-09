from zeep import Client
import sys
from protocol import *
import logging.config


def sensorFromServer(fromServer):
    sType = 0 if fromServer[3] == "DIGITAL" else 1
    return Sensor(int(fromServer[0]), int(fromServer[4]), sType)


# These function are only for prototyping
def getDevice(ID):
    client = Client("http://165.227.232.158:9902/SensorTcpService?wsdl")
    try:
        sensorIdList = client.service.get_Device_Sensors(ID)
        sensorList = []
        for sId in sensorIdList:
            sS = client.service.get_Sensor_Info(sId, 0)
            s = sensorFromServer(sS)
            sensorList.append(s)
        conf = Config(len(sensorList), sensorList)
        return conf
    except:
        print("Unexpected error when fetchin device from server:\n", sys.exc_info())
        return None

def uploadData(sd):

    client = Client("http://165.227.232.158:9902/SensorTcpService?wsdl")
    for dp in sd.dataPoints:
        print("Data point (Sensor Id, Data): " + str(dp['sensorID']) + ", " + str(dp['sensorData']))
        client.service.oploadData(dp['sensorID'], dp['sensorData'])


def createDevice(ID, Ip):
    data = None
    with open('./testData.json', 'r') as json_file:
        data = json.load(json_file)

    newDevice = {'id': ID, 'ip': Ip}
    data['devices'].append(newDevice)

    with open('./testData.json', 'w') as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    getDevice(1)
