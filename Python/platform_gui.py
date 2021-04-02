from tkinter import *
import math
import custom_tkinter_functions
import numpy as np

# Constants
screenWidth = 900
screenHeight = 900
sideLength = 600
margin = 120
centerRadius = 30
outlineRadius = sideLength
servoRingRadius = 20

# ======= Setting platform triangle points =======

# Point 1
x1 = screenWidth / 2
y1 = margin
p1 = np.array([x1, y1])

# Point 2
x2 = x1 - (sideLength*math.sin(math.radians(30)))
y2 = y1 + (sideLength*math.cos(math.radians(30)))
p2 = np.array([x2, y2])

# Point 3
x3 = x1 + (sideLength*math.sin(math.radians(30)))
y3 = y1 + (sideLength*math.cos(math.radians(30)))
p3 = np.array([x3, y3])

# Getting triangle height
triangleHeight = (sideLength/2) * math.tan(math.radians(60))

# Drawing GUI with TKinter
root= Tk()
can = Canvas(root, width=screenWidth, height=screenHeight)
can.pack()

# Drawing the platform triangle
points = [x1,y1, x2,y2, x3,y3]
can.create_polygon(points, fill='black')

# Drawing the centroid circle 
can.create_oval((screenWidth/2) - centerRadius, y1 + (triangleHeight*2/3) - centerRadius, (screenWidth/2) + centerRadius, y1 + (triangleHeight*2/3) + centerRadius, fill="red", width=2)

# Drawing the platform ring
can.create_oval((screenWidth/2) - (triangleHeight*2/3), y1 + (triangleHeight*2/3) - (triangleHeight*2/3), (screenWidth/2) + (triangleHeight*2/3), y1 + (triangleHeight*2/3) + (triangleHeight*2/3), outline="red", width=2)

# Drawing the first servo ring location
can.create_oval(x1 - servoRingRadius, y1 - servoRingRadius, x1 + servoRingRadius, y1 + servoRingRadius, outline="red", width=2)

# Drawing the second servo ring location
can.create_oval(x2 - servoRingRadius, y2 - servoRingRadius, x2 + servoRingRadius, y2 + servoRingRadius, outline="red", width=2)

# Drawing the third servo ring location
can.create_oval(x3 - servoRingRadius, y3 - servoRingRadius, x3 + servoRingRadius, y3 + servoRingRadius, outline="red", width=2)

# ============== Helper Functions ================
def clickedCoordinates(event):
    #outputting x and y coords to console
    xCoord = event.x
    yCoord = event.y

    if isInsidePlatformTriangle(xCoord, yCoord):
        print("Clicked inside platform triangle.")
    elif isInsidePlatformRing(xCoord, yCoord):
        print("Clicked inside platform ring.")
    else:
        print("X Coordinate: " + str(xCoord) + ", Y Coordinate: " + str(yCoord))


def isInsidePlatformTriangle(x, y):
    p = np.array([x, y])
    

def isInsidePlatformRing(x, y):

    xBound1 = x > ( (screenWidth/2) - (triangleHeight*2/3) )
    xBound2 = x < ( (screenWidth/2) + (triangleHeight*2/3) )

    yBound1 = y > ( y1 + (triangleHeight*2/3) - (triangleHeight*2/3) )
    yBound2 = y < ( y1 + (triangleHeight*2/3) + (triangleHeight*2/3) )

    if xBound1 and xBound2 and yBound1 and yBound2:
        return True
    else:
        return False


#mouseclick event
can.bind("<Button 1>", clickedCoordinates)

# Running the GUI
root.mainloop()

