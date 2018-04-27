import json
from protocol import *

# These function are only for prototyping
def getDevice(ID):
    conf = Config(3)
    conf.sensors = []
    for i in range(0, 3):
        s = Sensor(123, 36, 1)
        conf.sensors.append(s)
    return conf

def storeData(DeviceID, dataPoints):
    print("Got data from " + str(DeviceID))
    print(dataPoints)

def createDevice(ID, Ip):
    data = None
    with open('./testData.json', 'r') as json_file:
        data = json.load(json_file)

    if getDevice(ID) == None:
        newDevice = {'id': ID, 'ip': Ip}
        data['devices'].append(newDevice)
    else:
        for device in data['devices']:
            if device['id'] == ID:
                device['ip'] == Ip

    with open('./testData.json', 'w') as json_file:
        json.dump(data, json_file)



