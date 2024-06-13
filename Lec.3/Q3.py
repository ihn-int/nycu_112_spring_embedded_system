import RPi.GPIO as gpio
import math
import time
import random
import Q1

# random #################
random.seed(time.time())
guess = False
target = 0
threshold = 3

sensor = Q1.gy801()
compass = sensor.compass

try:
    while True:
        if guess == False : 
            target = random.uniform(0, 360)
            guess = True
        else :
            compass.getX()
            compass.getY()
            compass.getZ()
            mag = compass.getHeading()
            if mag >= target - threshold and mag <= target + threshold :
                print("Correct answer:", target)
                guess = False
            elif mag < target : 
                print("Your heading: %.3f is too small" % mag)
            elif mag > target :
                print("Yout heading: %.3f is too large" % mag)
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")
