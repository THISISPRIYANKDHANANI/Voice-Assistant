import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import speech_recognition as sr
import os
import sys
import win32com.client
import webbrowser
from core.chatbot import get_response
from core.nlp import parse_intent
from core.email_handler import send_email
from core.reminder import set_reminder, reminder_checker
from core.yt_video_player import play_on_youtube  # Assuming you have a youtube.py module for this
from core.utils import extract_subject_and_body  # Assuming you have a utils.py module for this
from core.weather import get_weather
from core.nlp import extract_reminder_parts

 # GUI Window
class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ARIA - Voice Assistant")
        self.root.geometry("300x300")
        self.label = tk.Label(root)
        self.label.pack()

        self.frames = [ImageTk.PhotoImage(img)
               for img in ImageSequence.Iterator(Image.open(r"d:\internship_project\myARIA\ARIA\ARIA\assets\listening.gif"))]

        self.animating = False

    def start_animation(self):
        self.animating = True
        self.update_frame(0)

    def stop_animation(self):
        self.animating = False

    def update_frame(self, index):
        if not self.animating:
            return
        frame = self.frames[index]
        self.label.configure(image=frame)
        self.root.after(100, self.update_frame, (index + 1) % len(self.frames))

# GUI setup
root = tk.Tk()
app = VoiceAssistantGUI(root)

#take command from admin / usesr
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        app.start_animation()
        r.pause_threshold = 1.5
        audio = r.listen(source)
        app.stop_animation()
        try:
            print("Listening...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            return query
        except Exception:
            return "Some Error Occurred. Sorry From Aria"

#Speaker for the text output
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# List available voices (manually check in Control Panel)
# Set the voice to "Microsoft Zira Desktop" (female voice)
for voice in speaker.GetVoices():
    print(voice.GetDescription())  # Prints available voices

speaker.Voice = speaker.GetVoices().Item(1)  # Change to the second voice (e.g., Zira)

def speak(text):
    root.after(0, lambda: speaker.Speak(text))

def assistant_loop():
    speak("Hello I am ARIA your personal A I assistant")

    while True:
        print("Waiting for the wake word 'hello'...")
        wake_word = takeCommand().lower()

        if "hello" in wake_word:
            speak("Yes, I am listening.")

            while True:
                query = takeCommand().lower()
                if "stop" in query or "quit" in query or "shutdown" in query:
                    speak("Goodbye! Have a great day!")
                    sys.exit()

                else:
                    result = parse_intent(query)
                    intent, entities = result
                    if result is None:
                        speak("Sorry, I couldn’t understand your request.")
                        continue  # Go to next loop iteration
                    
                    elif intent == "send_email":
                        recipient_name = entities.get("recipient_name")
                        contacts = {
                            "Uday": "udaidambali281104@gmail.com",
                            "uday": "udaidambali281104@gmail.com",
                            "priyank":"priyankdhanani17@gmail.com"
                        }

                        if not recipient_name:
                            speak("❌ I couldn't find the recipient's name. Who should I send the email to?")
                            recipient_name = takeCommand().lower()
                            if not recipient_name:
                                speak("Sorry, I still didn't catch the recipient's name. Cancelling email.")
                                return

                        to_email = contacts.get(recipient_name.lower())
                        if not to_email:
                            speak(f"❌ I couldn't find the email address for {recipient_name}.")
                            return

                        full_text = entities.get("full_text", "")
    
                        # ✅ Use your existing get_response() method to generate email
                        prompt = f"Generate a professional email for this instruction: '{full_text}'. Return subject and body."
                        response_text = get_response(prompt)  # Your method call

                        # ✅ Use helper to split subject & body from LLM output
                        subject, email_body = extract_subject_and_body(response_text)

                        # 🔄 Ask for user confirmation before sending
                        speak(f"Here is the email")
                        print(f"ARIA: {subject}\n{email_body}")
                        # speak(f"Subject: {subject}")
                        # speak(f"Body: {email_body}")
                        speak("📨 Do you want me to send this email?")

                        confirmation = takeCommand().lower()
                        if "no" in confirmation or "don't" in confirmation or "nahi" in confirmation:
                            speak("Okay, I won’t send the email.")
                        else:
                            success, message = send_email(to_email, subject, email_body)
                            speak("successfully send ")

                    # Reminder
                    elif intent == "set_reminder":
                        # Try to extract message and time from the query
                        message, time_part = extract_reminder_parts(query)
                        if not time_part:
                            speak("What time should I remind you?")
                            time_part = takeCommand()
                        import dateparser
                        reminder_time_str = time_part
                        reminder_time = dateparser.parse(reminder_time_str, settings={'PREFER_DATES_FROM': 'future'})
                        if not reminder_time:
                            speak("Sorry, I couldn't understand the time. Please try again.")
                            continue
                        success, response = set_reminder(reminder_time_str, message)
                        speak(response)
                        print(f"ARIA: {response}")

                    # #Weather
                    # elif intent == "get_weather":
                    #     location = entities.get("location")
                    #     retry_count = 0
                    #     max_retries = 2

                    #     while retry_count <= max_retries:
                    #         if not location:
                    #             if retry_count == 0:
                    #                 speak("Which city would you like the weather for?")
                    #             else:
                    #                 speak("Please try saying the city name again, more clearly.")
                    #             location = takeCommand()

                    #             # Check if location input was valid (including timeout and errors)
                    #             if (location in ["timeout", "could not understand", "network error", "please try again", "microphone error"] or
                    #                 "error" in location.lower() or "try again" in location.lower() or "could not" in location.lower()):
                    #                 retry_count += 1
                    #                 if retry_count > max_retries:
                    #                     speak("I'm having trouble understanding the city name. Please try asking for weather again later.")
                    #                     break
                    #                 location = None
                    #                 continue

                    #         speak(f"Fetching weather updates for {location}...")
                    #         weather_info = get_weather(location)

                    #         # Check if city was found
                    #         if "couldn't find weather information" in weather_info:
                    #             retry_count += 1
                    #             if retry_count <= max_retries:
                    #                 speak(f"I couldn't find {location}. Please try a different city name or a major city nearby.")
                    #                 location = None
                    #                 continue
                    #             else:
                    #                 speak("I'm having trouble finding that city. Please try asking for weather again with a major city name.")
                    #                 break
                    #         else:
                    #             speak(weather_info)
                    #             print(f"Weather: {weather_info}")
                    #             break
                    #Weather Mode
                    elif intent == "get_weather":
                        speak("Entering weather mode.")

                        # Continuous weather mode
                        while True:
                            location = entities.get("location")

                            # If no location in initial command, ask for it
                            if not location:
                                speak("city")
                                city_input = takeCommand().lower()

                                # Check for exit command
                                if "exit" in city_input or "stop" in city_input:
                                    speak("Exiting weather mode.")
                                    break

                                # Handle errors
                                error_responses = ["timeout", "could not understand", "network error", "please try again", "microphone error"]
                                if city_input in error_responses:
                                    speak("I didn't catch that. Please say the city name again.")
                                    continue

                                location = city_input

                            # Get weather for the city
                            speak(f"Getting weather for {location}...")
                            weather_info = get_weather(location)
                            speak(weather_info)
                            print(f"Weather: {weather_info}")

                            # Ask for next city
                            speak("weather for another city")
                            next_input = takeCommand().lower()

                            # Check for exit
                            if "exit weather" in next_input or "stop weather" in next_input or "no" in next_input:
                                speak("Exiting weather mode.")
                                break

                            # Handle errors for next input
                            if next_input in ["timeout", "could not understand", "network error", "please try again", "microphone error"]:
                                speak("I didn't hear you clearly. Let me ask again.")
                                continue

                            # Set location for next iteration
                            location = next_input
                            entities = {"location": location}  # Reset entities for next city

                    #YouTube
                    elif "search" in query and "youtube" in query:
                        search_term = query.replace("search", "").replace("on youtube", "").strip()
                        speak(f"Searching YouTube for {search_term}")
                        webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")

                    #playing YouTube videos
                    # elif "play" in query:
                    #     song = query.replace("play", "").strip()
                    #     speak(f"Playing {song} on YouTube")
                    #     webbrowser.open(f"https://www.youtube.com/results?search_query={song}")  
                    elif intent == "play_media":
                        query = entities.get("query", "")
                        speak(f"🎵 Playing {query} on YouTube.")
                        play_on_youtube(query)


                    #opening notepad
                    elif "notepad" in query:
                        speak("Opening Notepad")
                        os.system("notepad")   

                    elif "search" in query:
                        search_term = query.replace("search", "").strip()
                        speak(f"Searching Google for {search_term}")
                        webbrowser.open(f"https://www.google.com/search?q={search_term}")                       

                    elif intent == "general_knowledge":
                        question = entities.get("query", query)
                        response = get_response(question)
                        speak(response)
                        print(f"ARIA: {response}")

                    elif intent == "chat":
                        speak("Sure, let's chat! What would you like to talk about?")
                        while True:
                            user_input = takeCommand().lower()
                            if "exit chat" in user_input or "stop chat" in user_input:
                                speak("Exiting chat mode.")
                                break
                            else:
                                response = get_response(user_input)
                                speak(response)
                                print(f"ARIA: {response}")

                    elif intent == "unknown":
                        speak("I didn't quite catch that. Can you please rephrase your request?")
                        continue
                    
                    else:
                        # Fallback: treat as general assistant question
                        speak("Let me help you with that.")
                        response = get_response(query)
                        speak(response)
                        print(f"ARIA: {response}")



# Run assistant in background thread so GUI stays responsive
threading.Thread(target=assistant_loop, daemon=True).start()
threading.Thread(target=reminder_checker, daemon=True).start()
root.mainloop()