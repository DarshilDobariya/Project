# vs.py

import webbrowser
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
   if "hello" in command:
        return "Hello! How can I assist you with your research today?"
   elif "who are you" in command:
        return "I am a research assistant. You can ask me for information on scientific papers, define scientific terms, or perform calculations."
   elif "thank you" in command:
        return "You're welcome!"
   elif "goodbye" in command:
        return "Goodbye! Have a productive day!"
   elif "define" in command:
        term = command.split("define")[-1].strip()
        definition = get_definition(term)
        return f"The definition of {term} is: {definition}"
   elif "paper" in command or "research" in command:
        speak("What topic would you like to research?")
        topic = listen()
        if topic:
            speak("Opening search results in your web browser.")
            open_in_browser(topic)
            return "I have opened the search results in your web browser."
            # get_paper_info(topic)
            # if papers:
            #     speak("Opening search results in your web browser.")
            #     open_in_browser(papers)
            #     return "I have opened the search results in your web browser."
            # else:
            #     return f"Sorry, I couldn't find any relevant papers on {topic}."
        else:
            return "Sorry, I couldn't understand the topic you mentioned."

   elif "calculate" in command:
        expression = command.split("calculate")[-1].strip()
        result = calculate(expression)
        return f"The result of {expression} is {result}."
   else:
        return "I'm sorry, I didn't understand that."
   
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print("You said: " + command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""
    except Exception as e:
        print("An error occurred:", e)
        return ""

# Your listen function implementation

# def get_definition(term):
    # Your get_definition function implementation

# def open_in_browser(papers):
    # Your open_in_browser function implementation

# def calculate(expression):
    # Your calculate function implementation

def handle_voice_request():
    speak("Hello! How can I assist you with your research today?")
    command = listen()
    if command:
        response = process_command(command)
        return response
    return "Sorry, I didn't understand that."

