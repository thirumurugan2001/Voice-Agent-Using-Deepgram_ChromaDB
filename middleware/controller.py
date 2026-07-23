from utils.speechToText import SpeechToText
from utils.textToVoice import textToVoice
from utils.base64ToAudio import base64ToAudio
from utils.ConnectChatBot import ConnectChatBot
from utils.rag import similaritySearch

# Controller function for voice agent
def voiceAgentController(base64,extension):
    try:
        print(f"Start Converting base64 to audio file....")
        # Check if base64 is empty 
        if base64 == "":
            return {
                "message":"Invalid data !",
                "statusCode":400,
                "Status":False
            }
        
        print("Start Converting base64 to audio file.....")
        # Convert base64 to audio file
        fileurl= base64ToAudio(base64,extension)
        if fileurl is None:
            return {
                "message":"Failed to extract audio !",
                "statusCode":400,
                "Status":False
            }

        print(f"Start Transcribing audio to text.....")
        # Transcribe audio to text
        result = SpeechToText(fileurl)
        if result is None:
            return {
                "message":"Failed to transcribe audio !",
                "statusCode":400,
                "Status":False
            }

        print(f"starting similarity search for knowledge base data....")
        # Perform similarity search to get knowledge base data
        knowledgeBaseData = similaritySearch(result)
        if knowledgeBaseData is None:
            return {
                "message":"Failed to get knowledge base data !",
                "statusCode":400,
                "Status":False
            }

        print(f"Starting to connect to chatbot and get response....")
        # Connect to chatbot and get response
        chatbotResponse = ConnectChatBot(result,knowledgeBaseData)
        if chatbotResponse is None:
            return {
                "message":"Failed to get response from chatbot !",
                "statusCode":400,
                "Status":False
            }

        print(f"Starting to convert chatbot response to speech.....")    
        # Convert chatbot response to speech
        text_to_speech_response = textToVoice(chatbotResponse)
        if text_to_speech_response is None:
            return {
                "message":"Failed to convert text to speech !",
                "statusCode":400,
                "Status":False
            }

        print(f"Successfully converted text to speech and returning the response......")
        # Return the final response with audio data
        return {
                "message":"Successfully converted text to speech !",
                "statusCode":200,
                "Status":True,
                "data":text_to_speech_response
            }

    except Exception as e:
        print(f"Error in voiceAgentController function - controller.py file: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "message":"Error occurred while processing the request.",
                "Status":False
            }