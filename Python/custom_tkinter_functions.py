import math

def thirdpoint(a, b, c):
    result = []
    y=((a**2)+(b**2)-(c**2))/(a*2)
    x = math.sqrt((b**2)-(y**2))
    result.append(x)
    result.append(y)
    return result