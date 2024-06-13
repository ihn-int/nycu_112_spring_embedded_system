import RPi.GPIO as gpio
import time
from math import *
import Q1

BTN_PIN = 12
TRIGGER_PIN = 16
ECHO_PIN = 18

VELO = 343

gpio.setmode(gpio.BOARD)
gpio.setup(TRIGGER_PIN, gpio.OUT)
gpio.setup(ECHO_PIN, gpio.IN)
gpio.setup(BTN_PIN, gpio.IN)

def measure() -> float :
    gpio.output(TRIGGER_PIN, gpio.HIGH)
    time.sleep(0.00001)
    gpio.output(TRIGGER_PIN, gpio.LOW)
    pulse_start = time.time()
    while gpio.input(ECHO_PIN) == gpio.LOW :
        pulse_start = time.time()
    while gpio.input(ECHO_PIN) == gpio.HIGH:
        pulse_end = time.time()
    t = pulse_end - pulse_start
    d = (t * VELO) / 2
    return d * 100 # return in cm

def distance(a, b, angle) -> float :
    return sqrt(a*a + b*b - 2*a*b*cos(abs(radians(angle))))


pre_btn = gpio.HIGH
crt_btn = gpio.LOW
measure_state = 0
dis_1 = 0
dis_2 = 0
mag_1 = 0
mag_2 = 0



try:
    sensor = Q1.gy801()
    compass = sensor.compass

    while True:
        crt_btn = gpio.input(BTN_PIN)
        if crt_btn == gpio.HIGH and pre_btn == gpio.LOW :
            # edge trigger, press
            if measure_state == 0 :
                dis_1 = measure()
                #print( compass.getHeading() )
                compass.getX()
                compass.getY()
                compass.getZ()
                mag_1 = compass.getHeading()
                measure_state = 1
                print("mag: %d, distance: %.3f" % (mag_1, dis_1))
                print("1st object measurement completed")
            elif measure_state == 1 :
                dis_2 = measure()
                compass.getX()
                compass.getY()
                compass.getZ()
                mag_2 = compass.getHeading()
                measure_state = 2
                print("mag: %d, distance: %.3f" % (mag_2, dis_2))
                print("2nd object measurement completed")
        if measure_state == 2 :
            # calculate the distance between 1 and 2
            print("distance: ", distance(dis_1, dis_2, mag_1 - mag_2))
            measure_state = 0
        pre_btn = crt_btn

except KeyboardInterrupt:
    print("Execption: KeyboardInterrupt")
finally:
    gpio.output(TRIGGER_PIN, gpio.LOW)
    gpio.cleanup()
