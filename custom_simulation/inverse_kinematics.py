import numpy as np
import tinyik as ik
import math

platformWidth = 160.0
halfPlatformWidth = platformWidth / 2

alpha = 10.0  # degrees

x2 = 90.0 - (halfPlatformWidth * math.cos(math.radians(alpha)))
y2 = 120.0 + (halfPlatformWidth * math.sin(math.radians(alpha)))

# Defining actuator
leg = ik.Actuator(['z', [22.5, 0.0, 0.0], 'z', [120.0, 0.0, 0.0]])

# Sets the position of the end effector
leg.ee = [x2, y2, 0.0]

print(np.rad2deg(leg.angles))
