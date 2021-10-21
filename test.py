import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
text = 'Hello, how are you?'
engine.say(text)
engine.runAndWait()
