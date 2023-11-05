from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests
import re

# Set up OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to save the image locally
def save_my_image(image_url, file_path='/home/codespace/recent_img.png'):
    data = requests.get(image_url).content
    with open(file_path, 'wb') as f:
        f.write(data)

# Function to generate an image from a text prompt
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size='512x512',
    )
    image_url = response['data'][0]['url']
    save_my_image(image_url)
    return image_url

# Define a function to generate a DALL-E prompt from the transcript using GPT-3.5
def create_chat_for_dalle_prompt(transcription_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant who can create concise descriptions for sketches."},
        {"role": "user", "content": f"Create a short DALL-E prompt for a sketch based on these features and keep it under 200 characters. Remember, no fluff or unnecessary details, just the essentials for forensic purposes. Input: {transcription_text}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    # The last message from the assistant will contain the DALL-E prompt
    dalle_prompt = response['choices'][0]['message']['content']
    return dalle_prompt.strip()

# Patterns to match the necessary attributes
patterns = {
    "sex": r"\b(man|woman)\b",
    "age": r"(\b20ish\b|\b30ish\b)",
    "face_structure": r"\b(round|square)\b",
    "eyes": r"\b(big|small)\b",
    "nose_shape": r"\b(big|small)\b",
    "mouth_and_lips": r"\b(big|small)\b",
}

# Main Streamlit app
def app():
    st.set_page_config(layout="wide")
    st.title("Base Facial Features")

    submitted = False  # Initialize submitted to False here

    with st.sidebar:
        st.header("Record your description")
        audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "ogg", "m4a"])
        if st.button("Transcribe Audio"):
            if audio_file is not None:
                # Transcription using Whisper model
                transcription_response = openai.Audio.transcribe(
                    model="whisper-1", 
                    file=audio_file
                )
                transcription = transcription_response["text"]
                st.write("Transcription:", transcription)  # Display the transcription

                # Generate DALL-E prompt using the transcribed text
                dalle_prompt = create_chat_for_dalle_prompt(transcription)
                st.session_state['dalle_prompt'] = dalle_prompt  # Save the DALL-E prompt in the session
            else:
                st.error("Please upload an audio file.")

    col_1, col_2 = st.columns(2)
    with col_1:
        if 'dalle_prompt' in st.session_state:
            st.text("DALL-E Prompt:")
            st.write(st.session_state['dalle_prompt'])
            submitted = st.button("Generate Sketch")

    if submitted:
        with col_2:
            st.image(generate_image(st.session_state['dalle_prompt']), width=500)

if __name__ == "__main__":
    app()