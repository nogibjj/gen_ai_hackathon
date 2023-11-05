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
def save_my_image(image_url, file_path='img/recent_img.png'):
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

# Patterns to match the necessary attributes
patterns = {
    "sex": r"\b(man|woman)\b",
    "age": r"(\b20ish\b|\b30ish\b)",
    "face_structure": r"\b(round|square)\b",
    "eyes": r"\b(big|small)\b",
    "nose_shape": r"\b(big|small)\b",
    "mouth_and_lips": r"\b(big|small)\b",
}

# Function to search the text for the attributes
def parse_attributes(text, patterns):
    attributes = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            attributes[key] = match.group(0)
        else:
            attributes[key] = "Unknown"
    return attributes

# Main Streamlit app
def app():
    st.set_page_config(layout="wide")
    st.title("Base Facial Features")

    with st.sidebar:
        st.header("Record your description")
        audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "ogg", "m4a"])
        if st.button("Transcribe Audio"):
            if audio_file is not None:
                # Mock-up of transcription using an imaginary method provided by OpenAI
                # You will need to replace this with actual transcription logic
                transcription_response = openai.Audio.transcribe(
                    model="whisper-1", 
                    file=audio_file
                )
                transcription = transcription_response["text"]
                st.write("Transcription:", transcription)  # Display the transcription
                
                attributes = parse_attributes(transcription, patterns)
                st.session_state['attributes'] = attributes  # Save the attributes in the session
            else:
                st.error("Please upload an audio file.")

    col_1, col_2 = st.columns(2)
    with col_1:
        with st.form("base_face_form"):
            prompt_sex = st.text_input('Sex', value=st.session_state['attributes'].get("sex", ""))
            prompt_age = st.text_input('Age', value=st.session_state['attributes'].get("age", ""))
            prompt_face_structure = st.text_input('Face Structure', value=st.session_state['attributes'].get("face_structure", ""))
            prompt_eyes = st.text_input('Eyes', value=st.session_state['attributes'].get("eyes", ""))
            prompt_nose = st.text_input('Nose Shape', value=st.session_state['attributes'].get("nose_shape", ""))
            prompt_mouth_lips = st.text_input('Mouth and Lips', value=st.session_state['attributes'].get("mouth_and_lips", ""))
            submitted = st.form_submit_button("Generate Sketch")

    if submitted:
        dalle_prompt = f"Create an image of a {prompt_sex} in their {prompt_age} with a {prompt_face_structure} face structure. They have {prompt_eyes} eyes, a {prompt_nose} nose, and {prompt_mouth_lips} mouth and lips."
        with col_2:
            st.text("The Prompt:")
            st.write(dalle_prompt)
            st.image(generate_image(dalle_prompt), width=500)

if __name__ == "__main__":
    app()
