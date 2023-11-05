from dotenv import load_dotenv
import openai
import os
import streamlit as st

# Set up OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Transcribe the audio file
def transcribe_audio(uploaded_file):
    # Assuming OpenAI has a method to transcribe directly from file data
    transcript_response = openai.Audio.transcribe(
        model="whisper-1",
        file=uploaded_file.getvalue()
    )
    return transcript_response["data"]["text"]

# Main application logic
def app():
    st.title("AI Sketch Assistant")

    # Allow user to upload an audio file
    uploaded_audio = st.file_uploader("Upload an audio file", type=["m4a", "mp3", "wav", "ogg"])

    if st.button("Generate Sketch"):
        if uploaded_audio is not None:
            # Transcribe the audio file
            transcription = transcribe_audio(uploaded_audio)

            # Generate a prompt from transcription using GPT-3.5 model
            gpt_prompt = (
                "Take the following audio transcription and look for potential answers to fields: "
                "descriptions of sex, eyes, age, nose shape, face structure, and mouth and lips. "
                "Then create a DALL-E prompt to get a sketch based on these descriptions:\n\n"
                f"{transcription}"
            )
            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt=gpt_prompt,
                max_tokens=150
            )
            dall_e_prompt = response.choices[0].text.strip()

            # Generate and display the image from DALL-E prompt
            image_response = openai.Image.create(prompt=dall_e_prompt, n=1, size='512x512')
            image_url = image_response['data'][0]['url']
            st.image(image_url, caption="Generated Sketch")

            # Debug: Print transcription and prompts
            st.write("Transcription:", transcription)
            st.write("DALL-E Prompt:", dall_e_prompt)

if __name__ == "__main__":
    app()
