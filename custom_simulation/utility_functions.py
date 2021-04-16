import numpy as np
import math

'''
    These conversion functions assume the distance scale is in pixels per metre
'''

# Position
def pixelMeasurementToMetresMeasurement(distanceScale, positionInPixels):
    return positionInPixels * (1/distanceScale)  # metres, metres/s, or metres/s^2

def metresMeasurementToPixelMeasurement(distanceScale, positionInMetres):
    return positionInMetres * distanceScale  # pixels, pixels/s, or pixels/s^2


# Print iterations progress
def printProgressBar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def calculateAllImportantPoints(inverseKinematicsActuator, L1, halfPlatformWidth, alpha, origin_x, origin_y, x3, y3, x3_cartesian, y3_cartesian):
    # (x4, y4)
    x4_pixels = x3 + (halfPlatformWidth * math.cos(math.radians(alpha)))
    y4_pixels = y3 + (halfPlatformWidth * math.sin(math.radians(alpha)))

    # (x2, y2)
    # x2_cartesian = x3_cartesian - (halfPlatformWidth * math.cos(math.radians(alpha)))
    x2_cartesian = x3_cartesian - (80.0 * math.cos(math.radians(alpha)))
    # y2_cartesian = y3_cartesian + (halfPlatformWidth * math.sin(math.radians(alpha)))
    y2_cartesian = y3_cartesian + (80.0 * math.sin(math.radians(alpha)))
    
    x2_pixels = x3 - (halfPlatformWidth * math.cos(math.radians(alpha)))
    y2_pixels = y3 - (halfPlatformWidth * math.sin(math.radians(alpha)))

    # Setting actuator end effector to where it should be => (x2, y2)
    inverseKinematicsActuator.ee = [x2_cartesian, y2_cartesian, 0.0]

    # Calculating link angles with inverse kinematics
    [theta1, theta2] = inverseKinematicsActuator.angles

    # (x1, y1)
    x1_pixels = origin_x - (L1 * math.cos(theta1))
    y1_pixels = origin_y - (L1 * math.sin(theta1))

    lengthOfLowerLink = math.sqrt((abs(x1_pixels-origin_x)**2) + (abs(y1_pixels-origin_y)**2))
    lengthOfUpperLink = math.sqrt((abs(x2_pixels-x1_pixels)**2) + (abs(y2_pixels-y1_pixels)**2))

    print(alpha, math.degrees(theta1), math.degrees(theta2), lengthOfLowerLink, lengthOfUpperLink)

    return x1_pixels, y1_pixels, x2_pixels, y2_pixels, x4_pixels, y4_pixels