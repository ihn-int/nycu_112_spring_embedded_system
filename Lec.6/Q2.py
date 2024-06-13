from gtts import gTTS
import os
import RPi.GPIO as GPIO
import time
import random
import speech_recognition as sr

# voice command
command = "command function override code 10"
    # : override accepted.
r = sr.Recognizer()

# ultrasonic and RPi
TRIG_PIN = 14
ECHO_PIN = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setip(ECHO_PIN, GPIO.IN)

def measure():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW : # no echo
        pulse_start = time.time();
    while GPIO.input(ECHO_PIN) == GPIO.HIGH: # get echo
        pulse_end = time.time();
    return (pulse_end - pulse_start) * 343 / 2 * 100 # in cm
    
# create a wav file for Q2
def create_command(_command):
    tts = gTTS(text = _command, lang = "en")
    tts.save("cmd.mp3")
    os.system("ffmpeg -i cmd.mp3 cmd.wav")
    
def create_response(distance):
    tts = gTTS(text = "The distance is {0}.".format(distance))
    tts.save()
    
    
try:
    random.seed(time.time())
    create_command(command)
    time.sleep(random.randint(2, 5)) #imitation a delay for human speaking
    with sr.AudioFile("cmd.wav") as source:
        audio = r.record(source)
    if r.recognize_google(audio) == command :
        
        
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("No response from Google Speech Recognition service: {0}".format(e))
finally:
    GPIO.cleanup()