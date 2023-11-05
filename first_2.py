from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests

# Set up OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Base Features", page_icon="🎭", layout="wide")
st.sidebar.header("Base Features")
st.sidebar.write("Upload an audio file to generate a police sketch of a suspect.")
st.title("Base Facial Features")

# Function to save the image locally
def save_my_image(image_url, file_path='/home/codespace/recent_img.png'):
    data = requests.get(image_url).content
    with open(file_path, 'wb') as f:
        f.write(data)

# Function to generate an image from a text prompt
def generate_image(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size='512x512')
    image_url = response['data'][0]['url']
    save_my_image(image_url)
    return image_url

# Function to create a DALL-E prompt from the transcription
def create_dall_e_prompt_from_transcription(transcription_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant who can create concise descriptions for sketches."},
        {"role": "user", "content": f"Create a short DALL-E prompt for a sketch based on these features and keep it under 200 characters. Remember, no fluff or unnecessary details, just the essentials for forensic purposes. Input: {transcription_text}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    dalle_prompt = response['choices'][0]['message']['content']
    return dalle_prompt.strip()

# Main Streamlit app
def app():
    with st.sidebar:
        audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg", "m4a"])
        if audio_file and st.button("Transcribe Audio"):
            # Use OpenAI's Whisper model to transcribe the audio file
            transcription_response = openai.Audio.transcribe(model="whisper-1", file=audio_file)
            transcription = transcription_response['choices'][0]['text']
            st.text_area("Transcription Result", transcription, height=200)

            # Generate a DALL-E prompt from the transcription
            dalle_prompt = create_dall_e_prompt_from_transcription(transcription)
            st.write("DALL-E Prompt:", dalle_prompt)

            # Generate and display the image using DALL-E
            image_url = generate_image(dalle_prompt)
            if image_url:
                st.image(image_url, width=500)

if __name__ == "__main__":
    app()
