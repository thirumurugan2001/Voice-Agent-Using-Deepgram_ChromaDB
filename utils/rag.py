from ragPipeline.dbConnection import Dbconnection
from utils.getEmbedding import get_embedding
from Config.loadConfig import load_config
config = load_config()


# Function to get the most relevant documents from ChromaDB
def similaritySearch(Question):
    try:
        print("Connecting to ChromaDB ...")
        client = Dbconnection()
        if client is None:
            print("Failed to connect to ChromaDB!")
            return None
        
        collection = client.get_collection(
            name=config["ChromaDB"]["COLLECTION_NAME"]
        )

        print("Starting to get embedding for the question.....")
        embedding = get_embedding(Question)
        if embedding is None:
            return {
                "message": "Failed to get embedding!",
                "statusCode": 400,
                "Status": False
            }

        print("Starting similarity search.....")
        results = collection.query(
            query_embeddings=[embedding],
            n_results=2,
            include=["documents", "metadatas", "distances"]
        )

        print("Check whether documents are available....")
        if ( not results or not results.get("documents") or not results["documents"][0]):
            print("No relevant documents found.")
            return None
        documents = results["documents"][0]
        knowledgeBaseData = " ".join(documents)
        if not knowledgeBaseData.strip():
            return None
        
        print("Similarity search completed successfully.")
        return knowledgeBaseData
    except Exception as e:
        print(f"Error in similaritySearch function - rag.py file: {str(e)}")
        return None