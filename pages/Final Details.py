from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests
from PIL import Image
from source.mask_image import masker

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Final Details",
    # give me all the possible icons
    page_icon="🎭",
    layout="wide"
    )
st.sidebar.header("Final Details")
st.sidebar.write("Fill out the following form to generate a police sketch of a suspect.")
st.title("More Facial Features")

st.sidebar.markdown(
    """
    ## Instructions
    1. Type in the text box to update all the incorrect details of the face.
    2. Click the button to generate the face.
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

def update_image(image, mask, prompt):
    response = openai.Image.create_edit(
    image=open(image, "rb"),
    mask=open(mask, "rb"),
    prompt=prompt,
    n=1,
    size="512x512"
    )
    image_url = response['data'][0]['url']
    save_my_image(image_url)
    return image_url

def change_mask_format(mask_path):
    mask = Image.open(mask_path)
    mask = mask.convert('RGBA')
    mask = mask.convert('LA')
    mask = mask.convert('L')
    mask.save(mask_path)
    return None

def app():
    col_1, col_2 = st.columns(2)
    
    with col_1:

        col_x, col_y = st.columns(2)
        with col_x:
            prompt_eyebrows = st.text_input('Eyebrows', placeholder='thickness, length .etc')
            prompt_ears = st.text_input('Ears', placeholder='wide, small, .etc')
        with col_y:
            prompt_mouth = st.text_input('Mouth', placeholder='wide, narrow, .etc')
            prompt_accessories = st.text_input('Accessories', placeholder='glasses, earrings, .etc')
        prompt_essay = st.text_area('Additional Details', height=100, max_chars=200, help='Add any additional details here.')
    with col_2:
        image = Image.open('img/img.png')

        st.image(image, caption="Image from previous iteration", use_column_width=True)

    if st.button("Generate Sketch"):
        dalle_prompt = f"""
                Update the eyebrows to be {prompt_eyebrows} and with {prompt_ears} ears.
                With a {prompt_mouth} mouth, and {prompt_accessories} visible. Also update
                some additional details: {prompt_essay}
            """
        
        with col_2:
            st.text("")
            st.text("The description is:")
            st.write(dalle_prompt)
            # eric call the mask function here, and make sure that you save the mask.png file in the img folder as mask.png
            masker("img/img.png", "img/mask.png")
            change_mask_format("mask.png")
            st.image(update_image("img/img.png", "mask.png", dalle_prompt))

if __name__ == "__main__":
    app()