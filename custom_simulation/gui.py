from tkinter import *
import math

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

def createLegsGUI(tkRoot, screenWidth=500, screenHeight=500):
    # Creating the legs window
    legsWindow = Toplevel()
    legsWindow.title("Legs Simulation")

    # Creating root canvas
    legsCanvas = Canvas(legsWindow, width=screenWidth, height=screenHeight)
    legsCanvas.pack()

    legRect = legsCanvas.create_rectangle((screenWidth/2) - 100, (screenHeight/2) - 100, (screenWidth/2) + 100, (screenHeight/2) + 100, fill="black", width=2)

    # Returning the new window
    return tkRoot, legsCanvas


def redrawBall(canvas, ballOval, ballObject):
    # Removing old ball oval
    canvas.delete(ballOval)

    # Drawing new ball oval
    ballOval = canvas.create_oval(ballObject.xPosition - ballObject.radius, ballObject.yPosition - ballObject.radius, ballObject.xPosition + ballObject.radius, ballObject.yPosition + ballObject.radius)

    return canvas, ballOval