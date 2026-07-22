from utils.getEmbedding import get_embedding
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

# Function to set up a collection in the Qdrant database with specified vector size
def setup_collection(client, collection_name, vector_size):
    try:

        # Recreate the collection with the specified vector size and cosine distance metric
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size, 
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' has been set up successfully.")
        return True
    except Exception as e:
        print(f"Error in setting up collection: {str(e)}")
        return False

# Function to ingest chunks of text into the specified collection in the Qdrant database  
def ingest_chunks(client, collection_name, chunks):
    try :
        print(f"Ingesting {len(chunks)} chunks into collection '{collection_name}'...")
        points = []
        for chunk in chunks:
            embedding = get_embedding(chunk)
            
            # Create a PointStruct for each chunk with a unique ID, embedding vector, and payload containing the text
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()), 
                    vector=embedding, 
                    payload={"text": chunk}  
                )
            )
            print("Chunk are ready to push to Qdrant.")

        # Upsert the points into the specified collection in the Qdrant database   
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"Ingested {len(points)} chunks into collection '{collection_name}'.")
        return True
    except Exception as e:
        print(f"Error in ingesting chunks: {str(e)}")
        return False