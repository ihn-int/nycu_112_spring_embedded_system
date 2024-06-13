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
ACC = 20
#_time = 0
distance = 0

try:
    while True:
        duration = 0.2
        
        accel = mpu9250.readAccel()

        ax = accel['x'] * G
        ay = accel['y'] * G
        az = accel['z'] * G
        '''
        print(" ax = " , ( ax ))
        print(" ay = " , ( ay ))
        print(" az = " , ( az ))
        '''

        at = sqrt(ax*ax + ay*ay + az*az)	
        print(at)
        if at >= ACC :
            print("WARNING: You're FALLING!!!")
        #distance += 0.5 * at
        #print("distance:", distance)
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
        time.sleep(0.1)

except KeyboardInterrupt:
    sys.exit()
