from xmlrpc import client
from rag_utils.embedding import get_embedding
from rag_utils.ConnectChatBot import ConnectChatBot
from rag_utils.dbConnection import Dbconnection
from Config.loadConfig import load_config
config = load_config()

# Function to perform Retrieval-Augmented Generation (RAG) based on the provided question
def rag(Question):
    try:
        # Establish a connection to the Qdrant database and retrieve the top matches based on the embedding of the question
        client=Dbconnection()

        # Generate the embedding for the provided question using the get_embedding function
        embedding = get_embedding(Question)

        # Query the Qdrant collection for the top matches based on the embedding of the question, limiting the results to 2
        top_matches = client.query_points(collection_name=config["qdrant"]["collection_name"],query=embedding,limit=2)
        texts = []

        # Iterate through the top matches and extract the text from the payload of each match, appending it to the 'texts' list
        for hit in top_matches.points:
            texts.append(hit.payload["text"])
        context = "\n".join(texts)
        
        # Call the ConnectChatBot function with the provided question and the retrieved context to generate a response
        response = ConnectChatBot(Question,context)
        if response is None:
            return {
                "statusCode":200,
                "status":False,
                "message":"No relevant information found in the database.",
            }
        return {
            "statusCode":200,
            "status":True,
            "message":"Relevant information found.",
            "response":response
        }
    except Exception as e:
        print(f"Error in rag function: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "message":"Error occurred while processing the request.",
                "Status":False
            }
