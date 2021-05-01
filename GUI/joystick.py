import tkinter 
import paho.mqtt.publish as publish
import math
import numpy as np
import csv
from getpass import getpass

# sudo apt-get install python-passlib
from passlib.hash import sha256_crypt
debug = False
# Initial Username and Password Requirements
def check_user(usernamePath="users.txt", passwordPath="passwords.txt"):
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
    found_password = False
    with open(fileName,"r") as password_file:
        line = password_file.readline()
        line = line.replace(" ","")
        passwords = line.split(',')
        found_password = sha256_crypt.verify(password, passwords[idx])
    password_file.close()
    return found_password

# Initial setup
username, password = check_user()
width = 500
height = 500
dimensions = "{}x{}".format(width,height)
root = tkinter.Tk()
root.geometry(dimensions)
root.configure(bg='lightgrey')
root.title("Remote Controller")

#6 acceleration states: -3,-2,-1,0,1,2,3
# will send over mqtt line
accel_state = 0
turn_speed = 10
# joystick frame
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
dtheta = (2*np.pi)/80

#joystick canvas
canvas = tkinter.Canvas(frame_l, height=frame_height, width =frame_width, bg='lightgray')
canvas.grid(row=0,column=0)
ring_factor = 1.5
ring_1_radius = ring_factor*radius
ring_2_radius = ring_factor*ring_1_radius
ring_3_radius = ring_factor*ring_2_radius
curr_ring = 0

joystick_a1 = canvas.create_oval(joystick_x - ring_1_radius, joystick_y - ring_1_radius, joystick_x + ring_1_radius, joystick_y + ring_1_radius)
joystick_a2 = canvas.create_oval(joystick_x - ring_2_radius, joystick_y - ring_2_radius, joystick_x + ring_2_radius, joystick_y + ring_2_radius)
joystick_a3 = canvas.create_oval(joystick_x - ring_3_radius, joystick_y - ring_3_radius, joystick_x + ring_3_radius, joystick_y + ring_3_radius)
joystick = canvas.create_oval(joystick_x - radius, joystick_y - radius, joystick_x + radius, joystick_y + radius, fill="black")

# acceleration graphics
canvas_r_width = width-frame_width
canvas_r_height = frame_height

# initial 0 acceleration
rect_width = 60
rect_height = rect_width/3
canvas_r = tkinter.Canvas(root, height=canvas_r_height, width = canvas_r_width, bg='lightgrey')
zero_accel = canvas_r.create_rectangle(canvas_r_width/2 - rect_width/2,
    canvas_r_height/2 - rect_height/2, canvas_r_width/2 + rect_width/2,canvas_r_height/2 +rect_height/2, fill='grey', outline="")

# Upper acceleration levels

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

# Lower acceleration levels
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

# Publish to through MQTT network!
def publishMovement(r_x, r_y, accel_state, theta):
    global username, password, debug
    if debug:
        print("X: {:.3f}\t Y: {:.3f}\t Accel: {}\t Theta: {:.3f}".format(r_x,r_y,accel_state,theta))
        print("Publishing controller data...")
    data = ({'topic':"joystick/data/x", 'payload':r_x}, {'topic':"joystick/data/y", 'payload':r_y},
        {'topic':"joystick/data/accel", 'payload':accel_state})

    # TODO Make command line interface to ask for username and password
    auth = {'username':username, 'password':password}

    publish.multiple(data, hostname="192.168.1.130", auth=auth)
    if debug:
        print("----------Done----------")
    
def getQuadrant(theta):
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
    global accel_state
    if (accel_state < 3):
        accel_state = accel_state + 1
        updateAccelGraphics()

def downAccel():
    global accel_state
    if (accel_state > -3):
        accel_state = accel_state - 1
        updateAccelGraphics()

def updateAccelGraphics():
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
    global accel_state, r_x, r_y, theta
    accel_state = 0
    updateAccelGraphics()
    theta = 0
    canvas.move(joystick, -r_x, r_y)
    r_x = 0
    r_y = 0
    publishMovement(r_x, r_y, accel_state, theta)


# on click listeners
def wasd(event):

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
    onKeyLeft()

def right(event):
    onKeyRight()
    
def up(event):
    onKeyUp()
    
def down(event):
    onKeyDown()
    
root.bind("<Key>", wasd)
root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)


root.mainloop()