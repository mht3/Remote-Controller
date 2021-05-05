# Instructions

## Cloning The Repository

```
git clone https://github.com/mht3/Remote-Controller.git
cd Remote-Controller
```

## Installing Libraries

In this repository, several open source libraries are utilized. Many of these libraries are build into the default python library, but tkinter, paho-mqtt, numpy, and passlib likely are not installed. To install these run the following commands on terminal. Note that this is assuming the user is running on a linux system.

First, Make sure everything is up to date

```sudo apt-get update```

Optional:

```sudo apt-get upgrade```

Here are the very important installations to get the code running:

```
sudo apt-get install python3-tk
sudo apt-get install python3-passlib
sudo apt-get install python3-numpy

# If pip3 is not installed, install it with the following:
sudo apt-get install python3-pip

sudo pip3 install paho-mqtt
```



