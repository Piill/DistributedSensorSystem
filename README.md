# About

This part of the final project in 62596 Distribuerede systemer.
This specifically is the device server, an example device and a simulator. This connects to a server that handles the business logic.

## Server
The server resides in the server folder.

It's a simple tcp server in python.

## Device
The device is an ESP32 and uses platformIO and arduino for programming.
It needs a `info.h`, that contains the wifi information.

# TODO

- Add connection to business logic.
- Clean up mainloop in server
