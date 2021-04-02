import numpy as np
import math


def calculateRightTriangleHeight(base, hypotenuse):
    return math.sqrt((hypotenuse**2) - (base**2))


def calculateCentroidOfTriangle(p1, p2, p3):
    centroid_x = (p1[0] + p2[0] + p3[0]) / 3
    centroid_y = (p1[1] + p2[1] + p3[1]) / 3
    centroid_z = (p1[2] + p2[2] + p3[2]) / 3
    return np.array([centroid_x, centroid_y, centroid_z])


def calculateLengthOf3DVector(vec):
    return math.sqrt((vec[0]**2) + (vec[1]**2) + (vec[2]**2))


def calculateAngleWithZAxis(normalVector):
    return math.degrees(math.acos(normalVector[2] / calculateLengthOf3DVector(normalVector)))


def servoAngleToLegHeight(servoAngle, servoArmHeight, baseLegHeight):
    servoAngleInRadians = math.radians(servoAngle)
    phi = math.asin((servoArmHeight/baseLegHeight) * math.sin(math.radians(90) - servoAngleInRadians))
    alpha = math.radians(90) - phi + servoAngleInRadians
    return (baseLegHeight * math.sin(alpha)) / math.sin(math.radians(90) - servoAngleInRadians)


def checkAngleOfTwist(desiredAngleOfTwist, normalVector):
    calculatedAngleOfTwist = math.acos(normalVector[2] / calculateLengthOf3DVector(normalVector))
    if abs(calculatedAngleOfTwist - desiredAngleOfTwist) < 0.1:
        return True
    else:
        return False

def findZValuesForGivenAngleOfTwist(desiredAngleOfTwist, servoArmHeight, baseLegHeight, triangleSideLength=120):
    
    z1 = 50
    z2 = 50
    z3 = 50

    legHeightLowerBound = 10 * math.sqrt(21)
    legHeightHigherBound = 70

    # Setting points
    p1 = np.array([0, 0, z1])
    p2 = np.array([triangleSideLength, 0, z2])
    p3 = np.array([triangleSideLength/2, calculateRightTriangleHeight(triangleSideLength/2, triangleSideLength), z3])
    

