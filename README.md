# Jarvis Voice Assistant

A Jarvis-style voice assistant written in Python. Say the wake word **"Jarvis"**, then speak a command.

This is a rebuild of an earlier version I made as a college project (2025-2026), after the original files were lost.

## Features

- Opens websites: Google, YouTube, Facebook and X
- Plays songs from your own music library
- Reads top news headlines aloud (NewsAPI)
- Answers other questions through the OpenAI API (needs an OpenAI account with API credit)
- Speaks its replies using text-to-speech

## Requirements

- Python 3.9 or newer
- A working microphone and an internet connection (speech recognition uses Google's online service)
- Libraries:

```
pip install SpeechRecognition pyttsx3 pyaudio requests openai python-dotenv
```

## Setup

1. Download or clone this repository.
2. Create a file named `musiclibrary.py` in the same folder, with song names (lowercase) and links:

```python
music = {
    "song name": "https://www.youtube.com/watch?v=...",
}
```

3. Get your own API keys from [OpenAI](https://platform.openai.com) and [NewsAPI](https://newsapi.org).
4. Copy `.env.example` to a new file named `.env` in the same folder and put your keys in it. **Never upload your `.env` file or put keys in the code.**

```
OPENAI_API_KEY=your-key-here
NEWS_API_KEY=your-key-here
```

5. Run:

```
python jarvis_assistant.py
```

## How to use

1. Say **"Jarvis"**. The assistant replies "Yes sir, I am listening".
2. Say a command, for example:
   - "open YouTube"
   - "play" followed by a song name from your library
   - "news"
   - any other question, which is sent to the AI service

## Limitations

- Website commands must match exactly (for example "open YouTube").
- English only.
- Requires internet for speech recognition, news and AI answers.
- AI answers fail if the OpenAI account has no API credit.
- The number of news results depends on your NewsAPI plan and country.

## Tools

Python, SpeechRecognition, pyttsx3, requests, python-dotenv, OpenAI API, NewsAPI
