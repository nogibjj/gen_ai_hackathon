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
            prompt_face_shape = st.text_input("Face Shape", placeholder="oval, round, square, heart, etc.")
            prompt_chin_shape = st.text_input("Chin Shape", placeholder="pointed, rounded, double chin, cleft, etc.")
            prompt_jaw_line = st.text_input("Jaw Line", placeholder="strong, rounded, etc.")
            prompt_skin_complexion = st.text_input("Skin Complexion", placeholder="light, medium, dark, freckles, scars, etc.")
            prompt_skin_texture = st.text_input("Skin Texture", placeholder="smooth, wrinkled, etc.")
            prompt_skin_notable_features = st.text_input("Skin Notable Features", placeholder="tattoos, moles, scars")
            prompt_mouth_size = st.text_input("Mouth Size", placeholder="wide, narrow")
            prompt_lip_shape = st.text_input("Lip Shape", placeholder="full, thin, cupid's bow, etc.")
            prompt_ears_size = st.text_input("Ears Size", placeholder="large, small, etc.")
            prompt_ears_shape = st.text_input("Ears Shape", placeholder="attached lobes, detached lobes, etc.")
            prompt_ears_notable_features = st.text_input("Ears Notable Features", placeholder="piercings, etc.")
        with col_y:
            prompt_eyes_size = st.text_input("Eyes Size", placeholder="large, small")
            prompt_eyes_shape = st.text_input("Eyes Shape", placeholder="almond, round, deep-set, hooded, etc.")
            prompt_eyes_color = st.text_input("Eyes Color", placeholder="black, blue, .etc")
            prompt_eyebrows_type = st.text_input("Eyebrows Type", placeholder="thick, thin, arched, straight, color")
            prompt_eyelashes_type = st.text_input("Eyelashes Type", placeholder="long, short, thick, etc.")
            prompt_nose_size = st.text_input("Nose Size", placeholder="large, small, wide, narrow")
            prompt_nose_shape = st.text_input("Nose Shape", placeholder="straight, hooked, upturned, etc.")
            prompt_hair_length = st.text_input("Hair Length", placeholder="short, medium, long, bald")
            prompt_hair_style = st.text_input("Hair Style", placeholder="straight, curly, wavy, etc.")
            prompt_hair_color = st.text_input("Hair Color", placeholder="black, brown, blonde, red, etc.")
            prompt_hairline = st.text_input("Hairline", placeholder="receding, widow's peak, etc.")
        prompt_additional = st.text_area("Additional Features", height=200, placeholder="Describe any additional features of the suspect's face.")
    
    # Generate text completion
    if st.button("Generate sketch"):        
        # feed the dictionary into the prompt and ask the api to create prompt to make a sketch from the new_dict
        prompt = f"""
        Create a prompt for DALL-E to generate a front-facing human sketch of a suspect based on the following description:
        Face Shape: {prompt_face_shape}
        Chin Shape: {prompt_chin_shape}
        Jaw Line: {prompt_jaw_line}
        Skin Complexion: {prompt_skin_complexion}
        Skin Texture: {prompt_skin_texture}
        Skin Notable Features: {prompt_skin_notable_features}
        Mouth Size: {prompt_mouth_size}
        Lip Shape: {prompt_lip_shape}
        Ears Size: {prompt_ears_size}
        Ears Shape: {prompt_ears_shape}
        Ears Notable Features: {prompt_ears_notable_features}
        Eyes Size: {prompt_eyes_size}
        Eyes Shape: {prompt_eyes_shape}
        Eyes Color: {prompt_eyes_color}
        Eyebrows Type: {prompt_eyebrows_type}
        Eyelashes Type: {prompt_eyelashes_type}
        Nose Size: {prompt_nose_size}
        Nose Shape: {prompt_nose_shape}
        Hair Length: {prompt_hair_length}
        Hair Style: {prompt_hair_style}
        Hair Color: {prompt_hair_color}
        Hairline: {prompt_hairline}
        Also add the following additional features: {prompt_additional}
        """
        completion = generate_completion(prompt)
        with col_2:
            st.header("Sketch")
            st.text(completion)
            st.image(generate_image(completion), width=500)

# Run Streamlit app
if __name__ == "__main__":
    app()

    