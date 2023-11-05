from dotenv import load_dotenv
import openai
import os
import streamlit as st


# Set up OpenAI API credentials
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define function to generate text completions
def generate_completion(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
    )
    return response.choices[0].text

# Define a function to generate an image from a text prompt
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n = 1,
        size = '512x512',
    )
    image_url = response['data'][0]['url']
    return image_url

# Define Streamlit app
def app():
    st.set_page_config(layout="wide")
    st.title("Automated Police Sketch Artist")

    col_1, col_2 = st.columns(2)

    with col_1:
        st.header("Prompt")
        st.write("Fill out the following form to generate a police sketch of a suspect.")
    # Get user input
        col_x, col_y = st.columns(2)
        
        with col_x:
            prompt_sex = st.text_input("Sex", placeholder="male, female")
            prompt_age = st.text_input("Age", placeholder="number of approximations like 20s, 30s, etc.")
            prompt_face_shape = st.text_input("Face Shape", placeholder="oval, round, square, etc.")
            prompt_body_type = st.text_input("Body Type", placeholder="slender, muscular, etc.")
            prompt_jaw_line = st.text_input("Jaw Line", placeholder="strong, rounded, etc.")
            prompt_skin_complexion = st.text_input("Skin Complexion", placeholder="light, medium, dark, freckles, scars, etc.")
            prompt_expression = st.text_input("Expression", placeholder="happy, sad, angry, etc.")
            prompt_chin_shape = st.text_input("Chin Shape", placeholder="pointed, square, etc.")
            prompt_demeanor = st.text_input("Demeanor", placeholder="commanding, defiant, etc.")
        with col_y:
            prompt_eyes_size = st.text_input("Eyes Size", placeholder="large, small")
            prompt_eyebrows_type = st.text_input("Eyebrows Type", placeholder="thick, thin, arched, straight, color")
            prompt_nose_size = st.text_input("Nose Size", placeholder="large, small, wide, narrow")
            prompt_nose_shape = st.text_input("Nose Shape", placeholder="straight, hooked, upturned, etc.")
            prompt_moustache = st.text_input("Moustache", placeholder="thick, thin, etc.")
            prompt_beard = st.text_input("Beard", placeholder="thick, thin, etc.")
            prompt_clothes = st.text_input("Clothes", placeholder="tank-top, suit, etc.")
            prompt_lip_shape = st.text_input("Lip Shape", placeholder="full, thin, cupid's bow, etc.")
            prompt_hair = st.text_input("Hair", placeholder="color, length, style, etc.")
        prompt_additional = st.text_area("Additional Features", height=200, placeholder="Describe any additional features of the suspect's face.")
    
    # Generate text completion
    if st.button("Generate sketch"):                
        text1 = f"""
        Create an image of a {prompt_body_type}, powerfully built {prompt_sex} in 
        his {prompt_age} age with a {prompt_demeanor} demeanor. 
        He has an {prompt_face_shape} face with a {prompt_expression} expression,
        a {prompt_chin_shape} chin adorned with a {prompt_moustache} mustache, and a 
        {prompt_jaw_line} jawline framed by a {prompt_beard} beard.
        His hair is {prompt_hair}, revealing a {prompt_skin_complexion} complexion.
        His {prompt_eyes_size} eyes convey a protective nature, 
        sitting beneath {prompt_eyebrows_type} eyebrows. The nose is {prompt_nose_size} and 
        {prompt_nose_shape}, and the lips are {prompt_lip_shape}, contributing to his 
        thoughtful appearance. A notable feature is a {prompt_additional}. 
        He is wearing a {prompt_clothes}.
        """

        with col_2:
            st.header("Sketch")
            # st.code(completion)
            st.image(generate_image(text1), width=500)

# Run Streamlit app
if __name__ == "__main__":
    app()

    