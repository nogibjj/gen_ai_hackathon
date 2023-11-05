from dotenv import load_dotenv
import openai
import os
import streamlit as st

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Base Facial Features")

st.markdown(
    """
    This part of sketching is to generate a base picture of the face. 
    This will be used to generate the rest of the face.
    """
)

st.markdown(
    """
    ## Instructions
    1. Type in the text box to generate a base face.
    2. Click the button to generate a base face.
    3. Click the button again to generate a new base face.
    """
)

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n = 1,
        size = '512x512',
    )
    image_url = response['data'][0]['url']
    return image_url

def app():
    col_1, col_2 = st.columns(2)
    
    with col_1:
        prompt_sex = st.text_input('Sex', placeholder='man, woman, .etc')
        prompt_age = st.text_input('Age', placeholder='age approximations, 20ish, 30ish, .etc')
        prompt_face_structure = st.text_input('Face Structure', placeholder='round, square, .etc')
        prompt_eyes = st.text_input('Eyes', placeholder='big, small, .etc')
        prompt_nose = st.text_input('Nose Shape', placeholder='big, small, .etc')
        prompt_mouth_lips = st.text_input('Mouth and Lips', placeholder='big, small, .etc')