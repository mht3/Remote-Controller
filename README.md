# Remote-Controller

Telecommunications research project using the MQTT protocol. The goal of this project was to create a method to control a vehicle wirelessly. The MQTT protocol is a clean, fast solution to this problem. While this code does not control an actual vehicle, it simulates the vehicle with a GUI that copies how the joystick itself moves. 2 Raspberry pi's are used in this implemention. One is for the ground station remote controller and one will be used for onboard the vehicle. The ground station pi acts as a publisher and the central broker for the data.

This folder includes:

- Joystick (ground station) GUI that can be used with the up,down,left,right arrow keys as well as the 'w' 'a' 's' 'd' keys. 

- Reciever (vehicle) code that takes in the data sent by th joystick GUI and mimics th output

- Encryption techniques to make sure only verified users can control the joystick.

![image](https://user-images.githubusercontent.com/60635839/117226051-65a8c580-add9-11eb-8431-0fa3608ba539.png)


For more information, including how to run the code and set up a local broker, see **INSTRUCTIONS.md**

*A quick note: 

 In a real implementation, a vehicle's CAN bus system can take acceleration and deceleration signals as well as steering angle. Acceleration level is already sent over the MQTT line in this simulation, but the steering angle is not (since it is not needed to control the GUI). This code can be easily adapted to send the steering angle over the MQTT line since it is a variable (theta) in the code.


---

Created by Matt Taylor at the University of Illinois Spring 2021
