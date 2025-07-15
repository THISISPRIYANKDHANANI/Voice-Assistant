# # core/nlp.py

# def parse_intent(text):
#     """
#     Basic NLP parser to detect user intent from input text.
#     Returns a tuple (intent, entities)
#     """

#     text = text.lower()
#     entities = {}

#     # Email
#     if "send email" in text or "email" in text:
#         return "send_email", entities

#     # Reminder
#     elif "remind me" in text or "set reminder" in text:
#         return "set_reminder", entities

#     # Weather
#     elif "weather" in text:
#         entities["location"] = extract_location(text)
#         return "get_weather", entities

#     # Smart Home
#     elif "turn on" in text or "turn off" in text or "light" in text:
#         return "control_device", entities

#     # General Knowledge
#     elif "who is" in text or "what is" in text or "how" in text:
#         return "general_knowledge", {"query": text}

#     # Default (chat or unknown)
#     else:
#         return "chat", {"query": text}


# def extract_location(text):
#     # Very basic location extractor — can use spaCy later
#     for word in text.split():
#         if word.istitle():
#             return word
#     return "your location"
"""
Natural Language Processing module for ARIA
Handles intent recognition and entity extraction from user speech

Author: Your Name
Date: 2024
"""

import re

def parse_intent(text):
    """
    Analyze user input to determine what they want to do

    Args:
        user_input (str): The text from speech recognition

    Returns:
        tuple: (intent_name, extracted_entities)
    """

    text = text.lower()
    entities = {}

    # Email
    # 📧 Email Intent + Extract recipient
    if ("send email" in text or "email" in text or text.strip().startswith("send")):
        match = re.search(r"send (an )?email to (\w+)", text)
        if match:
            entities["recipient_name"] = match.group(2).strip()
        entities["full_text"] = text
        return "send_email", entities
    
    # Play Media
    if "play" in text:
        entities["query"] = text.replace("play", "").strip()
        return "play_media", entities

    # Reminder
    elif "remind me" in text or "set reminder" in text:
        return "set_reminder", entities

    # Weather queries
    elif "weather" in text:
        location = extract_location(text)
        if location:
            entities["location"] = location
        return "get_weather", entities

    # Smart Home
    elif "turn on" in text or "turn off" in text or "light" in text:
        return "control_device", entities

    # General Knowledge
    elif "who is" in text or "what is" in text or "how" in text or "search" in text:
        return "general_knowledge", {"query": text}

    # Casual Chat (optional keyword trigger)
    elif "talk" in text or "chat" in text:
        return "chat", {"query": text}

    # Unknown → treat as chat fallback
    return "unknown", {"query": text}
    
def extract_location(text):
    """
    Extract location from weather query text.
    Looks for common patterns and handles various city name formats.
    """
    text = text.lower()

    # Common city name mappings for speech recognition errors
    city_corrections = {
        # International Cities
        "london": "London",
        "new york": "New York",
        "newyork": "New York",
        "tokyo": "Tokyo",
        "paris": "Paris",

        # Major Indian Cities
        "delhi": "Delhi",
        "mumbai": "Mumbai",
        "bangalore": "Bangalore",
        "chennai": "Chennai",
        "kolkata": "Kolkata",
        "hyderabad": "Hyderabad",
        "pune": "Pune",
        "jaipur": "Jaipur",
        "lucknow": "Lucknow",
        "kanpur": "Kanpur",
        "nagpur": "Nagpur",
        "indore": "Indore",
        "thane": "Thane",
        "bhopal": "Bhopal",
        "visakhapatnam": "Visakhapatnam",
        "pimpri": "Pimpri-Chinchwad",
        "patna": "Patna",
        "ghaziabad": "Ghaziabad",
        "ludhiana": "Ludhiana",
        "agra": "Agra",
        "nashik": "Nashik",

        # All Gujarat Districts
        "ahmedabad": "Ahmedabad",
        "amreli": "Amreli",
        "anand": "Anand",
        "aravalli": "Aravalli",
        "banaskantha": "Banaskantha",
        "bharuch": "Bharuch",
        "bhavnagar": "Bhavnagar",
        "botad": "Botad",
        "chhota udaipur": "Chhota Udaipur",
        "dahod": "Dahod",
        "dang": "Dang",
        "devbhoomi dwarka": "Devbhoomi Dwarka",
        "gandhinagar": "Gandhinagar",
        "gir somnath": "Gir Somnath",
        "jamnagar": "Jamnagar",
        "junagadh": "Junagadh",
        "kheda": "Kheda",
        "kutch": "Kutch",
        "mahisagar": "Mahisagar",
        "mehsana": "Mehsana",
        "morbi": "Morbi",
        "narmada": "Narmada",
        "navsari": "Navsari",
        "panchmahal": "Panchmahal",
        "patan": "Patan",
        "porbandar": "Porbandar",
        "rajkot": "Rajkot",
        "sabarkantha": "Sabarkantha",
        "surat": "Surat",
        "surendranagar": "Surendranagar",
        "tapi": "Tapi",
        "vadodara": "Vadodara",
        "valsad": "Valsad",

        # Common variations and alternate names
        "baroda": "Vadodara",
        "kachchh": "Kutch",
        "kachch": "Kutch",
        "dwarka": "Devbhoomi Dwarka",
        "somnath": "Gir Somnath",
        "palanpur": "Banaskantha",
        "godhra": "Panchmahal",
        "nadiad": "Kheda",
        "ankleshwar": "Bharuch",
        "vapi": "Valsad",
        "bhuj": "Kutch",
        "veraval": "Gir Somnath"
    }

    # Look for patterns like "weather in [city]" or "weather for [city]"
    if " in " in text:
        parts = text.split(" in ")
        if len(parts) > 1:
            location_part = parts[1].strip()
            # Handle multi-word cities
            location = location_part.split("?")[0].split(".")[0].strip()
            return city_corrections.get(location, location.title())

    if " for " in text:
        parts = text.split(" for ")
        if len(parts) > 1:
            location_part = parts[1].strip()
            location = location_part.split("?")[0].split(".")[0].strip()
            return city_corrections.get(location, location.title())

    # Look for direct city mentions
    for city_key, city_name in city_corrections.items():
        if city_key in text:
            return city_name

    # Look for capitalized words (likely city names)
    words = text.split()
    for word in words:
        clean_word = word.strip("?.,!").lower()
        if clean_word in city_corrections:
            return city_corrections[clean_word]
        elif word.istitle() and word not in ["Weather", "What", "How", "The", "Tell", "Me"]:
            return word.strip("?.,!")

    # Default fallback
    return None

def extract_reminder_parts(text):
    """
    Extracts the reminder message and time part from a natural language command.
    Example: "remind me to drink water in 10 minutes"
    Returns: (message, time_part)
    """
    match = re.search(r"remind me (to|for)?\s*(.+?)\s*(in|at|on|after)?\s*(.+)?", text, re.IGNORECASE)
    if match:
        message = match.group(2).strip()
        time_part = match.group(4).strip() if match.group(4) else ""
        return message, time_part
    return text, ""  # fallback