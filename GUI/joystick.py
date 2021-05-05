# imports
import tkinter 
import paho.mqtt.publish as publish
import math
import numpy as np
import csv
from getpass import getpass
# sudo apt-get install python-passlib
from passlib.hash import sha256_crypt

# Flag to turn off/on print statements
debug = False

# Initial Username and Password Requirements
def check_user(usernamePath="users.txt", passwordPath="passwords.txt"):
    '''
    Prompts the user for a username and password and chacks whether or not these are in their respective files.
    Usernames and passwords in users.txt and passwords.txt.

    ---Parameters---
    usernamePath : the filename for the list of usernames
    passwordPath : the filename for the list of passwords
    '''
    username = input("Username: ")
    password = getpass("Password: ")
    idx = findUsername(usernamePath, username)
    found_password = False
    if (idx >= 0):
        found_password = findPassword(passwordPath, password, idx)
    if idx >= 0 and found_password:
        print("Welcome, {}!".format(username))
        print("----------")
    else:
        print("Invalid Username or Password. Try again. \n")
        check_user()
    return username,password


def findUsername(fileName, username):
    '''
    Helper method for check_user().
    Parses the usernames text file and checks to see if the usernames match.

    --Parameters--
    fileName : the fileName for the list of usernames
    username : the username entered by the user

    --Returns--
    idx : the indexed position of where the username is in the file
    '''
    found_username = False
    idx = -1
    with open(fileName,"r") as user_file:
        line = user_file.readline()
        line = line.replace(" ","")
        usernames = line.split(',')
        for i in range(len(usernames)):
            if (username == usernames[i]):
                idx = i
                break
    user_file.close()
    return idx

def findPassword(fileName, password, idx):
    '''
    Helper method for check_user().
    Parses the usernames text file and checks to see if the passwords match.

    --Parameters--
    fileName : the fileName for the list of usernames
    password : the password entered by the user
    idx      : the indexed position of where the password should be in the file

    --Returns--
    found_password : boolean stating whether or not the password was found
    '''
    found_password = False
    with open(fileName,"r") as password_file:
        line = password_file.readline()
        line = line.replace(" ","")
        passwords = line.split(',')
        found_password = sha256_crypt.verify(password, passwords[idx])
    password_file.close()
    return found_password

# Initial setup

# Prompts user for username and password
username, password = check_user()

# Tkinter setup for GUI
width = 500
height = 500
dimensions = "{}x{}".format(width,height)
root = tkinter.Tk()
root.geometry(dimensions)
root.configure(bg='lightgrey')
root.title("Remote Controller")

# acceleration states: -3,-2,-1,0,1,2,3
# Global variable for the acceleration state of the controller.
accel_state = 0



# Tkinter joystick frame setup
frame_width = width/1.5
frame_height = height
joystick_x = frame_width/2
joystick_y = frame_height/2
radius = 40
frame_l = tkinter.Frame(root)
frame_l.pack(side=tkinter.LEFT)

# joystick tracking to send over mqtt line
# this is the r vector starting at the origin of joystick_x and joystick_y
r_x = 0.0
r_y = 0.0
theta = np.pi/2

# Variable for how responsive the turning is with left/right keyboard inputs
# A higher number represents a slower turn speed (small change in dtheta)
turn_speed = 80
dtheta = (2*np.pi)/turn_speed

# The current ring the joystick is on. (More clear once the program is ran)
curr_ring = 0

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

# Publish data through MQTT network!
def publishMovement(r_x, r_y, accel_state, theta):
    '''
    Publishes the joystick's x, y, and acceleration state data to the vehicle using the MQTT protocol.
    This method is called everytime an on key listener is pressed
    '''
    global username, password, debug, username, password
    if debug:
        print("X: {:.3f}\t Y: {:.3f}\t Accel: {}\t Theta: {:.3f}".format(r_x,r_y,accel_state,theta))
        print("Publishing controller data...")

    # dictionary of topics to send over the MQTT line
    data = ({'topic':"joystick/data/x", 'payload':r_x}, {'topic':"joystick/data/y", 'payload':r_y},
        {'topic':"joystick/data/accel", 'payload':accel_state})

    # authentication dictionary: uses username and password entered by the user on the CLI
    auth = {'username':username, 'password':password}

    # Published to the local Mosquitto broker. In this case it is my raspberry pi 4.
    publish.multiple(data, hostname="192.168.1.28", auth=auth)
    if debug:
        print("----------Done----------")
    
def getQuadrant(theta):
    '''
    Gets the current quadrant of theta
    '''
    quadrant = 1
    if ( theta >= 0 and theta <= np.pi/2 ):
        quadrant = 1
    elif ( theta <= np.pi):
        quadrant = 2
    elif ( theta <= 3*np.pi/2 ):
        quadrant = 3
    elif ( theta <= 2*np.pi):
        quadrant = 4
    return quadrant

def updateDeltas(state, rd):
    '''
    Updates the dx and dy variables (change in joystick position) when accelerating.
    based off the current quadrant of theta.

    --Parameters--
    state : either "UP" or "DOWN" (from the on key listeners up arrow key/down arrow key)
    rd    : the radius differential between the current ring and the ring we're trying to get to
    '''
    global theta
    rd = abs(rd)
    quadrant = getQuadrant(theta)
    dx = 0
    dy = 0
    # New theta normalized depending on quadrant
    alpha = theta
    if ( quadrant == 2):
        alpha = np.pi - theta
    elif ( quadrant == 3 ):
        alpha = theta - np.pi
    elif ( quadrant == 4 ):
        alpha = 2*np.pi - theta

    if (state == "UP"):
        if (quadrant == 1 or quadrant == 3):
            dx = rd*np.cos(alpha)
            dy = -rd*np.sin(alpha)
        else:
            # quadrant 2 or 4
            dx = -rd*np.cos(alpha)
            dy = -rd*np.sin(alpha)
    else:
        if (quadrant == 1 or quadrant == 3):
            dx = -rd*np.cos(alpha)
            dy = rd*np.sin(alpha)
        else:
            # quadrant 2 or 4
            dx = rd*np.cos(alpha)
            dy = rd*np.sin(alpha)

    return (dx,dy)

def upAccel():
    '''
    Increases the acceleration state and updates the graphics
    '''
    global accel_state
    if (accel_state < 3):
        accel_state = accel_state + 1
        updateAccelGraphics()

def downAccel():
    '''
    Decreases the acceleration state and updates the graphics
    '''
    global accel_state
    if (accel_state > -3):
        accel_state = accel_state - 1
        updateAccelGraphics()

def updateAccelGraphics():
    '''
    updates the acceleration graphics by coloring the upper acceleration levels light green
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

def checkThetaBounds(state):
    '''
    Checks the bounds of theta.
    For this joystick, it can ONLY travel from 15 degrees to 165 degrees in the upper half 
    and from 195 degrees to 345 degrees on the lower half.

    ---Parameters---
    state : the state (either "LEFT" or "RIGHT") for when the left/right arrow keys are pressed
    '''
    global accel_state, theta, dtheta
    theta_temp = theta
    if (state == "LEFT"):
        if accel_state > 0:
            theta_temp = theta + dtheta
        elif accel_state < 0:
            theta_temp = theta_temp - dtheta
    else:
        if accel_state > 0:
            theta_temp = theta_temp - dtheta
        elif accel_state < 0:
            theta_temp = theta_temp + dtheta

    isUp = accel_state > 0
    isDown = accel_state < 0
    #Upper and lower bounds have range of 120 degrees (60 degrees on each size of x = 0 line)
    thetaUpBounds = (theta_temp > (np.pi/12)) and (theta_temp < (11*np.pi/12))
    thetaDownBounds = (theta_temp > (13*np.pi/12)) and (theta_temp < (23*np.pi/12))
    upBound = isUp and thetaUpBounds
    downBound = isDown and thetaDownBounds
    return (upBound or downBound)

def onKeyUp():
    '''
    On key listener method for the up arrow and w key.
    Updates the accel state as well as dx and dy.
    Publishes data to the Vehicle
    '''
    global accel_state, r_x, r_y, ring_1_radius, ring_2_radius, ring_3_radius, curr_ring, theta

    # the current radius differential
    rd = 0
    if (accel_state == 0 or accel_state == -1):
        if (accel_state == 0):
            curr_ring = ring_1_radius
            theta = np.pi/2
        else:
            curr_ring = 0

        rd = -ring_1_radius
    elif (accel_state == 1 or accel_state == -2):
        if (accel_state == 1):
            curr_ring = ring_2_radius
        else:
            curr_ring = ring_1_radius

        rd = -(ring_2_radius-ring_1_radius)
    elif (accel_state == 2 or accel_state == -3):
        if (accel_state == 2):
            curr_ring = ring_3_radius
        else:
            curr_ring = ring_2_radius
        
        rd = -(ring_3_radius-ring_2_radius)

    dx,dy = updateDeltas("UP",rd)

    if (((r_y-dy)**2 + (r_x+dx)**2) <= ring_3_radius**2):
        upAccel()
        if accel_state == 0:
            reset()
        else:
            r_y = r_y - dy
            r_x = r_x + dx
            canvas.move(joystick,dx,dy)
            publishMovement(r_x, r_y, accel_state, theta)

def onKeyDown():
    '''
    On key listener method for the down arrow and s key.
    Updates the accel state as well as dx and dy.
    Publishes data to the Vehicle
    '''
    global accel_state, r_x, r_y, ring_1_radius, ring_2_radius, ring_3_radius, curr_ring, theta

    # the current radius differential
    rd = 0
    if (accel_state == 0 or accel_state == 1):
        if (accel_state == 0):
            curr_ring = ring_1_radius
            theta = 3*np.pi/2
        else:
            curr_ring = 0

        rd = ring_1_radius
    elif (accel_state == -1 or accel_state == 2):
        if (accel_state == -1):
            curr_ring = ring_2_radius
        else:
            curr_ring = ring_1_radius

        rd = (ring_2_radius-ring_1_radius)
    elif (accel_state == -2 or accel_state == 3):
        if (accel_state == -2):
            curr_ring = ring_3_radius
        else:
            curr_ring = ring_2_radius

        rd = (ring_3_radius-ring_2_radius)

    dx,dy = updateDeltas("DOWN",rd)

    if (((r_y-dy)**2 + (r_x+dx)**2) <= ring_3_radius**2):
        downAccel()
        if accel_state == 0:
            reset()
        else:
            r_y = r_y - dy
            r_x = r_x + dx
            canvas.move(joystick,dx,dy)
            publishMovement(r_x, r_y, accel_state, theta)

def onKeyLeft():
    '''
    On key listener method for the left arrow and 'a' key.
    Updates theta, dx, and dy.
    Publishes data to the Vehicle
    '''
    global accel_state, r_x, r_y, ring_3_radius, curr_ring, theta, dtheta
    state = "LEFT"
    isWithinBounds = checkThetaBounds(state)
    if (isWithinBounds):
        if accel_state > 0:
            theta = theta + dtheta
        elif accel_state < 0:
            theta = theta - dtheta
        dx = curr_ring*np.cos(theta) - r_x
        dy = -curr_ring*np.sin(theta) + r_y
        if (((r_y-dy)**2 + (r_x+dx)**2) <= ring_3_radius**2):
            r_x = r_x + dx
            r_y = r_y - dy
            canvas.move(joystick,dx,dy)
            publishMovement(r_x, r_y, accel_state, theta)


def onKeyRight():
    '''
    On key listener method for the right arrow and 'd' key.
    Updates theta, dx, and dy.
    Publishes data to the Vehicle
    '''
    global accel_state, r_x, r_y, ring_3_radius, curr_ring, theta, dtheta
    state = "RIGHT"
    isWithinBounds = checkThetaBounds(state)
    if (isWithinBounds):
        if accel_state > 0:
            theta = theta - dtheta
        elif accel_state < 0:
            theta = theta + dtheta

        dx = curr_ring*np.cos(theta) - r_x
        dy = -curr_ring*np.sin(theta) + r_y
        if (((r_y-dy)**2 + (r_x+dx)**2) <= ring_3_radius**2):
            r_x = r_x + dx
            r_y = r_y - dy
            canvas.move(joystick,dx,dy)
            publishMovement(r_x, r_y, accel_state, theta)

def reset():
    '''
    Press 'r' to reset the joystick to its original state
    Published data to the Vehicle
    '''
    global accel_state, r_x, r_y, theta
    accel_state = 0
    updateAccelGraphics()
    theta = 0
    canvas.move(joystick, -r_x, r_y)
    r_x = 0
    r_y = 0
    publishMovement(r_x, r_y, accel_state, theta)


def wasd(event):
    '''
    On key listeners for wasd keys
    '''
    if (event.char == 'w'): 
        onKeyUp()

    if (event.char == 'a'): 
        onKeyLeft()

    if (event.char == 's'): 
        onKeyDown()

    if (event.char == 'd'): 
        onKeyRight()

    # reset to original state
    if (event.char == 'r'): 
        reset()
     
    

def left(event):
    '''
    What to do when the left arrow key is pressed. (Built in tkinter event)
    '''
    onKeyLeft()

def right(event):
    '''
    What to do when the right arrow key is pressed. (Built in tkinter event)
    '''
    onKeyRight()
    
def up(event):
    '''
    What to do when the up arrow key is pressed. (Built in tkinter event)
    '''
    onKeyUp()
    
def down(event):
    '''
    What to do when the down arrow key is pressed. (Built in tkinter event)
    '''
    onKeyDown()
    
# Binds the keys pressed to their respective on key listeners
root.bind("<Key>", wasd)
root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)

# keeps the tkinter window running indefinitely
# Press crtl+c to stop
root.mainloop()