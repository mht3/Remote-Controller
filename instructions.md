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

## Setting up a Local Broker
If you've already done this step, you can move on to the next step. Just make sure the IP address for your specific device is correct in the publisher and subscriber code.

**Step 1**: Find your raspberry pi'a IP address (or equivalent microcomputer) and change it to a static IP. This has to be done on every new network the device comes in contact with but is extremely beneficial and saves a lot of time. The your device isn't always guaranteed to have the same IP address everytime it connects to your router. This causes issues when setting up a local Mosquitto broker and can be easily resolved by going to your router's settings. A fantastic example of how to do this can be seen in the link attached below.

https://www.asus.com/support/FAQ/114068/#:~:text=Step%201%3A%20Launch%20a%20browser,menu%20on%20the%20left%20panel.&text=Step%203%3A%20Under%20the%20Basic,%22Enable%20Manual%20Assignment%22%20items.

**Step 2**: Install the mosquitto livrary

```

```




