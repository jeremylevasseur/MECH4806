from tkinter import *
import math

def createGUI(screenWidth=500, screenHeight=500):
    # Constants
    centerCircleRadius = 10

    # Creating tkinter canvas
    tkRoot = Tk()
    canvas = Canvas(tkRoot, width=screenWidth, height=screenHeight)
    canvas.pack()

    # Drawing centre circle
    platformCentreOval = canvas.create_oval((screenWidth/2) - centerCircleRadius, (screenHeight/2) - centerCircleRadius, (screenWidth/2) + centerCircleRadius, (screenHeight/2) + centerCircleRadius, fill="black", width=2)

    # Drawing platform border
    platformBorderRectangle = canvas.create_rectangle(0, 0, screenWidth, screenHeight, fill='', outline='black', width='10')

    # Returning tkinter object and the canvas object
    return tkRoot, canvas

def redrawBall(canvas, ballOval, ballObject):
    # Removing old ball oval
    canvas.delete(ballOval)

    # Drawing new ball oval
    ballOval = canvas.create_oval(ballObject.xPosition - ballObject.radius, ballObject.yPosition - ballObject.radius, ballObject.xPosition + ballObject.radius, ballObject.yPosition + ballObject.radius)

    return canvas, ballOval