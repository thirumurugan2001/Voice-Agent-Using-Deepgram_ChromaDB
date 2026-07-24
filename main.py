from fastapi import FastAPI
from middleware.middleware import setup_cors
from middleware.controller import voiceAgentController
from schema.voiceAgent import voiceAgent
app = FastAPI()
setup_cors(app)

# API endpoint for voice agent
@app.post("/chatbot/voice/")
async def rag(item: voiceAgent):
    try:
        response = voiceAgentController(item.base64,item.extension)
        if response.get("Status") == False:
            return {
                "message":response.get("message"),
                "statusCode":response.get("statusCode"),
                "Status":False,
            }
        return {
            "message":response.get("message"),
            "statusCode":response.get("statusCode"),
            "Status":True,
            "data":[{
                "file_path":response.get("file_Path")
            }]
        }
    except Exception as e:
        print(f"Error in rag function - main.py file: {str(e)}")
        return {
            "message":"An error occurred while processing the request.",
            "statusCode":500,
            "Status":False
        }
    
    
# Run Command: python -m uvicorn main:app --reload
