'''
Paho Library Link: https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
'''
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # From Paho Website: Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print("Connected with result code " + str(rc))
    print("----------")
    client.subscribe("joystick/data")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    print("Payload: {}".format(str(message.payload)))
    data = message.payload.split(',')

    r_x = float(data[0])
    r_y = float(data[1])
    accel_state = int(data[2])
    theta = float(data[3])

    print("X: {:.3f}\t Y: {:.3f}\t Accel: {}\t Theta: {:.3f}".format(r_x,r_y,accel_state,theta))

    print("----------")

# Callback for when there is a disconnect
def on_disconnect(client, userdata, rc):
    #rc indicates the disconnection state. rc = 0 means that the callback was called in response to a disconnect() call
    if (rc != 0):
        print("Unexpected disconnection.")


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
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

# loop forever (handles reconnecting)
client.loop_forever()

