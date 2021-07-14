# Desired features:
# - Lines (See Lesson 3 of the OpenCV course)
# - Circles (Lesson 3)
# - Rectangles (Lesson 3)
# - Text annovation (Lesson 3)
# - Pixel manipulation (Lesson 2)

# - Aside from the regular image, some text or icons at the bottom that allows switching between the five modes.
# - Two clicks for rectangles, lines, maybe circles
# - A separate staging image that shows the intermediate steps for the two click items.
# - For text annotation, maybe just the same message always, or a random message, or something that doesn't involve additional input.
# - For pixel manipulation, maybe draw a rainbow square. Just something to show pixel manipulation in a way that can't obviously be done with other functions.

# See https://www.python-course.eu/tkinter_canvas.php

import numpy as np
import cv2
from tkinter import *
from PIL import ImageTk
from PIL import Image

labels = ["Line","Circle","Rectangle","Annotation","Pixel"]
selection_number = [0] # Which option at the bottom is selected

master = Tk()

def add_dashboard(img):
    extra_rows = 255*np.ones([100,len(img[0]),3], dtype=np.uint8)
    img = np.concatenate((img,extra_rows))
    for i in range(len(labels)):
        x_start = int(i*(len(img[0])/len(labels))+15)
        y_start = int(len(img)-60)
        cv2.putText(img, labels[i], (x_start, y_start), cv2.FONT_HERSHEY_PLAIN, 1.3, (0,0,0), 1, cv2.LINE_AA);
    cv2.rectangle(
        img,
        (int(selection_number[0]*(len(img[0])/len(labels)))+2, int(len(img)-98)),
        (int((selection_number[0]+1)*(len(img[0])/len(labels)))-2, int(len(img)-2)),
        (255, 0, 255),
        thickness=3,
        lineType=cv2.LINE_8
    )
    return img

# Put in the picture
saturn = cv2.cvtColor(cv2.imread("saturn.png"), cv2.COLOR_BGR2RGB)
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

def mouse_click(event):
    x = event.x
    y = event.y
    if y<len(saturn):
        paint_operation(x,y)
    else:
        selection_number[0] = int(len(labels)*x/len(saturn[0]))
    # Convert the Image object into a TkPhoto object
    img = add_dashboard(saturn)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
    label.image = imgtk
    label.pack
    # Put it in the display window
    w.itemconfig(image_id, image=imgtk)
    
def paint_operation(x,y):
    if selection_number[0] == 3:
        img = cv2.putText(saturn, "Saturn", (x,y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
    else:
        cv2.line(saturn, (x-20, y-20), (x+20, y+20), (255, 0, 255), thickness=5, lineType=cv2.LINE_AA);
    
master.bind("<Button-1>", mouse_click)

mainloop()
