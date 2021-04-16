'''
    This file contains the classes for the ball and platform.

    Last Updated: 2021-04-16
    Written By: Jeremy Levasseur
'''

# Defining the Ball class
class Ball:
    def __init__(self, mass, radius, xPosition, yPosition, xVelocity, yVelocity, xAcceleration, yAcceleration):
        self.mass = mass
        self.radius = radius
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.xAcceleration = xAcceleration
        self.yAcceleration = yAcceleration


# Defining the Platform class
class Platform:
    def __init__(self, angleOfRotationInX, angleOfRotationInY):
        self.angleOfRotationInX = angleOfRotationInX
        self.angleOfRotationInY = angleOfRotationInY