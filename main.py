from fastapi import FastAPI
from middleware.middleware import setup_cors
from middleware.controller import voiceAgentController
app = FastAPI()
setup_cors(app)
from middleware.model import voiceAgent
from fastapi.responses import StreamingResponse
import io

# API endpoint for voice agent
@app.post("/chatbot/voice/")
async def rag(item: voiceAgent):
    try:
        response = voiceAgentController(item.base64,item.extension)
        if response.get("Status") == False:
            return {
                "message":response.get("message"),
                "statusCode":response.get("statusCode"),
                "Status":False
            }
        return StreamingResponse(
            io.BytesIO(response.get("data")),
            media_type="audio/mpeg"
        )
    except Exception as e:
        print(f"Error in rag function - main.py file: {str(e)}")
        return {
            "message":"An error occurred while processing the request.",
            "statusCode":500,
            "Status":False
        }
# Run Command: python -m uvicorn main:app --reload
