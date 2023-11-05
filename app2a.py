from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests

# Set up OpenAI API credentials
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
audio_file= open("/workspaces/gen_ai_hackathon/New Recording 55.m4a", "rb") ##audio file input 
transcript = openai.Audio.transcribe("whisper-1", audio_file)

print(transcript)