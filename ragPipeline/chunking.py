from langchain_text_splitters import RecursiveCharacterTextSplitter

# Function to chunk text into smaller pieces
def chunk_text(text):
    try :
        # Create a RecursiveCharacterTextSplitter instance with specified chunk size and overlap 
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = splitter.split_text(text)
        print(f"Chunking text. Total length: {len(text)} characters.")
        return chunks
    except Exception as e:
        print(f"Error in chunk_text: {str(e)}")
        return []