# LIBRARY IMPORTS
from utility_functions import pixelMeasurementToMetresMeasurement, metresMeasurementToPixelMeasurement
from gui import createGUI
from ball import Ball
from platform import Platform
from pid import PID_Controller
# import dynamics_and_kinematics
from dynamics_and_kinematics import distanceMoved_1

import time
import numpy as np
import matplotlib.pyplot as plt

# ================ CONSTANTS ================

# GUI Properties
screenWidth = 500  # pixels
screenHeight = 500  # pixels

# Environment
g = 9.81  # m/s^s
distanceScale = screenWidth * 2/5  # 1 metre = 200 pixels
sampleTime = 0.1

# Ball Properties
ballMass = 0.45  # kg
ballRadius = 0.04  # metres

# Platform Preconditions
startingPlatformAngleOfRotationInX = 0  # 0 degrees
startingPlatformAngleOfRotationInY = 0  # 0 degrees

# Ball Preconditions
startingXPosition = screenWidth / 4  # pixels
startingYPosition = screenHeight / 4  # pixels
startingXVelocity = 0  # m/s
startingYVelocity = 0  # m/s
startingXAcceleration = 0  # m/s^2
startingYAcceleration = 0  # m/s^2

# ================ CREATING SIMULATION ================

# Initializing Platform
platform = Platform(
    startingPlatformAngleOfRotationInX, 
    startingPlatformAngleOfRotationInY)

# Initializing ball
ball = Ball(
    ballMass, 
    ballRadius, 
    startingXPosition, 
    startingYPosition, 
    startingXVelocity, 
    startingYVelocity, 
    startingXAcceleration, 
    startingYAcceleration)

# Creating the GUI
tkRoot = createGUI(screenWidth, screenHeight)


# Running the GUI
tkRoot.mainloop()

