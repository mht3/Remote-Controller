'''
Paho Library Link: https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
'''
from paho.mqtt import client as mqtt
r_x = 0.0
r_y = 0.0
accel_state = 0
theta = 0.0
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # From Paho Website: Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print("Connected with result code " + str(rc))
    print("----------")
    # TODO Make command line interface to ask for username and password
    subs = [("joystick/data/x",0), ("joystick/data/y",0),("joystick/data/accel",0),("joystick/data/theta",0)]
    client.subscribe(subs)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    global r_x,r_y,accel_state,theta    
    print("Collecting " + str(message.topic) + " ...")
    if (message.topic == "joystick/data/x"):
        r_x = float(message.payload)
    elif (message.topic == "joystick/data/y"):
        r_y = float(message.payload)
    elif (message.topic == "joystick/data/accel"):
        accel_state = int(message.payload)
    elif (message.topic == "joystick/data/theta"):
        theta = float(message.payload)
        # Last message recieved so print everything
        print_data()
        print("----------")



# Callback for when there is a disconnect
def on_disconnect(client, userdata, rc):
    #rc indicates the disconnection state. rc = 0 means that the callback was called in response to a disconnect() call
    if (rc != 0):
        print("Unexpected disconnection.")


def print_data():
    global r_x,r_y,accel_state,theta    
    print("X: {:.3f}\t Y: {:.3f}\t Accel: {}\t Theta: {:.3f}".format(r_x,r_y,accel_state,theta))


# Create a new client with defaults
# Default constructor is: Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client = mqtt.Client()

# Tells client what to do once connected
client.on_connect = on_connect

# Tells client what to do once a message is recieved
client.on_message =  on_message

# Tells client what to do on disconnect
client.on_disconnect = on_disconnect

# Connects to the mosquitto broker with default port and keepalive configurations

# TODO Read a username password file and add correct users.
client.username_pw_set(username="admin",password="admin")
client.connect(host="192.168.1.130", port=1883, keepalive=60)

# loop forever (handles reconnecting)
client.loop_forever()

