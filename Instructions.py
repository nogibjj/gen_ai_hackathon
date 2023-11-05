from dotenv import load_dotenv
import openai
import os
import streamlit as st
import requests

# Set up OpenAI API credentials
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Instructions",
    page_icon="🧊",
    layout="wide",
    )
st.sidebar.success("Please proceed once you've read the instructions.")

# Define Streamlit app
def app():
    st.title("Automated Police Sketch Artist")

    st.markdown(
        """
        ## Instructions
        1. Please type in each space the impression you have on the fugitive.
        2. The drawing will show up on the right side of website.
        3. Then click on sidebar to go to the next page.
        4. You will see a similar page as the first one, but more details feature that will also needs to be filled in.
        5. The second drawing will show up on the right side.
        6. Click on sidebar to go to the next page.
        7. Now you will see a big bracket with several last details that needs to be filled up.
        8. After filling this page out, you will get your last pic.
        """
    )

# Run Streamlit app
if __name__ == "__main__":
    app()

    
