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
distance = 0

try:
    while True:
        duration = 0.2
        accel = mpu9250.readAccel()
        ax = G * round(accel['x'], 3)
        ay = G * round(accel['y'], 3)
        az = G * round(accel['z'], 3)
        #'''
        print(" ax = " , ( accel['x'] ))
        print(" ay = " , ( accel['y'] ))
        print(" az = " , ( accel['z'] ))
        #'''
        # total accelerate 
        at = sqrt(ax*ax + ay*ay + az*az)	

        # delta dis = 1/2 * at * duration**2
        delta = 0.5 * at * duration * duration
        distance += delta
        print("delta:", delta)
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
    print("total distance:", distance)
    sys.exit()
