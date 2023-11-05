from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide")
st.title("Base Facial Features")

st.markdown(
    """
    This part will update the details from our base picture of the face. 
    This will be used to generate the rest of the face.
    """
)

st.markdown(
    """
    ## Instructions
    1. Type in the text box to generate a base face.
    2. Click the button to generate a base face.
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

# create a function to use OpenCV to create a mask of the image in img directory
def create_mask(image):
    # import OpenCV
    import cv2
    # read the image
    img = cv2.imread(image)
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # threshold the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # apply morphology to clean up small spots
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    # invert the close image
    result = 255 - close
    # save the result
    cv2.imwrite('img/mask.png', result)
    return None

def app():
    col_1, col_2 = st.columns(2)
    
    with col_1:

        col_x, col_y = st.columns(2)
        with col_x:
            prompt_hair = st.text_input('Hair', placeholder='color, length, .etc')
            prompt_facial_hair = st.text_input('Facial Hair', placeholder='beard, mustache, .etc')
            prompt_complexion = st.text_input('Complexion', placeholder='skin tone, .etc')
        with col_y:
            prompt_demeanor = st.text_input('Demeanor', placeholder='intimidating, friendly, .etc')
            prompt_expression = st.text_input('Expression', placeholder='smiling, frowning, .etc')
            prompt_distinguishing_features = st.text_input('Distinguishing Features', placeholder='tattoos, scars, .etc')

    if st.button("Generate Sketch"):
        dalle_prompt = f"""
                The individual has a {prompt_hair} hair style, and have {prompt_facial_hair} visible.
                With a {prompt_complexion} complexion, and {prompt_demeanor} demeanor.
                The expression they showed is {prompt_expression}, and they have {prompt_distinguishing_features}.
            """
        
        with col_2:
            st.text("The prompt is:")
            st.write(dalle_prompt)
            st.image(update_image("img/img.png","img/mask.png",dalle_prompt))

if __name__ == "__main__":
    app()