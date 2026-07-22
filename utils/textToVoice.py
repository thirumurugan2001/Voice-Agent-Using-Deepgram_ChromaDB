from deepgram import DeepgramClient
from dotenv import load_dotenv
import os
load_dotenv()

def textToVoice(text: str) -> bytes:
    try:
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
        audio_stream = deepgram.speak.v1.audio.generate(
            text=text,
            model="aura-2-thalia-en",
        )
        audio_bytes = b"".join(audio_stream)
        return audio_bytes
    except Exception as e:
        print(f"Exception: {e}")
        raise
