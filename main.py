# See https://www.python-course.eu/tkinter_canvas.php

import numpy as np
import cv2
from tkinter import *
from PIL import ImageTk
from PIL import Image

labels = ["Line","Circle","Rectangle","Annotation","Pixel"]
selection_info = {
    "number":0, # Which label is currently highlighted
    "first_x":0, # For selections that require clicking twice, the first x and y coordinates of the click are recorded if necessary
    "first_y":0,
    "clicked_once":0 # If applicable, a 1 indicates that the user has clicked once.
}

master = Tk()
master.title("OpenCV image manipulation")

def add_dashboard(img):
    extra_rows = 255*np.ones([100,len(img[0]),3], dtype=np.uint8) # Note: OpenCV requires 8 bit integers for pixel arrays.
    img = np.concatenate((img,extra_rows))
    for i in range(len(labels)):
        x_start = int(i*(len(img[0])/len(labels))+15)
        y_start = int(len(img)-60)
        cv2.putText(img, labels[i], (x_start, y_start), cv2.FONT_HERSHEY_PLAIN, 1.3, (0,0,0), 1, cv2.LINE_AA);
    cv2.rectangle(
        img,
        (int(selection_info["number"]*(len(img[0])/len(labels)))+2, int(len(img)-98)),
        (int((selection_info["number"]+1)*(len(img[0])/len(labels)))-2, int(len(img)-2)),
        (128, 128, 128),
        thickness=3,
        lineType=cv2.LINE_8
    )
    return img

# Put in the picture
saturn = cv2.cvtColor(cv2.imread("saturn.png"), cv2.COLOR_BGR2RGB)
saturn_back = [np.copy(saturn)] # Treating this secondary image as an array of 1 was necessary for it to be responsive as a global variable.
img = add_dashboard(saturn)

# Canvas
canvas_height, canvas_width, no_channels = img.shape
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

# Convert the Image object into a TkPhoto object
im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)
label = Label(image=imgtk)
label.image = imgtk
# Put it in the display window
image_id = w.create_image(0, 0, image=imgtk, anchor=NW)

# Mouse stuff

def new_selection(x,y):
    selection_info["number"] = int(len(labels)*x/len(saturn[0]))
    selection_info["clicked_once"] = 0
    saturn_back[0] = np.copy(saturn)

def mouse_click(event):
    x = event.x
    y = event.y
    if y<len(saturn):
        paint_operation(x,y)
    else:
        new_selection(x,y)
    # Convert the Image object into a TkPhoto object
    if selection_info["clicked_once"] == 0:
        img = add_dashboard(saturn)
    else:
        img = add_dashboard(saturn_back[0])
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
    label.image = imgtk
    label.pack
    # Put it in the display window
    w.itemconfig(image_id, image=imgtk)
    
def first_click(x,y):
    selection_info["clicked_once"] = 1
    selection_info["first_x"] = x
    selection_info["first_y"] = y
    cv2.line(
        saturn_back[0],
        (x, y),
        (x, y),
        (255, 255, 255),
        thickness=5,
        lineType=cv2.LINE_AA
    );
    
def add_line(x,y):
    if selection_info["clicked_once"] == 0:
        first_click(x,y)
        return
    else:
        cv2.line(
            saturn,
            (selection_info["first_x"], selection_info["first_y"]),
            (x, y),
            (255, 0, 255),
            thickness=5,
            lineType=cv2.LINE_AA
        );
        saturn_back[0] = np.copy(saturn)
        selection_info["clicked_once"] = 0
        
def add_circle(x,y):
    if selection_info["clicked_once"] == 0:
        first_click(x,y)
        return
    else:
        radius = int(( (selection_info["first_x"]-x)**2 + (selection_info["first_y"]-y)**2 )**0.5)
        cv2.circle(
            saturn,
            (selection_info["first_x"], selection_info["first_y"]),
            radius,
            (0, 255, 255),
            thickness=5,
            lineType=cv2.LINE_AA
        );
        saturn_back[0] = np.copy(saturn)
        selection_info["clicked_once"] = 0
        
def add_rectangle(x,y):
    if selection_info["clicked_once"] == 0:
        first_click(x,y)
        return
    else:
        cv2.rectangle(
            saturn,
            (selection_info["first_x"], selection_info["first_y"]),
            (x,y),
            (255, 255, 0),
            thickness=5,
            lineType=cv2.LINE_AA
        );
        saturn_back[0] = np.copy(saturn)
        selection_info["clicked_once"] = 0
        
def add_text(x,y):
    img = cv2.putText(saturn, "Saturn", (x,y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
    saturn_back[0] = np.copy(saturn)
    
def pixel_manipulation(x,y):
    for i in range(-20, 20):
        for j in range(-20, 20):
            if x+i >= 0 and x+i < len(saturn[0]) and y+j >= 0 and y+j < len(saturn):
                color_red = int(255*(i+20)/39)
                color_blue = int(255*(j+20)/39)
                saturn[y+j][x+i] = [color_red,0,color_blue]
    
def paint_operation(x,y):
    if selection_info["number"] == 0: # Line
        add_line(x,y)
    if selection_info["number"] == 1: # Circle
        add_circle(x,y)
    if selection_info["number"] == 2: # Rectangle
        add_rectangle(x,y)
    if selection_info["number"] == 3: # Text
        add_text(x,y)
    if selection_info["number"] == 4: # Pixel manipulation
        pixel_manipulation(x,y)    
    
master.bind("<Button-1>", mouse_click)

mainloop()
