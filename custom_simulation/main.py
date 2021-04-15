# LIBRARY IMPORTS
from utility_functions import pixelMeasurementToMetresMeasurement, metresMeasurementToPixelMeasurement
from gui import createPlatformGUI, createLegsGUI
from ball_object import Ball
from platform_object import Platform
from pid import PID_Controller
from dynamics_and_kinematics import angleOfTiltToAcceleration, distanceMoved, finalVelocity
from plot_data import plotPidOutputAndBallPositionTimeseries, plotBallPositionTimeseries

import time


# ================ CONSTANTS ================

# GUI Properties
screenWidth = 500  # pixels
screenHeight = 500  # pixels

# Environment
gravity = 9.81  # m/s^s
distanceScale = screenWidth * 2  # 1 metre = 1000 pixels
sampleTime = 0.025

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
outputLowerLimit = -30  # degrees
outputUpperLimit = 30  # degrees
setPointX = screenWidth/2  # pixels
setPointY = screenHeight/2  # pixels


# ================ CREATING MONITORING OBJECTS ================

# Object to keep track of the system results
systemData = {
    'xAccuracy': {
        'consequtiveMeasurmentsNearSetpoint': 0
    },
    'yAccuracy': {
        'consequtiveMeasurmentsNearSetpoint': 0
    }
}

# Setting the measured distance value that is close enough 
# to the set point for it to be considered as satisfactory
nearSetpointCriteria = 1  # pixels

# Setting the number of consequtive setpoint satisfactions
# it will take for the system to end the program and display
# the plots
simulationFinished = 50  # Ball needs to be near the setpoint for 2 seconds straight

timeCyclesCounter = 0
timeSeries = []  # Will be a list of the timestamps throughout the simulation
pidXOutputData = []  # Will be a list of the outputs from the X PID controller throughout the simulation
pidYOutputData = []  # Will be a list of the outputs from the Y PID controller throughout the simulation
positionXData = []  # Will be a list of the X positions of the ball throughout the simulation
positionYData = []  # Will be a list of the Y positions of the ball throughout the simulation


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
tkRoot, canvas = createPlatformGUI(screenWidth, screenHeight)

# Creating the first leg GUI
windowLeg1, leg1Canvas = createLegsGUI(1, screenWidth=screenWidth, screenHeight=screenHeight)


# Creating the second leg GUI
windowLeg2, leg2Canvas = createLegsGUI(2, screenWidth=screenWidth, screenHeight=screenHeight)# windowLeg2, leg2Canvas = createLegsGUI()

# Drawing the ball in it's initial location
ballOval = canvas.create_oval(ball.xPosition - ball.radius, ball.yPosition - ball.radius, ball.xPosition + ball.radius, ball.yPosition + ball.radius, fill='red')

def controller():
    # Defining global variables
    global canvas
    global ballOval
    global timeCyclesCounter

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
    
    # Checking to see if the ball's current position is close enough to the setpoint
    # to be considered satisfactory
    if abs(ball.xPosition - setPointX) <= nearSetpointCriteria:
        systemData['xAccuracy']['consequtiveMeasurmentsNearSetpoint'] += 1
    
    if abs(ball.yPosition - setPointY) <= nearSetpointCriteria:
        systemData['yAccuracy']['consequtiveMeasurmentsNearSetpoint'] += 1
    
    # Checking to see if the ball has been near the setpoint (in both the x and y coordinate)
    # for the simulation to end and for the plots to be shown
    xCondition = systemData['xAccuracy']['consequtiveMeasurmentsNearSetpoint'] == simulationFinished
    yCondition = systemData['yAccuracy']['consequtiveMeasurmentsNearSetpoint'] == simulationFinished

    if xCondition and yCondition:
        # Ball has been at the setpoint for a sufficient amount of time
        tkRoot.destroy()
        # tkRootLegs.destroy()

        # Create plots
        # plotPidOutputAndPositionTimeseries('X', timeSeries, positionXData, pidXOutputData)
        # plotPidOutputAndPositionTimeseries('Y', timeSeries, positionYData, pidYOutputData)
        plotBallPositionTimeseries('X', timeSeries, positionXData)
        plotBallPositionTimeseries('Y', timeSeries, positionYData)

        exit()
    
    else:
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

        # Adding the calculated values to the data lists
        timeSeries.append(timeCyclesCounter)
        pidXOutputData.append(platform.angleOfRotationInX)
        pidYOutputData.append(platform.angleOfRotationInY)
        positionXData.append(pixelMeasurementToMetresMeasurement(distanceScale, ball.xPosition))
        positionYData.append(pixelMeasurementToMetresMeasurement(distanceScale, ball.yPosition))

        timeCyclesCounter += 1  # Incrementing the time cycle counter

        tkRoot.after(int(sampleTime*1000), controller)  # Re-run this function after interval (in milliseconds)


tkRoot.after(3000, controller)  # Begin the loop of getting control feedback

# Running the GUI
tkRoot.mainloop()

