# Instructions

## Cloning The Repository

```
git clone https://github.com/mht3/Remote-Controller.git
cd Remote-Controller
```

## Installing Libraries

In this repository, several open source libraries are utilized. Many of these libraries are build into the default python library, but tkinter, paho-mqtt, and passlib likely are not installed. To install these run the following commands on terminal. Note that this is assuming the user is running on a linux system.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-tk

# If pip3 is not installed, install it with the command below.
sudo apt-get install python3-pip

# Install paho-mqtt library with pip3
sudo pip3 install paho-mqtt
```



