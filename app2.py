from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests

# Set up OpenAI API credentials
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
audio_file= open("/workspaces/gen_ai_hackathon/New Recording 55.m4a", "rb") ##audio file input 
transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="text")

# Define a function to generate a DALL-E prompt from the transcript using GPT-3.5
def create_chat_for_dalle_prompt(transcription_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant who can create concise descriptions for sketches."},
        {"role": "user", "content": f"Create a short DALL-E prompt for a sketch based on these features and keep it under 200 characters. Remember, no fluff or unnecessary details, just the essentials for forensic purposes. Input: {transcript}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    # The last message from the assistant will contain the DALL-E prompt
    dalle_prompt = response['choices'][0]['message']['content']
    return dalle_prompt.strip()

# Generate the DALL-E prompt
dalle_prompt = create_chat_for_dalle_prompt(transcript)

# Print the DALL-E prompt
print("DALL-E Prompt:", dalle_prompt)