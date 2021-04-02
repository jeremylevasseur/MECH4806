from tkinter import *
import math
import custom_tkinter_functions

screenWidth = 900
screenHeight = 900

sideLength = 600

margin = 120
centerRadius = 30
outlineRadius = sideLength

x1 = screenWidth / 2
y1 = margin

x2 = x1 - (sideLength*math.sin(math.radians(30)))
y2 = y1 + (sideLength*math.cos(math.radians(30)))

x3 = x1 + (sideLength*math.sin(math.radians(30)))
y3 = y1 + (sideLength*math.cos(math.radians(30)))

triangleHeight = (sideLength/2) * math.tan(math.radians(60))

root= Tk()
can = Canvas(root, width=screenWidth, height=screenHeight)

can.pack()

points = [x1,y1, x2,y2, x3,y3]
can.create_polygon(points, fill='black')
can.create_oval((screenWidth/2) - centerRadius, y1 + (triangleHeight*2/3) - centerRadius, (screenWidth/2) + centerRadius, y1 + (triangleHeight*2/3) + centerRadius, fill="red", width=2)
can.create_oval((screenWidth/2) - (triangleHeight*2/3), y1 + (triangleHeight*2/3) - (triangleHeight*2/3), (screenWidth/2) + (triangleHeight*2/3), y1 + (triangleHeight*2/3) + (triangleHeight*2/3), outline="red", width=2)
root.mainloop()