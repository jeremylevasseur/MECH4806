from tkinter import *
import math

def createGUI(screenWidth=500, screenHeight=500):
    # Constants
    centerCircleRadius = 10

    # Creating tkinter canvas
    root= Tk()
    canvas = Canvas(root, width=screenWidth, height=screenHeight)
    canvas.pack()

    # Drawing center circle
    canvas.create_oval((screenWidth/2) - centerCircleRadius, (screenHeight/2) - centerCircleRadius, (screenWidth/2) + centerCircleRadius, (screenHeight/2) + centerCircleRadius, fill="black", width=2)

    # Drawing platform border
    canvas.create_rectangle(0, 0, screenWidth, screenHeight, fill='', outline='black', width='10')

    # Returning tkinter object
    return root
