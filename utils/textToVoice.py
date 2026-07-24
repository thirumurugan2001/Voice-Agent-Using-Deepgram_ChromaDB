from deepgram import DeepgramClient
from dotenv import load_dotenv
import os
import uuid
load_dotenv()

# Function to convert text to voice and save audio
def textToVoice(text: str) -> str:
    try:
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
        audio_stream = deepgram.speak.v1.audio.generate(text=text,model="aura-2-thalia-en",)
        audio_bytes = b"".join(audio_stream)
        current_dir = os.getcwd()
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(audio_dir, filename)
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_bytes)
        print(f"Audio saved successfully: {file_path}")
        return file_path

    except Exception as e:
        print(f"Error in textToVoice function - "f"textToVoice.py file: {str(e)}")
        return None