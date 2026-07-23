from deepgram import DeepgramClient
import os
from dotenv import load_dotenv
load_dotenv()


# Function to convert speech to text using Deepgram API
def SpeechToText(file_path):
    try:
        with open(file_path, "rb") as audio:
            audio_data = audio.read()

        client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
        response = client.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-3",
            language="en",
            smart_format=True,
        )
        transcript = response.results.channels[0].alternatives[0].transcript
        print("Audio Transcript : ", transcript)
        return transcript
    except Exception as e:
        print(f"Error in SpeechToText function - speechToText.py file: {str(e)}")
        return None
