import openai
import os
import streamlit as st

# Set up OpenAI API credentials
openai.api_key = os.getenv("YOUR_API_KEY")

# Define function to generate text completions
def generate_completion(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

# Define Streamlit app
def app():
    st.title("Text Completion Generator")

    # Get user input
    prompt = st.text_input("Enter some text:")

    # Generate text completion
    if prompt:
        completion = generate_completion(prompt)
        st.write("Completion:")
        st.write(completion)

# Run Streamlit app
if __name__ == "__main__":
    app()

    