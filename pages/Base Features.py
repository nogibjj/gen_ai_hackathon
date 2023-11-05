from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Base Features",
    page_icon="🎭",
    layout="wide"
    )
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
    
def save_my_image(image_url, file_path = 'img/recent_img.png'):
    # Use requests to download the image
    # Write the image to a file in binary mode
    # Hint: You want to use a 'with' statement
    data = requests.get(image_url).content
    f = open('img/img.png','wb')
    f.write(data)
    f.close()
    return None

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n = 1,
        size = '512x512',
    )
    image_url = response['data'][0]['url']
    save_my_image(image_url)
    return image_url

def app():
    col_1, col_2 = st.columns(2)
    
    with col_1:

        col_x, col_y = st.columns(2)
        with col_x:
            prompt_sex = st.text_input('Sex', placeholder='man, woman, .etc')
            prompt_age = st.text_input('Age', placeholder='age approximations, 20ish, 30ish, .etc')
            prompt_face_structure = st.text_input('Face Structure', placeholder='round, square, .etc')
        with col_y:
            prompt_eyes = st.text_input('Eyes', placeholder='big, small, .etc')
            prompt_nose = st.text_input('Nose Shape', placeholder='big, small, .etc')
            prompt_mouth_lips = st.text_input('Mouth and Lips', placeholder='big, small, .etc')

    if st.button("Generate Sketch"):
        if prompt_sex == "man":
            dalle_prompt = f"""
                Create an image of a {prompt_sex} in his {prompt_age} with a 
                {prompt_face_structure} face structure. He has {prompt_eyes} 
                eyes, a {prompt_nose} nose, and {prompt_mouth_lips} mouth and 
                lips.
            """
        elif prompt_sex == "woman":
            dalle_prompt = f"""
                Create an image of a {prompt_sex} in her {prompt_age} with a 
                {prompt_face_structure} face structure. She has {prompt_eyes} 
                eyes, a {prompt_nose} nose, and {prompt_mouth_lips} mouth and 
                lips.
            """
        else:
            dalle_prompt = f"""
                Create an image of a {prompt_sex} in their {prompt_age} with a 
                {prompt_face_structure} face structure. They have {prompt_eyes} 
                eyes, a {prompt_nose} nose, and {prompt_mouth_lips} mouth and 
                lips.
            """
        
        with col_2:
            st.text("The prompt is:")
            st.write(dalle_prompt)
            st.image(generate_image(dalle_prompt))

if __name__ == "__main__":
    app()