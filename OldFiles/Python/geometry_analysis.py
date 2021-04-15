import numpy as np
import geometry_functions

# ============== Constants =================


# ==========================================

# Creating starting positions that lead to a flat platform
# Geometry of system is based off of CAD starting point

# Lower Link 1 Points
lowerLink1_P_0 = np.array([22.50, 77.9, 0])
lowerLink1_P_1 = np.array([44.957, 77.9, -1.392])

# Lower Link 2 Points
lowerLink2_P_0 = np.array([77.9, 22.5, 0])
lowerLink2_P_1 = np.array([77.9, 44.957, -1.392])

# Upper Link 1 Points
upperLink1_P_0 = lowerLink1_P_1
upperLink1_P_1 = np.array([32.5, 77.9, 126])

# Upper Link 2 Points
upperLink2_P_0 = lowerLink2_P_1
upperLink2_P_1 = np.array([77.9, 32.5, 126])


def tiltToServoAngle(tilt):
    '''
    Using geometry from CAD, there is a linear relationship between the servo angle and the platform angle:
        y = 0.2867x + 1.0021
    where
        y = tilt of platform in X-plane or in Y-plane
        x = servo angle
    
    We must find the servo angle given the desired tilt of the platform in the X-plane or Y-Plane by solving the linear relationship for y:
        x = 3.488y - 3.495
    '''

    return (3.488 * tilt) - 3.495

print(tiltToServoAngle(10))