from tkinter import *
import math
import custom_tkinter_functions
import numpy as np

# Constants
screenWidth = 900
screenHeight = 900
sideLength = 600
margin = 120
centerRadius = 7
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
can.create_oval((screenWidth/2) - (triangleHeight*2/3), y1, (screenWidth/2) + (triangleHeight*2/3), y1 + (triangleHeight*2/3) + (triangleHeight*2/3), outline="red", width=2)

# Drawing the first servo ring location
can.create_oval(x1 - servoRingRadius, y1 - servoRingRadius, x1 + servoRingRadius, y1 + servoRingRadius, outline="red", width=2)

# Drawing the second servo ring location
can.create_oval(x2 - servoRingRadius, y2 - servoRingRadius, x2 + servoRingRadius, y2 + servoRingRadius, outline="red", width=2)

# Drawing the third servo ring location
can.create_oval(x3 - servoRingRadius, y3 - servoRingRadius, x3 + servoRingRadius, y3 + servoRingRadius, outline="red", width=2)

# ============== Helper Functions ================
def distanceFromCenterAndServos(p):

    # Getting distance from center
    centerOfRing = np.array([ screenWidth/2, (triangleHeight*2/3) + margin])
    localXFromCenter = abs(p[0] - centerOfRing[0])
    localYFromCenter = abs(p[1] - centerOfRing[1])

    distanceFromCenter = math.sqrt((localXFromCenter**2) + (localYFromCenter**2))

    # Getting distance from servos
    localX1 = abs(p[0] - x1)
    localY1 = abs(p[1] - y1)

    localX2 = abs(p[0] - x2)
    localY2 = abs(p[1] - y2)

    localX3 = abs(p[0] - x3)
    localY3 = abs(p[1] - y3)

    distanceFromServo1 = math.sqrt( (localX1**2) + (localY1**2) )
    distanceFromServo2 = math.sqrt( (localX2**2) + (localY2**2) )
    distanceFromServo3 = math.sqrt( (localX3**2) + (localY3**2) )

    return [distanceFromCenter, distanceFromServo1, distanceFromServo2, distanceFromServo3]


def printMessage(status, distanceFromCenter, distanceFromServo1, distanceFromServo2, distanceFromServo3):

    # Calculating servo weights
    sumOfServoDistances = distanceFromServo1 + distanceFromServo2 + distanceFromServo3

    servo1Percentage = (distanceFromServo1 / sumOfServoDistances) * 100
    servo2Percentage = (distanceFromServo2 / sumOfServoDistances) * 100
    servo3Percentage = (distanceFromServo3 / sumOfServoDistances) * 100

    print("=======================================")
    print("Location: " + status)
    print("Distance From Center: " + str(distanceFromCenter))
    print("Distance From Servo 1: " + str(distanceFromServo1) + ", Percentage: " + str(servo1Percentage))
    print("Distance From Servo 2: " + str(distanceFromServo2) + ", Percentage: " + str(servo2Percentage))
    print("Distance From Servo 3: " + str(distanceFromServo3) + ", Percentage: " + str(servo3Percentage))
    print("=======================================")
    print("\n\n\n")


def clickedCoordinates(event):
    #outputting x and y coords to console
    xCoord = event.x
    yCoord = event.y

    distanceFromCenter, distanceFromServo1, distanceFromServo2, distanceFromServo3 = distanceFromCenterAndServos([xCoord, yCoord])

    if isInsidePlatformTriangle(xCoord, yCoord):
        status = "Inside platform triangle"
        printMessage(status, distanceFromCenter, distanceFromServo1, distanceFromServo2, distanceFromServo3)
    elif isInsidePlatformRing(xCoord, yCoord):
        status = "Inside platform ring"
        printMessage(status, distanceFromCenter, distanceFromServo1, distanceFromServo2, distanceFromServo3)
    else:
        status = "Outside platform ring"
        printMessage(status, distanceFromCenter, distanceFromServo1, distanceFromServo2, distanceFromServo3)


def sign (p1, p2, p3):
    # The edges of the triangle create half-planes
    # The following calculation checks which side the point is on
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


def isInsidePlatformTriangle(x, y):
    p = np.array([x, y])

    d1 = sign(p, p1, p2)
    d2 = sign(p, p2, p3)
    d3 = sign(p, p3, p1)

    hasNeg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    hasPos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not(hasNeg and hasPos)
    

def isInsidePlatformRing(x, y):

    centerOfRing = np.array([ screenWidth/2, (triangleHeight*2/3) + margin])
    localX = abs(centerOfRing[0] - x)
    localY = abs(centerOfRing[1] - y)

    radiusOfClick = math.sqrt((localX**2) + (localY**2))

    if radiusOfClick <= (triangleHeight*2/3):
        return True
    else:
        return False


#mouseclick event
can.bind("<Button 1>", clickedCoordinates)

# Running the GUI
root.mainloop()

