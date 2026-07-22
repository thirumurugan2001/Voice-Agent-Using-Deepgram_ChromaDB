from deepgram import DeepgramClient

DEEPGRAM_API_KEY = "b282a677fea410cbc82dc908955059e0aa0defd3"

AUDIO_FILE_PATH = r"C:\Users\intel\OneDrive\Desktop\Studies\Voice-Agent-Using-Deepgram\audio.mp3"

def SpeechToText(file_path):
    try:
        client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
        with open(file_path, "rb") as audio:
            audio_data = audio.read()
        response = client.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-3",
            language="en",
            smart_format=True,
        )
        transcript = response.results.channels[0].alternatives[0].transcript
        return transcript
    except Exception as e:
        print(f"Exception: {e}")
        return None

text = SpeechToText(AUDIO_FILE_PATH)