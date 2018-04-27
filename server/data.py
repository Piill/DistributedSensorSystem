# These function are only for prototyping
def getDevice(ID):
    with open('./testData.json') as json_data:
        data = json.load(json_data)
        for device in data['devices']:
            if device['id'] == ID:
                return device
        return None

def createDevice(ID, Ip):
    data = None
    with open('./testData.json', 'r') as json_file:
        data = json.load(json_file)

    newDevice = {'id': ID, 'ip': Ip}
    data['devices'].append(newDevice)

    with open('./testData.json', 'w') as json_file:
        json.dump(data, json_file)


