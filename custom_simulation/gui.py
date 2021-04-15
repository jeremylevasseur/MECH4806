from tkinter import *
import math
from utility_functions import pixelMeasurementToMetresMeasurement, metresMeasurementToPixelMeasurement

def createPlatformGUI(screenWidth=500, screenHeight=500):
    # Constants
    centerCircleRadius = 10

    # Creating the root window
    tkRoot = Tk()
    tkRoot.title("Platform Simulation")

    # Creating root canvas
    rootCanvas = Canvas(tkRoot, width=screenWidth, height=screenHeight)
    rootCanvas.pack()

    # Drawing centre circle
    platformCentreOval = rootCanvas.create_oval((screenWidth/2) - centerCircleRadius, (screenHeight/2) - centerCircleRadius, (screenWidth/2) + centerCircleRadius, (screenHeight/2) + centerCircleRadius, fill="black", width=2)

    # Drawing platform border
    platformBorderRectangle = rootCanvas.create_rectangle(0, 0, screenWidth, screenHeight, fill='', outline='black', width='10')

    # Returning tkinter object and the canvas object
    return tkRoot, rootCanvas

def createLegsGUI(legNumber, screenWidth=500, screenHeight=500, theta=30, alpha=7.854):
    # Constants
    distanceScaleLegs = screenWidth * 4  # 1 metre = 2000 pixels
    margin = 100
    L1 = 0.0225  # 22.5 mm
    L2 = 0.120  # 120 mm
    platformWidth = 0.160  # 160 mm
    halfPlatformWidth = platformWidth / 2
    rotationPointRadius = 5

    # Creating the legs window
    legsWindow = Toplevel()
    legsWindow.title("Leg " + str(legNumber) + " Simulation")

    # Creating root canvas
    legsCanvas = Canvas(legsWindow, width=screenWidth, height=screenHeight)
    legsCanvas.pack()

    # ================ IMPORTANT POINTS ================

    # Origin
    origin_x = margin
    origin_y = (screenHeight - margin)

    # (x1, y1)
    x1 = origin_x + (metresMeasurementToPixelMeasurement(distanceScaleLegs, L1) * math.cos(math.radians(theta)))
    y1 = origin_y - (metresMeasurementToPixelMeasurement(distanceScaleLegs, L1) * math.sin(math.radians(theta)))

    # (x3, y3)
    x3 = origin_x + (metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.090) * math.cos(math.radians(theta)))
    y3 = origin_y - (metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.120) * math.sin(math.radians(theta)))

    # (x2, y2)
    x2 = x3 - ((metresMeasurementToPixelMeasurement(distanceScaleLegs, halfPlatformWidth)) * math.cos(math.radians(alpha)))
    y2 = y3 - ((metresMeasurementToPixelMeasurement(distanceScaleLegs, halfPlatformWidth)) * math.sin(math.radians(alpha)))

    # (x4, y4)
    x4 = x3 + ((metresMeasurementToPixelMeasurement(distanceScaleLegs, halfPlatformWidth)) * math.cos(math.radians(alpha)))
    y4 = y3 + ((metresMeasurementToPixelMeasurement(distanceScaleLegs, halfPlatformWidth)) * math.sin(math.radians(alpha)))

    # ================ DRAWING SYSTEM ================

    # Servo Rotation Point
    servoRotationPoint = legsCanvas.create_oval(origin_x - rotationPointRadius, origin_y - rotationPointRadius, origin_x + rotationPointRadius, origin_y + rotationPointRadius, fill='black')

    # Lower Link
    lowerLinkLine = legsCanvas.create_line(origin_x, origin_y, x1, y1, width=5)

    # Upper Link
    upperLinkLine = legsCanvas.create_line(x1, y1, x2, y2, width=5)

    # Platform Rotation Point
    platformRotationPoint = legsCanvas.create_oval(x3 - rotationPointRadius, y3 - rotationPointRadius, x3 + rotationPointRadius, y3 + rotationPointRadius, fill='black')

    # Platform Line 1
    platformLine1 = legsCanvas.create_line(x2, y2, x3, y3, width=5)

    # Platform Line 2
    platformLine2 = legsCanvas.create_line(x3, y3, x4, y4, width=5)

    # Returning the new window
    return legsWindow, legsCanvas
