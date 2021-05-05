# Instructions

## Cloning The Repository

```
$ git clone https://github.com/mht3/Remote-Controller.git
$ cd Remote-Controller
```

## Installing Libraries

In this repository, several open source libraries are utilized. Many of these libraries are build into the default python library, but tkinter, paho-mqtt, numpy, and passlib likely are not installed. To install these run the following commands on terminal. Note that this is assuming the user is running on a linux system.

First, Make sure everything is up to date

```$ sudo apt-get update```

Optional:

```$ sudo apt-get upgrade```

Here are the very important installations to get the code running:

```
$ sudo apt-get install python3-tk
$ sudo apt-get install python3-passlib
$ sudo apt-get install python3-numpy

# If pip3 is not installed, install it with the following:
$ sudo apt-get install python3-pip

$ sudo pip3 install paho-mqtt
```

## Setting up a Local Broker with Mosquitto
If you've already done this step, you can move on to the next step. Just make sure the IP address for your specific device is correct in the publisher and subscriber code.

### **Step 1**: Setting up a static IP
Find your raspberry pi'a IP address (or equivalent microcomputer) and change it to a static IP. This has to be done on every new network the device comes in contact with but is extremely beneficial and saves a lot of time. Your device isn't always guaranteed to have the same IP address everytime it connects to your router. This causes issues when setting up a local Mosquitto broker and can be easily resolved by going to your router's settings. A fantastic example of how to do this can be seen in the link attached below. In this library the IP address of the local broker was just ```192.168.1.28```.

https://www.asus.com/support/FAQ/114068/#:~:text=Step%201%3A%20Launch%20a%20browser,menu%20on%20the%20left%20panel.&text=Step%203%3A%20Under%20the%20Basic,%22Enable%20Manual%20Assignment%22%20items.

### **Step 2**: Setup Mosquitto

More information on the Mosquitto library can be found here: https://mosquitto.org/. For our purposes, we just have to install the library and set the daemon to run on bootup.

```
$ sudo apt-get install mosquitto mosquitto-clients
$ sudo systemctl enable mosquitto
# To check if the broker is running: 
$ sudo systemctl status mosquitto
```

After running the above commands, the terminal should show that the mosquitto service is active.

### **Step 3**: Encryption
Setting up a username and password for the local broker is extremely important, especially when creating something like a remote controller. We only want authorized users to be able to connect to the broker to control the vehicle.

The first step is to add a password file to mosquitto's config file.

```
cd ~
cd /etc/mosquitto
sudo mosquitto_passwd -c passwordfile [username]
```

This should prompt the user for a password. Once this password is reentered, a new file named 'passwordfile' will be created with your hashed password inside.
To add/delete a user do the follwoing in the /etc/mosquitto directory:

```
# add a user:
$ sudo mosquitto_passwd -b passwordfile [username] [password]

#delete a user:
$ sudo mosquitto_passwd -D passwordfile [username]
```

Finally, you need to add the password file to the mosquitto configuration file.

```
$ sudo nano mosquitto.conf
```
Add 2 lines at the bottom of this file:

```
allow_anonymous false

password_file /etc/mosquitto/passwordfile
```
Congrats! You've set up a local Mosquitto broker.

## Adding authentication to the publisher and subscriber code

Now that the Mosquitto broker has an authentication system, your code needs to account for that. 

A great example is shown in the code I wrote for joystick.py and joystick_receiver.py.

There, I set the username to 'admin' and password to 'admin'. I know right, great, safe password! This must be the EXACT same as whatever the username and password is with the local broker.

Change directories to this repository, ie ```Remote-Controller```.

As you can see in users.txt and passwords.txt, I already have admin entered in. To add a new username, just edit the usernames.txt file with a , followed by your username. Ex ```admin,[nextUsername]```. Additionally, you need to create a password in the passwords file but that's a little more complicated. Luckily there's a file called hash_passwords.py already there for you. Run the following command:

```
$ python3 hash_passwords.py
```

This will teke the password you enter, automatically encrypt it using SHA-256 hashing, and automatically insert it into the passwords.txt file. Great!
