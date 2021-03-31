from tkinter import *
import paho.mqtt.publish as publish
import math
import numpy as np

# Initial setup
width = 500
height = 500
dimensions = "{}x{}".format(width,height)
root = Tk()
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
frame_l = Frame(root)
frame_l.pack(side=LEFT)

# joystick tracking to send over mqtt line
# this is the r vector starting at the origin of joystick_x and joystick_y
r_x = 0.0
r_y = 0.0
theta = np.pi/2
dtheta = (2*np.pi)/80

#joystick canvas
canvas = Canvas(frame_l, height=frame_height, width =frame_width, bg='lightgray')
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
canvas_r = Canvas(root, height=canvas_r_height, width = canvas_r_width, bg='lightgrey')
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
canvas_r.pack(side=LEFT)

# Publish to through MQTT network!
def publishMovement(r_x, r_y, accel_state, theta):
    print("X: {:.3f}\t Y: {:.3f}\t Accel: {}\t Theta: {:.3f}".format(r_x,r_y,accel_state,theta))
    print("Publishing controller data...")
    data = ({'topic':"joystick/data/x", 'payload':r_x}, {'topic':"joystick/data/y", 'payload':r_y},
        {'topic':"joystick/data/accel", 'payload':accel_state}, {'topic':"joystick/data/theta", 'payload':theta})
    publish.multiple(data, hostname="test.mosquitto.org")
    print("----------Done----------")

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
    thetaUpBounds = (theta_temp > (np.pi/6)) and (theta_temp < (5*np.pi/6))
    thetaDownBounds = (theta_temp > (7*np.pi/6)) and (theta_temp < (11*np.pi/6))
    upBound = isUp and thetaUpBounds
    downBound = isDown and thetaDownBounds
    return (upBound or downBound)

def onKeyUp():
    global accel_state, r_x, r_y, ring_1_radius, ring_2_radius, ring_3_radius, curr_ring, theta
    dx = 0.0
    dy = 0.0
    
    if (accel_state == 0 or accel_state == -1):
        if (accel_state == 0):
            curr_ring = ring_1_radius
        else:
            curr_ring = 0

        dy = -ring_1_radius
    elif (accel_state == 1 or accel_state == -2):
        if (accel_state == 1):
            curr_ring = ring_2_radius
        else:
            curr_ring = ring_1_radius

        dy = -(ring_2_radius-ring_1_radius)
    elif (accel_state == 2 or accel_state == -3):
        if (accel_state == 2):
            curr_ring = ring_3_radius
        else:
            curr_ring = ring_2_radius
        
        dy = -(ring_3_radius-ring_2_radius)
    if (((r_y-dy)**2 + r_x**2) <= ring_3_radius**2):
        upAccel()
        if (accel_state == 1): theta = np.pi/2
        if accel_state == 0:
            reset()
        else:
            r_y = r_y - dy
            canvas.move(joystick,dx,dy)
            publishMovement(r_x, r_y, accel_state, theta)

def onKeyDown():
    global accel_state, r_x, r_y, ring_1_radius, ring_2_radius, ring_3_radius, curr_ring, theta
    dx = 0.0
    dy = 0.0
    
    if (accel_state == 0 or accel_state == 1):
        if (accel_state == 0):
            curr_ring = ring_1_radius
        else:
            curr_ring = 0

        dy = ring_1_radius
    elif (accel_state == -1 or accel_state == 2):
        if (accel_state == -1):
            curr_ring = ring_2_radius
        else:
            curr_ring = ring_1_radius

        dy = (ring_2_radius-ring_1_radius)
    elif (accel_state == -2 or accel_state == 3):
        if (accel_state == -2):
            curr_ring = ring_3_radius
        else:
            curr_ring = ring_2_radius

        dy = (ring_3_radius-ring_2_radius)

    if (((r_y-dy)**2 + r_x**2) <= ring_3_radius**2):
        downAccel()
        if (accel_state == -1): theta = 3*np.pi/2
        if accel_state == 0:
            reset()
        else:
            r_y = r_y - dy
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
    theta = np.pi
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

