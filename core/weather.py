# core/weather.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    if not API_KEY:"""
Weather module for ARIA Voice Assistant
Fetches real-time weather data using OpenWeatherMap API

Created by: Your Name
Last updated: 2024
"""

import requests
import os
from dotenv import load_dotenv

# Load configuration from environment file
load_dotenv()

# API configuration
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    """
    Fetch current weather information for a given city

    Args:
        city_name (str): Name of the city to get weather for

    Returns:
        str: Formatted weather information or error message
    """
    # Check if API key is configured
    if not WEATHER_API_KEY:
        return "Weather service is not configured. Please add your OpenWeatherMap API key."

    # Clean and format city name
    city_name = city_name.strip().title()

    # Try different city name formats to improve success rate
    city_formats = [
        city_name,
        city_name.replace(" ", ""),  # "New York" -> "NewYork"
        city_name.replace("-", " "), # "Pimpri-Chinchwad" -> "Pimpri Chinchwad"
        city_name.split(",")[0].strip() if "," in city_name else city_name  # Remove state/country
    ]

    # Try each format until one works
    for city_format in city_formats:
        request_params = {
            "q": city_format,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        try:
            # Make API request
            api_response = requests.get(WEATHER_BASE_URL, params=request_params)
            weather_data = api_response.json()

            # Check if request was successful
            if weather_data["cod"] == 200:
                # Extract weather information
                temperature = weather_data["main"]["temp"]
                weather_desc = weather_data["weather"][0]["description"]
                humidity_level = weather_data["main"]["humidity"]
                wind_speed = weather_data["wind"]["speed"]
                city_actual = weather_data["name"]
                country_code = weather_data["sys"]["country"]

                # Format response message
                weather_report = (
                    f"Current weather in {city_actual}, {country_code}: "
                    f"{temperature}°C with {weather_desc}. "
                    f"Humidity: {humidity_level}%, Wind: {wind_speed} m/s."
                )
                return weather_report

        except requests.RequestException:
            # Network error, try next format
            continue
        except KeyError:
            # Invalid response format, try next format
            continue
        except Exception:
            # Other error, try next format
            continue

    # If all formats failed, return helpful error message
    error_message = (
        f"Could not find weather data for '{city_name}'. "
        f"Please check the spelling or try a nearby major city."
    )
    return error_message

def get_weather_demo(city_name):
    """Demo version that works without API key for testing"""
    import random

    # Demo weather data for testing
    demo_data = {
        "london": {"temp": 15, "desc": "cloudy", "humidity": 65, "wind": 3.2},
        "new york": {"temp": 22, "desc": "sunny", "humidity": 45, "wind": 2.1},
        "tokyo": {"temp": 18, "desc": "partly cloudy", "humidity": 70, "wind": 1.8},
        "paris": {"temp": 16, "desc": "light rain", "humidity": 80, "wind": 2.5},
        "berlin": {"temp": 12, "desc": "overcast", "humidity": 75, "wind": 4.1}
    }

    city_lower = city_name.lower()

    if city_lower in demo_data:
        data = demo_data[city_lower]
        return (
            f"[DEMO] The current temperature in {city_name} is {data['temp']}°C with {data['desc']}. "
            f"Humidity is at {data['humidity']}% and wind speed is {data['wind']} meters per second."
        )
    else:
        # Generate random demo data for unknown cities
        temp = random.randint(5, 30)
        descriptions = ["sunny", "cloudy", "partly cloudy", "light rain", "overcast"]
        desc = random.choice(descriptions)
        humidity = random.randint(40, 90)
        wind = round(random.uniform(1.0, 5.0), 1)

        return (
            f"[DEMO] The current temperature in {city_name} is {temp}°C with {desc}. "
            f"Humidity is at {humidity}% and wind speed is {wind} meters per second."
        )

        return "Weather API key is missing."

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            return f"Sorry, I couldn't find weather info for {city_name}."

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"The current temperature in {city_name} is {temp}°C with {description}. "
            f"Humidity is at {humidity}% and wind speed is {wind_speed} meters per second."
        )

    except Exception as e:
        return f"An error occurred while fetching weather data: {e}"
