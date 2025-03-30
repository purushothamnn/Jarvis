import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
for i in voices:
    print(i)