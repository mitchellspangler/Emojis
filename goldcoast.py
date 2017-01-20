# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import emoji
import sys


def replacements(string):
    #  lower :
    string = string.lower()
    #  characters :
    string = string.replace(" ", "")
    string = string.replace("underscore", "_")
    string = string.replace("plus", "+")
    string = string.replace("minus", "-")
    #  numbers :
    string = string.replace("zero", "0")
    string = string.replace("one", "1")
    string = string.replace("two", "2")
    string = string.replace("three", "3")
    string = string.replace("four", "4")
    string = string.replace("five", "5")
    string = string.replace("six", "6")
    string = string.replace("seven", "7")
    string = string.replace("eight", "8")
    string = string.replace("nine", "9")

    return string;


def emojiTime(workString):
    normalOutput(workString)
    source = replacements(workString)
    print("This is what we think you said if it was an emoji: " + emoji.emojize(":" + workString + ":", use_aliases=True))
    return;


def normalOutput(source):
    print("This is what Google Speech Recognition thought you said: " + source)


# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        print("Starting request . . .")
        emojiTime(recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    print("Request finished . . . ")


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
import time

for _ in range(10000):
    time.sleep(0.1)  # we're still listening even though the main thread is doing other things
    if _ == 0:
        print("Speech Recognition System starting up . . . ")
        print("Keep sleeping until something is said . . .")
    if (_ % 100 == 0) & (_ != 0):
        print("Slept for the " + str(_) + "th time")
stop_listening()  # calling this function requests that the background listener stop listening
