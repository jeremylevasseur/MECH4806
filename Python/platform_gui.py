from tkinter import *
import math
import custom_tkinter_functions

screenWidth = 900
screenHeight = 900
# screenHeight = (screenWidth/2) * math.tan(math.radians(60))

margin = 120
centerRadius = 30


x1 = screenWidth / 2
y1 = margin

x2 = margin
y2 = (screenWidth/2) * math.tan(math.radians(60)) - margin

x3 = screenWidth - margin
y3 = (screenWidth/2) * math.tan(math.radians(60)) - margin

root= Tk()
can = Canvas(root, width=screenWidth, height=screenHeight)

can.pack()

points = [x1,y1, x2,y2, x3,y3]
can.create_polygon(points, fill='black')
can.create_oval((screenWidth/2) - centerRadius, (screenHeight/2) - centerRadius, (screenWidth/2) + centerRadius, (screenHeight/2) + centerRadius, outline="#f11", fill="red", width=2)
can.create_oval((screenWidth/2) - centerRadius, (screenHeight/2) - centerRadius, (screenWidth/2) + centerRadius, (screenHeight/2) + centerRadius, outline="#f11", fill="red", width=2)
root.mainloop()