'''
    This file contains functions that create GUI windows.

    Last Updated: 2021-04-16
    Written By: Jeremy Levasseur
'''

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

def createLegsGUI(legLetter, screenWidth=500, screenHeight=500, theta=30, alpha=7.854):
    # Creating the legs window
    legsWindow = Toplevel()
    legsWindow.title("Leg " + str(legLetter) + " Simulation")

    # Creating the leg canvas
    legCanvas = Canvas(legsWindow, width=screenWidth, height=screenHeight)
    legCanvas.pack()

    # Returning the new window
    return legsWindow, legCanvas


def createButtonGUI(screenWidth=500, screenHeight=500):
    # Creating the buttons window
    buttonsWindow = Toplevel()
    buttonsWindow.title("Move The Ball")

    # Creating the button canvas
    buttonCanvas = Canvas(buttonsWindow, width=screenWidth, height=screenHeight)

    # Returning the new window
    return buttonsWindow, buttonCanvas