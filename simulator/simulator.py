import socket
import sys
sys.path.append('../server')
from protocol import *

HOST, PORT = "127.0.0.1", 9001
if len(sys.argv) > 1:
    HOST = sys.argv[1]

conf = None

ID = None
while ID == None:
    try:
        ID=int(input('Device ID:'))
    except ValueError:
        print("Not a number")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while conf == None:
    reg = Register(ID)
    print(type(reg))
    sock.sendall(encode_message(message_type['REGISTER'], reg))
    received = decode_message(sock.recv(1024))
    if received['type'] == message_type['CONFIG']:
        print("New conf")
        conf = received['config']
        print(conf)
        sock.sendall(encode_message(message_type['ACK'], reg))
    elif received['type'] == message_type['ACK']:
        print("No config")
    elif received['type'] == message_type['ERROR']:
        print("Error")
        Reg()
    else:
        sock.sendall(encode_message(message_type['ERROR'], reg))

sock.close()

while True:
    print("Choose option")
    print("(0) Send data")
    print("(1) Exit program")
    option = None
    while option == None:
        try:
            option = int(input("\n"))
        except:
            print("Not a valid option")

    if option == 0:
        dp = []
        for s in conf.sensors:
            sd = None
            while sd == None:
                try:
                    sd = int(input("Input sensordata: "))
                except:
                    print("Not a valid number. Try again")
            dp.append({'sensorID':s.sensorID, 'sensorData':sd})
        s = SensorData(ID, conf.numSensors, dp)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ack = False

        while ack == False:
            sock.connect((HOST, PORT))
            sock.sendall(encode_message(message_type['DATA'], s))
            received = decode_message(sock.recv(1024))
            if received['type'] == message_type['CONFIG']:
                conf = received['config']
                sock.sendall(encode_message(message_type['ACK'], reg))
                ack = True
            elif received['type'] == message_type['ACK']:
                ack = True

        sock.close()
    else:
        sys.exit(0)

