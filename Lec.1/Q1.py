import RPi.GPIO as GPIO
import time

# pin declaration
LED_PIN  = 12
TRIG_PIN = 16
ECHO_PIN = 18

v = 343
H_FREQ = 0.25
L_FREQ = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    t = pulse_end - pulse_start
    d = t * v
    d /= 2
    return d * 100

try:
    while True:
        dis = measure()
        print(dis)
        if dis < 50 :
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(H_FREQ)
        elif dis >= 50 and dis < 100 :
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(L_FREQ)
        else :
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(H_FREQ)
        
        dis = measure()
        print(dis)
        if dis < 50 :
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(H_FREQ)
        elif dis >= 50 and dis < 100 :
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(L_FREQ)
        else :
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(H_FREQ)

except KeyboardInterrupt:
    print("Stop")

finally:
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    GPIO.cleanup()
