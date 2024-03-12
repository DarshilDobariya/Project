from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import webbrowser
import re


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    if not engine.isBusy(): 
        engine.say(text)
        engine.runAndWait()

def process_command(command):

    if "hello" in command:
        speak("Hello! How can I assist you with your research today?")
        return "Hello! How can I assist you with your research today?"
    elif "who are you" in command:
        speak("I am your assistant. You can ask me for information on scientific papers, define scientific terms, or perform calculations.")
        return "I am your assistant. You can ask me for information on scientific papers, define scientific terms, or perform calculations."
    elif "thank you" in command:
        speak("You're welcome!")
        return "You're welcome!"
    elif "goodbye" in command:
        speak("Goodbye! Have a productive day!")
        return "Goodbye! Have a productive day!"
    elif "define" in command:
        term = command.split("define")[-1].strip()
        definition = get_definition(term)
        return f"The definition of {term} is: {definition}"
    
    elif any(keyword in command for keyword in ['paper', 'papers', 'research', 'study', 'article']):
        speak("What topic would you like to research?")
        topic = extract_topic(command)
        # topic = listen()
        print(topic)
        if topic:
            speak("Opening search results in your web browser.")
            google_scholer(topic)
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
    elif "youtube" in command:
        open_youtube()
        return "Opening YouTube."
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

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def extract_topic(command):
    # Define keywords related to papers, research, etc.
    keywords = ['paper', 'papers', 'research', 'study', 'article']

    # Regular expression pattern to extract topic
    pattern = rf"\b({'|'.join(keywords)})\b\s+(?:of\s+)?(.+)$"

    # Search for pattern in command
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        return match.group(2).strip()
    else:
        return None

def get_definition(term):
    print(term)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{term}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            meanings = data[0].get('meanings', [])
            if meanings:
                first_meaning = meanings[0].get('definitions', [])
                if first_meaning:
                    return first_meaning[0]['definition']
            return "No definition found."
        except Exception as e:
            print("Error parsing JSON:", e)
            return "Error parsing response."
    else:
        print("Error:", response.status_code)
        return "Error fetching data."

    # soup = BeautifulSoup(response.text, 'html.parser')
    # list_items = soup.find_all('li')
    # # Iterate through each list item
    # for item in list_items:
    #     # Find the div element inside the list item
    #     div_element = item.find('div', class_='BNeawe s3v9rd AP7Wnd')
    #     if div_element:
    #         # Extract the content
    #         content = div_element.text.strip()
    #         print("Content:", content)
    #         return content
    
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

def google_scholer(papers):
    # for paper in papers:
        link = f'https://scholar.google.com/scholar?&q='+papers
        webbrowser.open(link)

def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return str(e)

def main():
    speak("Hello! How can I assist you with your research today?")
    while True:
        try:
            command = listen()
            if command:
                response = process_command(command)
                speak(response)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()

def index(request):
    # speak("Hello! How can I assist you with your research today?")
    if request.method == 'POST':
        command = request.POST.get('command')
        response = process_command(command)
        speak(response)  # Speak the response
        return JsonResponse({'response': response})
        # return HttpResponse(response)
    else:
        return render(request, 'voiceassistant/index.html')