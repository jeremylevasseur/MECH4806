import math


# ================ DYNAMICS ================

'''
    This function returns the linear acceleration of the ball
    that is caused by a platform angle of tilt.

    The math was done on paper using the following equations:
        T = I * alpha       =>      (Torque) = (Moment of Inertia) * (Angular Acceleration)
        F = m * a           =>      (Force) = (Mass) * (Linear Acceleration)

    Inputs:
        gravity         =>      metres per second
        angleOfTilt     =>      degrees
    
    Outputs:
        acceleration    =>      metres per second^2

'''
def angleOfTiltToAcceleration(gravity, angleOfTilt):
    return (5/7) * gravity * math.sin(math.radians(angleOfTilt))


# ================ CONSTANT ACCELERATION KINEMATICS ================

def distanceMoved_1(v_i, a, t):
    return ( v_i * t ) + ( 0.5 * a * (t**2) )

# def distanceMoved_2(v_i, v_f, t):
#     return 0.5 * (v_i + v_f) * t

