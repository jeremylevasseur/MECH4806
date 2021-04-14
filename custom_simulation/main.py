# LIBRARY IMPORTS
from utility_functions import pixelMeasurementToMetresMeasurement, metresMeasurementToPixelMeasurement
from gui import createGUI, redrawBall
from ball_object import Ball
from platform_object import Platform
from pid import PID_Controller
from dynamics_and_kinematics import angleOfTiltToAcceleration, distanceMoved, finalVelocity

import time
import numpy as np
import matplotlib.pyplot as plt

# ================ CONSTANTS ================

# GUI Properties
screenWidth = 500  # pixels
screenHeight = 500  # pixels

# Environment
gravity = 9.81  # m/s^s
distanceScale = screenWidth * 2  # 1 metre = 1000 pixels
sampleTime = 0.1

# Ball Properties
ballMass = 0.45  # kg
ballRadius = 0.02  # metres

# Platform Preconditions
startingPlatformAngleOfRotationInX = 0  # 0 degrees
startingPlatformAngleOfRotationInY = 0  # 0 degrees

# Ball Preconditions
startingXPosition = screenWidth / 4  # pixels
startingYPosition = screenHeight / 4  # pixels
startingXVelocity = 0  # pixels/s
startingYVelocity = 0  # pixels/s
startingXAcceleration = 0  # pixels/s^2
startingYAcceleration = 0  # pixels/s^2

# PID Properties
kp = 10
ki = 0.005
kd = 7
outputLowerLimit = -30 # Degrees
outputUpperLimit = 30 # Degrees
setPointX = screenWidth/2
setPointY = screenHeight/2


# ================ CREATING MONITORING OBJECTS ================

# Object to keep track of the system results
systemData = {
    xAccuracy: {
        consequtiveMeasurmentsNearSetpoint: 0
    },
    yAccuracy: {
        consequtiveMeasurmentsNearSetpoint: 0
    }
}

# Setting the measured distance value that is close enough 
# to the set point for it to be considered as satisfactory
nearSetpointCriteria = 5  # Pixels

# Setting the number of consequtive setpoint satisfactions
# it will take for the system to end the program and display
# the plots
simulationFinished = 20  # Ball needs to be near the setpoint for 2 seconds straight


# ================ CREATING SIMULATION ================

# Initializing Platform
platform = Platform(
    startingPlatformAngleOfRotationInX,
    startingPlatformAngleOfRotationInY)

# Initializing ball
ball = Ball(
    ballMass,
    metresMeasurementToPixelMeasurement(distanceScale, ballRadius),
    startingXPosition,
    startingYPosition,
    startingXVelocity,
    startingYVelocity,
    startingXAcceleration,
    startingYAcceleration)

# Initializing PID controllers
pidX = PID_Controller(
    kp,
    ki,
    kd,
    sampleTime,
    outputLowerLimit,
    outputUpperLimit,
    setPointX)

pidY = PID_Controller(
    kp,
    ki,
    kd,
    sampleTime,
    outputLowerLimit,
    outputUpperLimit,
    setPointY)

# Creating the platform GUI
tkRoot, canvas = createGUI(screenWidth, screenHeight)

# Creating the legs GUI
tkRootLegs, canvasLegs = createGUI(screenWidth, screenHeight)

# Drawing the ball in it's initial location
ballOval = canvas.create_oval(ball.xPosition - ball.radius, ball.yPosition - ball.radius, ball.xPosition + ball.radius, ball.yPosition + ball.radius, fill='red')

def controller():
    # Defining global variables
    global systemData
    global canvas
    global ballOval

    # Calculate ball's new position
    ball.xPosition = metresMeasurementToPixelMeasurement(
        distanceScale,
        distanceMoved(
            pixelMeasurementToMetresMeasurement(distanceScale, ball.xPosition),
            pixelMeasurementToMetresMeasurement(distanceScale, ball.xVelocity),
            pixelMeasurementToMetresMeasurement(distanceScale, ball.xAcceleration),
            sampleTime))
    
    ball.yPosition = metresMeasurementToPixelMeasurement(
        distanceScale,
        distanceMoved(
            pixelMeasurementToMetresMeasurement(distanceScale, ball.yPosition),
            pixelMeasurementToMetresMeasurement(distanceScale, ball.yVelocity),
            pixelMeasurementToMetresMeasurement(distanceScale, ball.yAcceleration),
            sampleTime))
    
    # Checking to see if 

    # Calculate ball's new velocity
    ball.xVelocity = metresMeasurementToPixelMeasurement(
        distanceScale,
        finalVelocity(
            pixelMeasurementToMetresMeasurement(distanceScale, ball.xVelocity),
            pixelMeasurementToMetresMeasurement(distanceScale, ball.xAcceleration),
            sampleTime))
    
    ball.yVelocity = metresMeasurementToPixelMeasurement(
        distanceScale,
        finalVelocity(
            pixelMeasurementToMetresMeasurement(distanceScale, ball.yVelocity),
            pixelMeasurementToMetresMeasurement(distanceScale, ball.yAcceleration),
            sampleTime))

    # Updating GUI with new ball location
    # by removing old ball oval and then drawing it's new location
    canvas.delete(ballOval)
    ballOval = canvas.create_oval(ball.xPosition - ball.radius, ball.yPosition - ball.radius, ball.xPosition + ball.radius, ball.yPosition + ball.radius, fill='red')

    # Updating the platform state by assigning it's angle
    # of tilts to the outputs of the PID controllers
    platform.angleOfRotationInX = pidX.getOutput(ball.xPosition)
    platform.angleOfRotationInY = pidY.getOutput(ball.yPosition)

    # Updating the ball acceleration states
    ball.xAcceleration = angleOfTiltToAcceleration(gravity, platform.angleOfRotationInX)
    ball.yAcceleration = angleOfTiltToAcceleration(gravity, platform.angleOfRotationInY)

    tkRoot.after(int(sampleTime*1000), controller)  # Re-run this function after interval (in milliseconds)


tkRoot.after(0, controller)  # Begin the loop of getting control feedback

# Running the GUI
tkRoot.mainloop()

