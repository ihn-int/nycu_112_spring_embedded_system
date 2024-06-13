import RPi.GPIO as gpio
import time
BTN_PIN = 12
gpio.setmode(gpio.BOARD)
gpio.setup(BTN_PIN, gpio.IN)

pre = gpio.HIGH
crt = gpio.LOW

try:
    time.sleep(0.1)
    while True:
        crt = gpio.input(BTN_PIN)
        if crt == gpio.HIGH and pre == gpio.LOW :
            print("PRESS")
        pre = crt
except KeyboardInterrupt:
    print("DONE")
