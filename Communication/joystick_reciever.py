'''
Paho Library Link: https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php
'''
from paho.mqtt import client as mqtt
import tkinter
import numpy as np

debug = False

r_x = 0.0
r_y = 0.0
accel_state = 0
new_r_x = 0.0
new_r_y = 0.0  
new_accel_state = 0

# ----- VEHICLE GRAPHICS SETUP -----
width = 500
height = 500
dimensions = "{}x{}".format(width,height)
root = tkinter.Tk()
root.geometry(dimensions)
root.configure(bg='lightgrey')
root.title("Vehicle")

# joystick frame setup. Same as in joystick.py
frame_width = width/1.5
frame_height = height
joystick_x = frame_width/2
joystick_y = frame_height/2
radius = 40
frame_l = tkinter.Frame(root)
frame_l.pack(side=tkinter.LEFT)

# Tkinter joystick canvas setup
canvas = tkinter.Canvas(frame_l, height=frame_height, width =frame_width, bg='lightgray')
canvas.grid(row=0,column=0)
ring_factor = 1.5
ring_1_radius = ring_factor*radius
ring_2_radius = ring_factor*ring_1_radius
ring_3_radius = ring_factor*ring_2_radius

# Creates the three rings and initializes the joystick to its center position
joystick_a1 = canvas.create_oval(joystick_x - ring_1_radius, joystick_y - ring_1_radius, joystick_x + ring_1_radius, joystick_y + ring_1_radius)
joystick_a2 = canvas.create_oval(joystick_x - ring_2_radius, joystick_y - ring_2_radius, joystick_x + ring_2_radius, joystick_y + ring_2_radius)
joystick_a3 = canvas.create_oval(joystick_x - ring_3_radius, joystick_y - ring_3_radius, joystick_x + ring_3_radius, joystick_y + ring_3_radius)
joystick = canvas.create_oval(joystick_x - radius, joystick_y - radius, joystick_x + radius, joystick_y + radius, fill="black")

# acceleration canvis graphics setup
# this takes up the right half of the GUI
canvas_r_width = width-frame_width
canvas_r_height = frame_height

# initializing 0 acceleration level graphic (The grey rectangle in the middle of the right hand side of the GUI)
rect_width = 60
rect_height = rect_width/3
canvas_r = tkinter.Canvas(root, height=canvas_r_height, width = canvas_r_width, bg='lightgrey')
zero_accel = canvas_r.create_rectangle(canvas_r_width/2 - rect_width/2,
    canvas_r_height/2 - rect_height/2, canvas_r_width/2 + rect_width/2,canvas_r_height/2 +rect_height/2, fill='grey', outline="")

# Upper acceleration level graphics
# Initializes the 3 rectangles above the 0 level acceleration. Colors them dark green indicating acceleration
shift = rect_height
space = 10
up_1_width = rect_width*0.8
up_1_height = rect_height*0.8
level_up_1 = canvas_r.create_rectangle(canvas_r_width/2 - up_1_width/2,
    canvas_r_height/2 - up_1_height/2 -  shift - space, canvas_r_width/2 + up_1_width/2,
    canvas_r_height/2 + up_1_height/2 - shift - space, fill='darkgreen', outline="")

up_2_width = up_1_width*0.8
up_2_height = up_1_height*0.8
level_up_2 = canvas_r.create_rectangle(canvas_r_width/2 - up_2_width/2,
    canvas_r_height/2 - up_2_height/2 -  2*(shift + 0.8*space), canvas_r_width/2 + up_2_width/2,
    canvas_r_height/2 + up_2_height/2 - 2*(shift + 0.8*space), fill='darkgreen', outline="")

up_3_width = up_2_width*0.8
up_3_height = up_2_height*0.8
level_up_3 = canvas_r.create_rectangle(canvas_r_width/2 - up_3_width/2,
    canvas_r_height/2 - up_3_height/2 -  3*(shift + 0.8*0.8*space), canvas_r_width/2 + up_3_width/2,
    canvas_r_height/2 + up_3_height/2 - 3*(shift + 0.8*0.8*space), fill='darkgreen', outline="")

# Lower acceleration level graphics
# Initializes the 3 rectangles below the 0 level acceleration. Colors them dark red indicating deceleration
level_down_1 = canvas_r.create_rectangle(canvas_r_width/2 - up_1_width/2,
    canvas_r_height/2 - up_1_height/2 + shift + space, canvas_r_width/2 + up_1_width/2,
    canvas_r_height/2 + up_1_height/2 + shift + space, fill='darkred', outline="")

level_down_2 = canvas_r.create_rectangle(canvas_r_width/2 - up_2_width/2,
    canvas_r_height/2 - up_2_height/2 +  2*(shift + 0.8*space), canvas_r_width/2 + up_2_width/2,
    canvas_r_height/2 + up_2_height/2 + 2*(shift + 0.8*space), fill='darkred', outline="")

level_down_3 = canvas_r.create_rectangle(canvas_r_width/2 - up_3_width/2,
    canvas_r_height/2 - up_3_height/2 +  3*(shift + 0.8*0.8*space), canvas_r_width/2 + up_3_width/2,
    canvas_r_height/2 + up_3_height/2 + 3*(shift + 0.8*0.8*space), fill='darkred', outline="")
canvas_r.pack(side=tkinter.LEFT)


def updateAccelGraphics():
    '''
    Updates the acceleration graphics by coloring the upper acceleration levels light green
    and lower acceleration levels light red.
    '''
    global accel_state
    global canvas_r
    if (accel_state == 3): 
        canvas_r.itemconfig(level_up_3,fill='lightgreen')
    elif (accel_state == 2):
        canvas_r.itemconfig(level_up_2,fill='lightgreen')
        canvas_r.itemconfig(level_up_3,fill='darkgreen')
    elif (accel_state == 1):
        canvas_r.itemconfig(level_up_1,fill='lightgreen')
        canvas_r.itemconfig(level_up_2,fill='darkgreen')
    elif (accel_state == 0):
        canvas_r.itemconfig(level_up_1,fill='darkgreen')
        canvas_r.itemconfig(level_down_1,fill='darkred')
        canvas_r.itemconfig(level_up_2,fill='darkgreen')
        canvas_r.itemconfig(level_down_2,fill='darkred')
        canvas_r.itemconfig(level_up_3,fill='darkgreen')
        canvas_r.itemconfig(level_down_3,fill='darkred')
    elif (accel_state == -1):
        canvas_r.itemconfig(level_down_1,fill='red')
        canvas_r.itemconfig(level_down_2,fill='darkred')
    elif (accel_state == -2):
        canvas_r.itemconfig(level_down_2,fill='red')
        canvas_r.itemconfig(level_down_3,fill='darkred')
    else:
        canvas_r.itemconfig(level_down_3,fill='red')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # From Paho Website: Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print("Connected with result code " + str(rc))
    print("----------")
    # data we are subscribing to with its respective QoS level. (Quality of Service levels are 0 for enhanced speed)
    subs = [("joystick/data/x",0), ("joystick/data/y",0),("joystick/data/accel",0)]
    client.subscribe(subs)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    global r_x, r_y, accel_state, canvas, joystick, new_r_x, new_r_y, new_accel_state, debug
    if debug:
        print("Collecting " + str(message.topic) + " ...")
    if (message.topic == "joystick/data/x"):
        new_r_x = float(message.payload)
    elif (message.topic == "joystick/data/y"):
        new_r_y= float(message.payload)
    elif (message.topic == "joystick/data/accel"):
        new_accel_state = int(message.payload)
        # Last message recieved so calculate everything
        dx = new_r_x - r_x
        dy = r_y - new_r_y
        r_x = new_r_x 
        r_y = new_r_y 
        canvas.move(joystick,dx,dy)
        if (new_accel_state != accel_state):
            accel_state = new_accel_state
            updateAccelGraphics()
        if debug:
            print_data()
            print("----------")



# Callback for when there is a disconnect
def on_disconnect(client, userdata, rc):
    #rc indicates the disconnection state. rc = 0 means that the callback was called in response to a disconnect() call
    if (rc != 0):
        print("Unexpected disconnection.")
    client.loop_stop()


def print_data():
    '''
    Debugger method for printing data recieved
    '''
    global r_x,r_y,accel_state   
    print("X: {:.3f}\t Y: {:.3f}\t Accel: {}".format(r_x,r_y,accel_state))

def findUsernames(fileName):
    '''
    Finds all of the usernames in the text file
    Currently unused in the program.
    '''
    usernames = []
    with open(fileName,"r") as user_file:
        line = user_file.readline()
        line = line.replace(" ","")
        usernames = line.split(',')
    user_file.close()
    return usernames

def findPasswords(fileName):
    '''
    Finds all of the passwords in the text file.
    Currently unused in the program.
    '''
    passwords = []
    with open(fileName,"r") as password_file:
        line = password_file.readline()
        line = line.replace(" ","")
        passwords = line.split(',')
    password_file.close()
    return passwords

# Initial setup

# Create a new client with defaults
# Default constructor is: Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client = mqtt.Client()

# Method to add allowed users to recieving side 
def add_user(subscriber_id=0, usernamePath="users.txt", passwordPath="passwords.txt"):
    global client
    # have the ability to find usernames and passwords, however the password file is hashed
    # usernames = findUsernames(usernamePath)
    # passwords = findPasswords(passwordPath)
    
    # Use the admin override. We don't care if someone can recieve our MQTT control messages, only who can send them/
    client.username_pw_set(username='admin',password='admin')

# Tells client what to do once connected
client.on_connect = on_connect

# Tells client what to do once a message is recieved
client.on_message =  on_message

# Tells client what to do on disconnect
client.on_disconnect = on_disconnect

# Unlocks the account so data can be recieved.
add_user()

# Connects to the local mosquitto broker with default port and keepalive configurations
client.connect(host="192.168.1.130", port=1883, keepalive=60)

# need loop_start() and not loop_forever() in order to have the GUI run in a loop
client.loop_start()
root.mainloop()

