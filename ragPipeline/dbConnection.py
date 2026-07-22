
from qdrant_client import QdrantClient
from Config.loadConfig import load_config
config = load_config()

# Function to establish a connection to the Qdrant database
def Dbconnection():
    try:
        # Create a QdrantClient instance using the host and port specified in the configuration
        client = QdrantClient(host=config["qdrant"]["host"], port=config["qdrant"]["port"])
        print("Connected to Qdrant successfully.")
        return client
    except Exception as e:
        print(f"Error in Dbconnection: {str(e)}")
        return {
            "Error": str(e),
            "statusCode": 500,
            "message": "Error occurred while connecting to the database.",
            "Status": False
        }