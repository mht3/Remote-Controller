# Remote-Controller

Telecommunications research project using the MQTT protocol. The goal of this project was to create a method to control a vehicle wirelessly. The MQTT protocol is a clean, fast solution to this problem. While this code does not control an actual vehicle, it simulates the vehicle with a graphics that copy how the joystick itself moves. 2 Raspberry pi's are used in this implemention. One is for the ground station and one will be used for onboard the vehicle. The ground station pi acts as a publisher and the central broker for the data. 

This folder includes:

- Joystick (ground station) GUI that can be used with the up,down,left,right arrow keys as well as the 'w' 'a' 's' 'd' keys. 

- Reciever (vehicle) code that takes in the data sent by th joystick GUI and mimics th output

- encryption techniques to make sure only verified users can control the joystick.

For more information on how to use this code, see instructions.md

Created by Matt Taylor at the University of Illinois Spring 2021
