# This code snippet demonstrates how to use the Google GenAI client library
# to generate content using the Gemini model. It includes examples of generating text
# from google import genai

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)

from google import genai
from google.genai import types
# Set the API key for Google GenAI
import api

client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="tomorows weather report in khanvel,dadra and nagar haveli",
#     config=types.GenerateContentConfig(
#         thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
#     ),
# )
# print(response.text)

def get_response(prompt):
    system_instruction = (
        "You are ARIA, an intelligent and friendly AI voice assistant. "
        "Always respond in a helpful, clear, and conversational manner. "
        "Use a polite and positive tone. "
        "If the user asks for information, provide concise and accurate answers. "
        "If the user asks for reminders, emails, or actions, confirm and guide them as needed. "
        "If you don’t know something, admit it gracefully and offer to help in another way. "
        "Keep responses short and easy to understand, unless the user asks for more detail. "
        "Use natural, human-like language and avoid sounding robotic. "
        "If the user greets you, greet them back warmly. "
        "If the user says goodbye, wish them well.\n\n"
    )
    full_prompt = system_instruction + prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=4)
        )
    )
    return response.text.strip()