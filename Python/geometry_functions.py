import numpy as np
import math


def calculateRightTriangleHeight(base, hypotenuse):
    return math.sqrt((hypotenuse**2) - (base**2))


def calculateCentroidOfTriangle(p1, p2, p3):
    centroid_x = (p1[0] + p2[0] + p3[0]) / 3
    centroid_y = (p1[1] + p2[1] + p3[1]) / 3
    centroid_z = (p1[2] + p2[2] + p3[2]) / 3
    return np.array([centroid_x, centroid_y, centroid_z])


def calculateLengthOf3DVector(x, y, z):
    return math.sqrt((x**2) + (y**2) + (z**2))


def calculateAngleWithZAxis(normalVector):
    return math.degrees(math.acos(normalVector[2] / calculateLengthOf3DVector(normalVector[0], normalVector[1], normalVector[2])))