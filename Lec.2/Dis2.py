# coding: utf-8
## @package faboMPU9250
#  This is a library for the FaBo 9AXIS I2C Brick.
#  http://fabo.io/202.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import libmpu9250
import time
import sys
from math import *

mpu9250 = libmpu9250.MPU9250()

G = 9.8
num_of_test = 10
bias = []
tax = 0
tay = 0
taz = 0
tat = 0

try:
    for i in range(num_of_test):
        duration = 0.2
        accel = mpu9250.readAccel()
        ax = G * accel['x']
        ay = G * accel['y']
        az = G * accel['z']
        '''
        print("Case #" + str(i))
        print(" ax = " , ( ax ))
        print(" ay = " , ( ay ))
        print(" az = " , ( az ))
        #'''
        # total accelerate 
        at = sqrt(ax*ax + ay*ay + az*az)
        bias.append([ax, ay, az, at])
        tax += ax
        tay += ay
        taz += az
        tat += at

        '''
        gyro = mpu9250.readGyro()
        print(" gx = " , ( gyro['x'] ))
        print(" gy = " , ( gyro['y'] ))
        print(" gz = " , ( gyro['z'] ))

        mag = mpu9250.readMagnet()
        print(" mx = " , ( mag['x'] ))
        print(" my = " , ( mag['y'] ))
        print(" mz = " , ( mag['z'] ))
        print()
        '''
        time.sleep(0.2)

except KeyboardInterrupt:
    sys.exit()
finally:
    for i in range(num_of_test):
        print("%f,%f,%f,%f" %(bias[i][0], bias[i][1], bias[i][2], bias[i][3]))
    print("%f,%f,%f,%f" %(tax/num_of_test, tay/num_of_test, taz/num_of_test, tat/num_of_test))
