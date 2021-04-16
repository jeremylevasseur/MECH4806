# ================ LIBRARY IMPORTS ================

# Personally Created Libraries
from utility_functions import pixelMeasurementToMetresMeasurement, metresMeasurementToPixelMeasurement, calculateAllImportantPoints
from gui import createPlatformGUI, createLegsGUI, createButtonGUI
from ball_object import Ball
from platform_object import Platform
from pid import PID_Controller
from dynamics_and_kinematics import angleOfTiltToAcceleration, distanceMoved, finalVelocity
from plot_data import plotPidOutputAndBallPositionTimeseries, plotBallPositionTimeseries

# Third Party Libraries
from tkinter import *
import tinyik as ik

# ================ CONSTANTS ================

# GUI Properties
screenWidth = 500  # pixels
screenHeight = 500  # pixels

# Environment
gravity = 9.81  # m/s^s
distanceScale = screenWidth * 2  # 1 metre = 1000 pixels
sampleTime = 0.025  # Rate at which the position measurements occur
appliedAcceleration = 40000.0  # pixels/s^2 - The acceleration value that is applied to the ball when a button is clicked

# Ball Properties
ballMass = 0.45  # kg
ballRadius = 0.02  # metres

# Platform Preconditions
startingPlatformAngleOfRotationInX = 0  # degrees
startingPlatformAngleOfRotationInY = 0  # degrees

# Ball Preconditions
startingXPosition = screenWidth * 3/4  # pixels
startingYPosition = screenHeight * 3/4  # pixels
startingXVelocity = 0  # pixels/s
startingYVelocity = 0  # pixels/s
startingXAcceleration = 0  # pixels/s^2
startingYAcceleration = 0  # pixels/s^2

# PID Properties
kp = 1  # Proportional gain
ki = 0.8  # Integral gain
kd = 0.5  # Derivative gain
outputLowerLimit = -30  # degrees - Sets the minimum angle of platform rotation
outputUpperLimit = 30  # degrees - Sets the maximum angle of platform rotation
setPointX = screenWidth/2  # pixels - Where you want the ball to end up in the X coordinate system
setPointY = screenHeight/2  # pixels - Where you want the ball to end up in the Y coordinate system

# Leg Constants
distanceScaleLegs = screenWidth * 4  # 1 metre = 2000 pixels
margin = 100  # Offsets drawings so that they aren't next to the GUI border
L1 = metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.0225)  # 22.5 mm - Length of the lower link
L2 = metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.120)  # 120 mm - Length of the upper link
platformWidth = metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.160)  # 160 mm
halfPlatformWidth = platformWidth / 2
rotationPointRadius = 5  # For drawings
origin_x = margin
origin_y = (screenHeight - margin)
x3 = origin_x + metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.090)  # 90 mm
y3 = origin_y - metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.120)  # 120 mm
x3_cartesian = 90.0  # 90 mm
# x3_cartesian = metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.090)  # 90 mm
y3_cartesian = 120.0  # 120 mm
# y3_cartesian = metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.120)  # 120 mm

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
nearSetpointCriteria = 5  # pixels

# Setting the number of consequtive setpoint satisfactions
# it will take for the system to end the program and display
# the plots
simulationFinished = 200  # Ball needs to be near the setpoint for 2 seconds straight

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

# Initializing the actuators for inverse kinematics
# legXActuator = ik.Actuator(['z', [metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.0225), 0.0, 0.0], 'z', [metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.120), 0.0, 0.0]])
legXActuator = ik.Actuator(['z', [22.5, 0.0, 0.0], 'z', [120.0, 0.0, 0.0]])
# legYActuator = ik.Actuator(['z', [metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.0225), 0.0, 0.0], 'z', [metresMeasurementToPixelMeasurement(distanceScaleLegs, 0.120), 0.0, 0.0]])
legYActuator = ik.Actuator(['z', [22.5, 0.0, 0.0], 'z', [120.0, 0.0, 0.0]])

# Creating the platform GUI
tkRoot, canvas = createPlatformGUI(screenWidth, screenHeight)

# Creating the first leg GUI
legXWindow, legXCanvas = createLegsGUI(1, screenWidth=screenWidth, screenHeight=screenHeight)

# Creating the second leg GUI
legYWindow, legYCanvas = createLegsGUI(2, screenWidth=screenWidth, screenHeight=screenHeight)

# Creating the button GUI
buttonsWindow, buttonsCanvas = createButtonGUI(screenWidth=screenWidth, screenHeight=screenHeight)

# ================ DRAWING INITIAL CANVAS OBJECTS ================

# Drawing the ball in it's initial location
ballOval = canvas.create_oval(ball.xPosition - ball.radius, ball.yPosition - ball.radius, ball.xPosition + ball.radius, ball.yPosition + ball.radius, fill='red')

# Calculating important points for the legs GUI
x1, y1, x2, y2, x4, y4 = calculateAllImportantPoints(legXActuator, L1, halfPlatformWidth, platform.angleOfRotationInX, origin_x, origin_y, x3, y3, x3_cartesian, y3_cartesian)

# X CANVAS
# Drawing platform rotation point on leg X canvas
platformRotationPointLegX = legXCanvas.create_oval(x3 - rotationPointRadius, y3 - rotationPointRadius, x3 + rotationPointRadius, y3 + rotationPointRadius, fill='black')
# Drawing platform line 1 on leg X canvas
platformLine1LegX = legXCanvas.create_line(x2, y2, x3, y3, width=5)
# Drawing platform line 2 on leg X canvas
platformLine2LegX = legXCanvas.create_line(x3, y3, x4, y4, width=5)
# Drawing servo rotation point on leg X canvas
servoRotationPointLegX = legXCanvas.create_oval(origin_x - rotationPointRadius, origin_y - rotationPointRadius, origin_x + rotationPointRadius, origin_y + rotationPointRadius, fill='black')
# Drawing lower link line on leg X canvas
lowerLinkLineLegX = legXCanvas.create_line(origin_x, origin_y, x1, y1, width=5)
# Drawing upper link line on leg X canvas
upperLinkLineLegX = legXCanvas.create_line(x1, y1, x2, y2, width=5)

# Y CANVAS
# Drawing platform rotation point on leg Y canvas
platformRotationPointLegY = legYCanvas.create_oval(x3 - rotationPointRadius, y3 - rotationPointRadius, x3 + rotationPointRadius, y3 + rotationPointRadius, fill='black')
# Drawing platform line 1 on leg Y canvas
platformLine1LegY = legYCanvas.create_line(x2, y2, x3, y3, width=5)
# Drawing platform line 2 on leg Y canvas
platformLine2LegY = legYCanvas.create_line(x3, y3, x4, y4, width=5)
# Drawing servo rotation point on leg Y canvas
servoRotationPointLegY = legYCanvas.create_oval(origin_x - rotationPointRadius, origin_y - rotationPointRadius, origin_x + rotationPointRadius, origin_y + rotationPointRadius, fill='black')
# Drawing lower link line on leg Y canvas
lowerLinkLineLegY = legYCanvas.create_line(origin_x, origin_y, x1, y1, width=5)
# Drawing upper link line on leg Y canvas
upperLinkLineLegY = legYCanvas.create_line(x1, y1, x2, y2, width=5)

def applyForceInPositiveX():
    print("Applying Force In +X")
    ball.xAcceleration = appliedAcceleration

def applyForceInNegativeX():
    print("Applying Force In -X")
    ball.xAcceleration = (-1) * appliedAcceleration

def applyForceInPositiveY():
    print("Applying Force In -Y")
    ball.yAcceleration = appliedAcceleration

def applyForceInNegativeY():
    print("Applying Force In +Y")
    ball.yAcceleration = (-1) * appliedAcceleration


# Creating buttons on the button window
# Note that, from the viewer's perspective, the Y directions are flipped and because of
# this, the button labels and print messages in the Y direction are also flipped
forceInPositiveXButton = Button(buttonsWindow, text="Apply Force In +X", command=applyForceInPositiveX).grid()
forceInNegativeXButton = Button(buttonsWindow, text="Apply Force In -X", command=applyForceInNegativeX).grid()
forceInNegativeYButton = Button(buttonsWindow, text="Apply Force In +Y", command=applyForceInNegativeY).grid()
forceInPositiveYButton = Button(buttonsWindow, text="Apply Force In -Y", command=applyForceInPositiveY).grid()


def updateLegX(alpha):
    # Defining global variables
    global legXWindow, legXCanvas
    global platformLine1LegX, platformLine2LegX, lowerLinkLineLegX, upperLinkLineLegX

    x1, y1, x2, y2, x4, y4 = calculateAllImportantPoints(legXActuator, L1, halfPlatformWidth, platform.angleOfRotationInX, origin_x, origin_y, x3, y3, x3_cartesian, y3_cartesian)

    # ================ RE-DRAWING SYSTEM ================

    # Removing previous lines on leg X canvas
    legXCanvas.delete(platformLine1LegX)
    legXCanvas.delete(platformLine2LegX)
    legXCanvas.delete(lowerLinkLineLegX)
    legXCanvas.delete(upperLinkLineLegX)

    # Drawing platform line 1 on leg X canvas
    platformLine1LegX = legXCanvas.create_line(x2, y2, x3, y3, width=5)
    # Drawing platform line 2 on leg X canvas
    platformLine2LegX = legXCanvas.create_line(x3, y3, x4, y4, width=5)
    # Drawing lower link line on leg X canvas
    lowerLinkLineLegX = legXCanvas.create_line(origin_x, origin_y, x1, y1, width=5)
    # Drawing upper link line on leg X canvas
    upperLinkLineLegX = legXCanvas.create_line(x1, y1, x2, y2, width=5)


def updateLegY(alpha):
    # Defining global variables
    global legYWindow, legYCanvas
    global platformLine1LegY, platformLine2LegY, lowerLinkLineLegY, upperLinkLineLegY

    x1, y1, x2, y2, x4, y4 = calculateAllImportantPoints(legYActuator, L1, halfPlatformWidth, platform.angleOfRotationInY, origin_x, origin_y, x3, y3, x3_cartesian, y3_cartesian)

    # ================ RE-DRAWING SYSTEM ================

    # Removing previous lines on leg Y canvas
    legYCanvas.delete(platformLine1LegY)
    legYCanvas.delete(platformLine2LegY)
    legYCanvas.delete(lowerLinkLineLegY)
    legYCanvas.delete(upperLinkLineLegY)

    # Drawing platform line 1 on leg Y canvas
    platformLine1LegY = legYCanvas.create_line(x2, y2, x3, y3, width=5)
    # Drawing platform line 2 on leg Y canvas
    platformLine2LegY = legYCanvas.create_line(x3, y3, x4, y4, width=5)
    # Drawing lower link line on leg Y canvas
    lowerLinkLineLegY = legYCanvas.create_line(origin_x, origin_y, x1, y1, width=5)
    # Drawing upper link line on leg Y canvas
    upperLinkLineLegY = legYCanvas.create_line(x1, y1, x2, y2, width=5)


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
    else:
        systemData['xAccuracy']['consequtiveMeasurmentsNearSetpoint'] = 0
    
    if abs(ball.yPosition - setPointY) <= nearSetpointCriteria:
        systemData['yAccuracy']['consequtiveMeasurmentsNearSetpoint'] += 1
    else:
        systemData['yAccuracy']['consequtiveMeasurmentsNearSetpoint'] = 0
    
    # Checking to see if the ball has been near the setpoint (in both the x and y coordinate)
    # for the simulation to end and for the plots to be shown
    xCondition = systemData['xAccuracy']['consequtiveMeasurmentsNearSetpoint'] > simulationFinished
    yCondition = systemData['yAccuracy']['consequtiveMeasurmentsNearSetpoint'] > simulationFinished

    if xCondition and yCondition:
        # Ball has been at the setpoint for a sufficient amount of time
        tkRoot.destroy()
        # tkRootLegs.destroy()

        # Create plots
        plotPidOutputAndBallPositionTimeseries('X', timeSeries, positionXData, pidXOutputData)
        plotPidOutputAndBallPositionTimeseries('Y', timeSeries, positionYData, pidYOutputData)
        # plotBallPositionTimeseries('X', timeSeries, positionXData)
        # plotBallPositionTimeseries('Y', timeSeries, positionYData)

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
        updateLegX(platform.angleOfRotationInX)
        updateLegY(platform.angleOfRotationInY)

        # Updating the ball acceleration states
        ball.xAcceleration = metresMeasurementToPixelMeasurement(distanceScale, angleOfTiltToAcceleration(gravity, platform.angleOfRotationInX))
        ball.yAcceleration = metresMeasurementToPixelMeasurement(distanceScale, angleOfTiltToAcceleration(gravity, platform.angleOfRotationInY))

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

