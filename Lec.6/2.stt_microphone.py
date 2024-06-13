import speech_recognition as sr
from contextlib import contextmanager

#obtain audio from the microphone
r=sr.Recognizer() 

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

with sr.Microphone() as source:
    with noalsaerr():
        print("Please wait. Calibrating microphone...") 
        #listen for 1 seconds and create the ambient noise energy level 
        r.adjust_for_ambient_noise(source, duration=1) 
        print("Say something!")
        audio=r.listen(source)

# recognize speech using Google Speech Recognition 
try:
    print("Google Speech Recognition thinks you said:")
    print(r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("No response from Google Speech Recognition service: {0}".format(e))
