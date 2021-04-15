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


def calculateAllImportantPoints(origin_x, origin_y, distanceScale, halfPlatformWidth, alpha, theta, L1):
    # (x1, y1)
    x1 = origin_x + (metresMeasurementToPixelMeasurement(distanceScale, L1) * math.cos(math.radians(theta)))
    y1 = origin_y - (metresMeasurementToPixelMeasurement(distanceScale, L1) * math.sin(math.radians(theta)))

    # (x3, y3)
    x3 = origin_x + (metresMeasurementToPixelMeasurement(distanceScale, 0.090) * math.cos(math.radians(theta)))
    y3 = origin_y - (metresMeasurementToPixelMeasurement(distanceScale, 0.120) * math.sin(math.radians(theta)))

    # (x2, y2)
    x2 = x3 - ((metresMeasurementToPixelMeasurement(distanceScale, halfPlatformWidth)) * math.cos(
        math.radians(alpha)))
    y2 = y3 - ((metresMeasurementToPixelMeasurement(distanceScale, halfPlatformWidth)) * math.sin(
        math.radians(alpha)))

    # (x4, y4)
    x4 = x3 + ((metresMeasurementToPixelMeasurement(distanceScale, halfPlatformWidth)) * math.cos(
        math.radians(alpha)))
    y4 = y3 + ((metresMeasurementToPixelMeasurement(distanceScale, halfPlatformWidth)) * math.sin(
        math.radians(alpha)))

    return x1, y1, x2, y2, x3, y3, x4, y4