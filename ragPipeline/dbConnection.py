import os
import chromadb
from dotenv import load_dotenv
from Config.loadConfig import load_config
config = load_config()
load_dotenv()

# Function to establish a connection to ChromaDB
def Dbconnection():
    try:
        client = chromadb.CloudClient(
            tenant=config["ChromaDB"]["CHROMA_TENANT"],
            database=config["ChromaDB"]["CHROMA_DATABASE"],
            api_key=os.getenv("CHROMA_API_KEY")
        )
        print("Connected to ChromaDB successfully.")
        return client

    except Exception as e:
        print(f"Error in Dbconnection: {str(e)}")
        return None