import threading
import socket
import sys
import json
import time
from protocol import *
from data import *
from loggin import *


class ClientConnection(threading.Thread):
    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.socket = clientsocket

    def run(self):
        # self.request is the TCP socket connected to the client
        time.sleep(1)
        self.data = self.socket.recv(1024)
        message = decode_message(self.data)
        header = message['type']
        try:
            if message == None:
                self.socket.sendall(encode_message(message_type['ERROR'], None))
                return None

            if header == message_type['DATA']:
                print("Got data from device:")
                uploadData(message['data'])
                conf = getDevice(message['data'].deviceID)
                if conf == None:
                    return None
                self.socket.sendall(encode_message(message_type['CONFIG'], conf))
                time.sleep(1);
                self.data = self.socket.recv(1024)
                message = decode_message(self.data)
                if header != message_type['ACK']:
                    self.socket.sendall(encode_message(message_type['ERROR'], None))
                return None

            elif header == message_type['REGISTER']:
                conf = getDevice(message['deviceID'])
                if conf == None:
                    print("Got 'register', but no config is availeble for device")
                    self.socket.sendall(encode_message(message_type['ACK'], None))
                    return None
                print("Got 'register', sending config")
                self.socket.sendall(encode_message(message_type['CONFIG'], conf))
                time.sleep(1);
                self.data = self.socket.recv(1024)
                message = decode_message(self.data)
                if message['type'] != message_type['ACK']:
                    print("Send config, no ack")
                    self.socket.sendall(encode_message(message_type['ERROR'], None))
                else:
                    print("Ack recieved. device configured");
                return None

            else:
                self.socket.sendall(encode_message(message_type['ERROR'], None))
        except:
            print("Unexpected error:", sys.exc_info())


if __name__ == "__main__":

    HOST, PORT = "localhost", 9001
    if len(sys.argv) > 1:
        HOST = sys.argv[1]

    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serversocket.bind((HOST, PORT))
    # become a server socket
    serversocket.listen(5)

    print("Server on: " + HOST)

    while True:
        # accept connections from outside
        (clientsocket, address) = serversocket.accept()
        # now do something with the clientsocket
        # in this case, we'll pretend this is a threaded server
        ct = ClientConnection(clientsocket)
        ct.run()

