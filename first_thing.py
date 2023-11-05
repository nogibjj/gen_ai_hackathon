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
st.sidebar.write("Fill out the following form to generate a police sketch of a suspect.")
st.title("Base Facial Features")

st.sidebar.markdown(
    """
    ## Instructions
    1. Type in the text box to generate a base face.
    2. Click the button to generate a base face.
    3. Move to the next page by clicking the sidebar.
    """
)

# Function to save the image locally in the given path
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

# Main Streamlit app
def app():
    col_1, col_2 = st.columns(2)

    with col_1:
        st.header("Prompt")
        st.write("Fill out the following form to generate a police sketch of a suspect.")
        col_x, col_y = st.columns(2)
        with col_x:
            prompt_sex = st.text_input('Sex', placeholder='man, woman, etc.')
            prompt_age = st.text_input('Age', placeholder='age approximations, 20s, 30s, etc.')
            prompt_face_structure = st.text_input('Face Structure', placeholder='round, square, etc.')
        with col_y:
            prompt_eyes = st.text_input('Eyes', placeholder='big, small, etc.')
            prompt_nose = st.text_input('Nose Shape', placeholder='big, small, etc.')
            prompt_mouth_lips = st.text_input('Mouth and Lips', placeholder='big, small, etc.')

        prompt_additional = st.text_area("Additional Features", height=200, placeholder="Describe any additional features of the suspect.")

    if st.button("Generate Sketch"):
        descriptive_paragraph = (
            f"Create a front-facing sketch with the following attributes: "
            f"A {prompt_face_structure} face structure, {prompt_eyes} eyes, "
            f"{prompt_nose} nose, and {prompt_mouth_lips} mouth and lips for a "
            f"{prompt_age}, {prompt_sex}. Additional features: {prompt_additional}."
        )

        st.text("Generated Prompt:")
        st.write(descriptive_paragraph)

        try:
            image_url = generate_image(descriptive_paragraph)
            with col_2:
                st.header("Sketch")
                st.image(image_url, width=500)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    app()
