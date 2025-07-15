# Voice-Assistant

COMPANY: Oasis Infobyte

NAME: Priyank Dhanani

"INTERN ID: OIB/J1/IP3779

*DOMAIN: PYTHON PROGRAMMING

*DURATION: 4 WEEEKS


# ARIA - Voice Assistant

ARIA is an intelligent, friendly AI voice assistant for Windows, built with Python. It can recognize your speech, answer questions, send emails, set reminders, fetch weather updates, play YouTube videos, and more—all through a simple GUI.

## Features

- 🎤 **Voice Recognition**: Listen and respond to your voice commands.
- 🤖 **Conversational AI**: Uses Google Gemini (via `google-genai`) for natural, helpful responses.
- 📧 **Email Assistant**: Compose and send emails by voice.
- ⏰ **Reminders**: Set reminders and get notified.
- 🌦️ **Weather Updates**: Get weather info for any city.
- 📺 **YouTube Integration**: Search and play videos on YouTube.
- 📝 **General Knowledge**: Ask questions and get answers.
- 🗂️ **Simple GUI**: Animated listening indicator and easy-to-use interface.

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/aria-voice-assistant.git
   cd aria-voice-assistant/ARIA/ARIA
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

   If you get errors with `pyaudio`, download the appropriate wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it:
   ```
   pip install PyAudio‑0.2.11‑cp3xx‑cp3xx‑win_amd64.whl
   ```

3. **Set up your Google Gemini API key:**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_google_gemini_api_key_here
     ```

4. **Run the assistant:**
   ```
   python main.py
   ```

## Usage

- Say "hello" to activate ARIA.
- Ask ARIA to send emails, set reminders, get weather, play YouTube videos, or answer questions.
- To stop ARIA, say "stop", "quit", or "shutdown".

## Project Structure

```
ARIA/
├── assets/
│   └── listening.gif
├── core/
│   ├── chatbot.py
│   ├── email_handler.py
│   ├── nlp.py
│   ├── reminder.py
│   ├── utils.py
│   ├── weather.py
│   └── yt_video_player.py
├── main.py
└── requirements.txt
```

## Requirements

- Python 3.10+
- See `requirements.txt` for all dependencies.

## Credits

- [Google Gemini API](https://ai.google.dev/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [Pillow](https://pypi.org/project/Pillow/)
- [dateparser](https://pypi.org/project/dateparser/)

## License

MIT License

---

# output
![img](https://github.com/user-attachments/assets/a9882558-7568-4c9d-8efb-e72b48328b39)
![img](https://github.com/user-attachments/assets/d50d2c15-2dd0-4a0a-8013-84e5a549feb5)
![img](https://github.com/user-attachments/assets/4f53ed55-dff3-4eb6-9ae4-be5fdaec76f6)
![img](https://github.com/user-attachments/assets/4ca891ef-b09a-448d-9cbd-ba78cded1635)
