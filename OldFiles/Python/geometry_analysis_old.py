import numpy as np
import geometry_functions

# Constants
triangleSideLength = 120
legOneHeight = 40
legTwoHeight = 60
legThreeHeight = 50

# Setting points
p1 = np.array([0, 0, legOneHeight])
p2 = np.array([triangleSideLength, 0, legTwoHeight])
p3 = np.array([triangleSideLength/2, geometry_functions.calculateRightTriangleHeight(triangleSideLength/2, triangleSideLength), legThreeHeight])

# Setting desired angle of tilt
desiredAngleOfTilt = 10  # Degrees

planeNormalVector = np.cross( (p2 - p1) , (p3 - p1) )

triangleCentroidVector = geometry_functions.calculateCentroidOfTriangle(p1, p2, p3)
lengthOfCentroidVector = geometry_functions.calculateLengthOf3DVector(triangleCentroidVector)

angleOfTilt = geometry_functions.calculateAngleWithZAxis(planeNormalVector)

# print(geometry_functions.servoAngleToLegHeight(10.0, 20.0, 50.0))


