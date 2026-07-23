from utils.getEmbedding import get_embedding
from ragPipeline.dbConnection import Dbconnection
from Config.loadConfig import load_config
config = load_config()
import uuid


# Function to ingest chunks into ChromaDB
def ingest_chunks(chunks):
    try:
        # Establish ChromaDB connection
        client = Dbconnection()

        if client is None:
            return False
        
        # Get the existing collection
        collection = client.get_collection(
            name=config["ChromaDB"]["COLLECTION_NAME"]
        )

        # Insert each chunk
        for index, chunk in enumerate(chunks):
            # Generate embedding
            embedding = get_embedding(chunk)
            if embedding is None:
                print(f"Failed to generate embedding for chunk")
                continue

            document_id = str(uuid.uuid4())

            # Insert into ChromaDB
            metadata = {
                "source": "HR_Policy.pdf",
                "chunk_index": index,
                "document_type": "hr_policy"
            }
            collection.add(
                ids=[document_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[metadata]
            )

        print(f"Successfully ingested {len(chunks)} chunks into ChromaDB.")
        return {
            "message": "Chunks ingested successfully.",
            "statusCode": 200,
            "Status": True
        }

    except Exception as e:
        print(f"Error in ingesting chunks Vectorstore.py file : {str(e)}")
        return False