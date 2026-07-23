from ragPipeline.dbConnection import Dbconnection
from ragPipeline.fetch_data import load_pdf
from ragPipeline.preprocessing import preprocess
from ragPipeline.chunking import chunk_text
from ragPipeline.vectorstore import ingest_chunks
    

# Function to create a Retrieval-Augmented Generation (RAG) pipeline by loading a PDF, preprocessing the text, chunking it, and ingesting it into a Qdrant collection
def Create_rag_pipeline():
    try:
        # Load the PDF and extract its text
        print("Load the PDF and extract its text")
        text = load_pdf()
        if text is None:    
            return {
                "Error": "Failed to load PDF.",
                "statusCode": 500,
                "message": "Error occurred while loading the PDF.",
                "Status": False
            }

        print("Preprocess the extracted text to clean it up")
        # Preprocess the extracted text to clean it up
        cleaned_text = preprocess(text)
        if cleaned_text is None:
            return {
                "Error": "Failed to preprocess text.",
                "statusCode": 500,
                "message": "Error occurred while preprocessing the text.",
                "Status": False
            }
        
        print("Chunk the cleaned text into smaller pieces for ingestion into the Qdrant collection")
        # Chunk the cleaned text into smaller pieces for ingestion into the Qdrant collection
        chunks = chunk_text(cleaned_text)
        if not chunks:
            return {
                "Error": "Failed to chunk text.",
                "statusCode": 500,
                "message": "Error occurred while chunking the text.",
                "Status": False
            }

        print("Ingest the chunks into the Qdrant collection")
        # Ingest the chunks into the Qdrant collection
        if not ingest_chunks(chunks):
            return {
                "Error": "Failed to ingest chunks into Qdrant.",
                "statusCode": 500,
                "message": "Error occurred while ingesting chunks into Qdrant.",
                "Status": False
            }
        print("RAG pipeline created successfully.")
    
    except Exception as e:
        print(f"Error in Create_rag_pipeline: {str(e)}")
        return {
            "Error": str(e),
            "statusCode": 500,
            "message": "Error occurred while creating the RAG pipeline.",
            "Status": False
        }

if __name__ == "__main__":
    # Run the Create_rag_pipeline function and handle any errors that occur during its execution
    result = Create_rag_pipeline()
    if result is not None and "Error" in result:
        print(f"Pipeline creation failed: {result['Error']}")
    else:
        print("Pipeline created successfully.")     
