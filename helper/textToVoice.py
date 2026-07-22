from deepgram import DeepgramClient

DEEPGRAM_API_KEY = "b282a677fea410cbc82dc908955059e0aa0defd3"

def textToVoice(text):
    try:
        FILENAME = "audio.mp3"
        deepgram = DeepgramClient(api_key=DEEPGRAM_API_KEY)

        with open(FILENAME, "wb") as f:
            for chunk in deepgram.speak.v1.audio.generate(
                text=text,
                model="aura-2-thalia-en",
            ):
                f.write(chunk)

        print(f"Wrote to {FILENAME}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    textToVoice("Your lab results show elevated cholesterol levels of 240 mg/dL; I recommend starting Atorvastatin 10 mg daily and scheduling a follow-up in eight weeks to reassess.")