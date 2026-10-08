
from openai import OpenAI, OpenAIError, RateLimitError
from dotenv import load_dotenv
import importlib.util
import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()
load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def aiprocess(command):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-6-astra",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def process_command(command):
    normalized_command = command.lower().strip()

    if normalized_command == "open google":
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif normalized_command == "open youtube":
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif normalized_command == "open facebook":
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif normalized_command == "open x":
        speak("Opening x")
        webbrowser.open("https://www.x.com")
    elif normalized_command.startswith("play "):
        song = normalized_command.removeprefix("play ").strip()
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found")
    elif "news" in normalized_command:
        if not news_api_key:
            speak("The news service is not configured")
            return

        try:
            response = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "in", "apiKey": news_api_key},
                timeout=10,
            )
            response.raise_for_status()
            articles = response.json().get("articles", [])[:5]
        except requests.RequestException as error:
            print(f"News request failed: {error}")
            speak("Sorry, I could not get the news")
            return

        if articles:
            for article in articles:
                title = article.get("title")
                if title:
                    speak(title)
        else:
            speak("There are no news articles available")
    else:
        try:
            output = aiprocess(command)
        except RateLimitError as error:
            print(f"OpenAI rate limit or quota error: {error}")
            speak("OpenAI is unavailable because the API quota or rate limit was reached.")
            return
        except OpenAIError as error:
            print(f"OpenAI request failed: {error}")
            speak("Sorry, the AI service is unavailable right now.")
            return
        if output:
            speak(output)
        else:
            speak("Sorry, I did not get a response.")
        
        

if __name__ == "__main__":
    if importlib.util.find_spec("pyaudio") is None:
        raise SystemExit(
            "PyAudio is required for microphone input. Use the Python 3.13 "
            "environment where PyAudio is installed."
        )

    speak("Initializing Jarvis.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for Jarvis...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            if word.lower().strip() == "jarvis":
                speak("Yes, I am listening.")
                with sr.Microphone() as source:
                    print("Listening for your command...")
                    audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                process_command(command)
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as error:
            print(f"Google Speech Recognition request failed: {error}")
        except Exception as error:
            print(f"Unexpected error ({type(error).__name__}): {error}")
        