# core/reminder.py

import time
import threading
from datetime import datetime
import win32com.client
import dateparser  # <-- Add this

# Use Windows TTS
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Stores reminders as tuples: (datetime_obj, message)
reminders = []

def set_reminder(reminder_time_str, message):
    # Try to parse natural language time
    reminder_time = dateparser.parse(reminder_time_str, settings={'PREFER_DATES_FROM': 'future'})
    if not reminder_time:
        return False, "Sorry, I couldn't understand the time. Please try again."
    now = datetime.now()
    if reminder_time <= now:
        return False, "The time you provided is in the past."
    reminders.append((reminder_time, message))
    return True, f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')}"

def reminder_checker():
    while True:
        now = datetime.now()
        for reminder in reminders[:]:
            reminder_time, message = reminder
            if now >= reminder_time:
                speaker.Speak(f"Reminder: {message}")
                reminders.remove(reminder)
        time.sleep(10)  # Check more frequently for better accuracy
