import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import user_config
import smtplib, ssl
import openai_request as ai
import image_generation
import mtranslate

engine = pyttsx3.init()
voices = engine.getProperty('voices')       
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def command():
    content = " "
    while content == " ":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language='en-in')
            content = mtranslate.translate(content,to_language="en-in")
            print("You Said............" + content)
        except Exception as e:
            print("Please try again...")
    
    return content

def main_process():
    jarvis_chat = []
    while True:
        request = command().lower()
        if "hello" in request:
            speak("Welcome, How can i help you.")
       
        elif "play" in request and "song" in request:
            # Extract the song name from the request
            song = request.replace("play", "").replace("song", "").strip()
            if song:
                speak(f"Playing {song} on YouTube")
                pwk.playonyt(song)
            else:
                speak("Please tell me which song to play")
      
        elif "say time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + str(now_time))
        elif "say date" in request:
            now_time = datetime.datetime.now().strftime("%d:%m")
            speak("Current date is " + str(now_time))
        elif "new task" in request:
            task = request.replace("new task", "")
            task = task.strip()
            if task != "":
                speak("Adding task : "+ task)
                with open ("todo.txt", "a") as file:
                    file.write(task + "\n")
        elif "speak task" in request:
            with open ("todo.txt", "r") as file:
                speak("Work we have to do today is : " + file.read())
        elif "show work" in request:
            with open ("todo.txt", "r") as file:
                tasks = file.read()
            notification.notify(
                title = "Today's work",
                message = tasks
            )
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")
        elif "open" in request:
            query = request.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "wikipedia" in request:
            request = request.replace("jarvis ", "")
            request = request.replace("search wikipedia ", "")
            result = wikipedia.summary(request, sentences=2)
            speak(result)
        elif "search google" in request:
            request = request.replace("jarvis ", "")
            request = request.replace("search google ", "")
            webbrowser.open("https://www.google.com/search?q="+request)
      
        elif "send whatsapp" in request:
            pwk.sendwhatmsg("+910123456789", "Hi, How are you", 2, 10, 30)
       
        elif "image" in request:
            request = request.replace("jarvis ", "")
            image_generation.generate_image(request)
        elif "ask ai" in request:
            jarvis_chat = []
            request = request.replace("jarvis ", "")
            request = request.replace("ask ai ", "")
            jarvis_chat.append({"role": "user","content": request})

            response = ai.send_request(jarvis_chat)

            speak(response)
        elif "clear chat" in request:
            jarvis_chat = []
            speak("Chat Cleared")
        else:
            request = request.replace("jarvis ", "")

            jarvis_chat.append({"role": "user","content": request})
            response = ai.send_request(jarvis_chat)

            jarvis_chat.append({"role": "assistant", "content": response})
            speak(response)

if __name__ == "__main__":
    main_process()