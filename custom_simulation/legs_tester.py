from tkinter import *
import math

'''
    DISREGARD THIS FILE, I'M USING IT FOR TESTING
'''

# Constants
centerCircleRadius = 10
screenWidth = 500  # pixels
screenHeight = 500  # pixels
distanceScale = screenWidth * 2  # 1 metre = 1000 pixels

# Creating the root window
tkRoot = Tk()
tkRoot.title("Legs Simulation")

# Creating root canvas
rootCanvas = Canvas(tkRoot, width=screenWidth, height=screenHeight)
rootCanvas.pack()

platformBorderRectangle = rootCanvas.create_rectangle(10, 10, screenWidth, screenHeight, fill='', outline='black', width='10')


# Running the GUI
tkRoot.mainloop()