# {0}_{4}T = [

# [ (-s1*s2 + c1*c2)*c3 + (-s1*c2 - s2*c1)*s2, -(-s1*s2 + c1*c2)*s2 + (-s1*c2 - s2*c1)*c3, 0, L1*c1 + L2*(-s1*s2 + c1*c2) + L3*((-s1*s2 + c1*c2)*c3 + (-s1*c2 - s2*c1)*s2)],
# [ (-s1*s2 + c1*c2)*s2 + (s1*c2 + s2*c1)*c3,   (-s1*s2 + c1*c2)*c3 - (s1*c2 + s2*c1)*s2, 0,   L1*s1 + L2*(s1*c2 + s2*c1) + L3*((-s1*s2 + c1*c2)*s2 + (s1*c2 + s2*c1)*c3)],
# [ 0, 0, 1, 0],
# [ 0, 0, 0, 1]

# ]

# T = [
# [(-sin(T1)*sin(T2) + cos(T1)*cos(T2))*cos(T3) - (-sin(T1)*cos(T2) - sin(T2)*cos(T1))*sin(T3), (-sin(T1)*sin(T2) + cos(T1)*cos(T2))*sin(T3) + (-sin(T1)*cos(T2) - sin(T2)*cos(T1))*cos(T3), 0, L1*cos(T1) + L2*(-sin(T1)*sin(T2) + cos(T1)*cos(T2)) + L3*((-sin(T1)*sin(T2) + cos(T1)*cos(T2))*cos(T3) - (-sin(T1)*cos(T2) - sin(T2)*cos(T1))*sin(T3))],
# [-(-sin(T1)*sin(T2) + cos(T1)*cos(T2))*sin(T3) + (sin(T1)*cos(T2) + sin(T2)*cos(T1))*cos(T3),  (-sin(T1)*sin(T2) + cos(T1)*cos(T2))*cos(T3) + (sin(T1)*cos(T2) + sin(T2)*cos(T1))*sin(T3), 0,  L1*sin(T1) + L2*(sin(T1)*cos(T2) + sin(T2)*cos(T1)) + L3*(-(-sin(T1)*sin(T2) + cos(T1)*cos(T2))*sin(T3) + (sin(T1)*cos(T2) + sin(T2)*cos(T1))*cos(T3))],
# [ 0, 0, 1, 0],
# [ 0, 0, 0, 1]
# ]

import math

L1 = 22.5
L2 = 120
L3 = 80

t1 = 38.674090
t2 = 54.359546
t3 = 103.033636

def c(angle):
    return math.cos(math.radians(angle))

def s(angle):
    return math.sin(math.radians(angle))


T_x = L1*c(t1) + L2*(-s(t1)*s(t2) + c(t1)*c(t2)) + L3*((-s(t1)*s(t2) + c(t1)*c(t2))*c(t3) - (-s(t1)*c(t2) - s(t2)*c(t1))*s(t3))
T_y = L1*s(t1) + L2*(s(t1)*c(t2) + s(t2)*c(t1)) + L3*(-(-s(t1)*s(t2) + c(t1)*c(t2))*s(t3) + (s(t1)*c(t2) + s(t2)*c(t1))*c(t3))

r_0_0 = (-s(t1)*s(t2) + c(t1)*c(t2))*c(t3) - (-s(t1)*c(t2) - s(t2)*c(t1))*s(t3)
r_0_1 = (-s(t1)*s(t2) + c(t1)*c(t2))*s(t3) + (-s(t1)*c(t2) - s(t2)*c(t1))*c(t3)
r_0_2 = 0
r_1_0 = -(-s(t1)*s(t2) + c(t1)*c(t2))*s(t3) + (s(t1)*c(t2) + s(t2)*c(t1))*c(t3)
r_1_1 = (-s(t1)*s(t2) + c(t1)*c(t2))*c(t3) + (s(t1)*c(t2) + s(t2)*c(t1))*s(t3)
r_1_2 = 0
r_2_0 = 0
r_2_1 = 0
r_2_2 = 1

alpha = -1 * math.atan2(r_1_0, r_0_0)

'''
    Correct Values:
        T_x = 90
        T_y = 120

        alpha = 10 degrees
'''

print('(', T_x, T_y, ')')
print('alpha = ', math.degrees(alpha))

new_r_1_0 = math.sin(-alpha)
new_r_0_0 = math.cos(alpha)
print('old_r_1_0 = ', r_1_0)
print('old_r_0_0 = ', r_0_0)
print('new_r_1_0 = ', new_r_1_0)
print('new_r_0_0 = ', new_r_0_0)