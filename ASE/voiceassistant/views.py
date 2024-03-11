from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import webbrowser


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

def get_definition(term):
    print(term)
    url = f"https://www.google.com/search?q=define+{term}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    list_items = soup.find_all('li')
    # Iterate through each list item
    for item in list_items:
        # Find the div element inside the list item
        div_element = item.find('div', class_='BNeawe s3v9rd AP7Wnd')
        if div_element:
            # Extract the content
            content = div_element.text.strip()
            print("Content:", content)
            return content
    
    # definition = soup.find("p").text
    # return definition

# def get_paper_info(topic):
    # Use SerpApi to search for documents on Google Scholar
    # serpapi_key = "e0ed4736fdf12e0ae16722523061c5a611bc7ae4195f757fd6e25da59dcd24aa"
    # params = {
    #     "engine": "google_scholar",
    #     "q": topic,
    #     "api_key": serpapi_key
    # }
    # response = requests.get("https://serpapi.com/search", params=params)
    # data = response.json()
    # papers = []
    # for result in data.get("organic_results", []):
    #     title = result.get("title", "")
    #     link = result.get("link", "")
    #     papers.append({"title": title, "link": link})
    # return papers

def open_in_browser(papers):
    # for paper in papers:
        webbrowser.open('https://scholar.google.com/scholar?&q='+papers)

def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return str(e)

def main():
    speak("Hello! How can I assist you with your research today?")
    while True:
        command = listen()
        if command:
            response = process_command(command)
            speak(response)

if __name__ == "__main__":
    main()

def index(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        response = process_command(command)
        return HttpResponse(response)
    else:
        return render(request, 'voiceassistant/index.html')