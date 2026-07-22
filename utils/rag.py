from Database.dbconnection import dbconnection
from utils.getEmbedding import get_embedding
from utils.ConnectChatBot import ConnectChatBot

# Function to get the most relevant answer from the database
def similaritySearch(Question):
    try:
        print(f"Starting to connect to database and get knowledge base data")
        conn=dbconnection()
        if conn is None:
            return {
                "message":"Failed to connect to database !",
                "statusCode":400,
                "Status":False
            }
        cursor=conn.cursor()

        # Get the embedding for the question and perform a similarity search in the database
        print(f"Starting to get embedding for the question")
        embedding = get_embedding(Question)
        if embedding is None:
            return {
                "message":"Failed to get embedding !",
                "statusCode":400,
                "Status":False
            }
        
        # Perform a similarity search in the database using the embedding
        select_query = """SELECT description, dot_product(vector, JSON_ARRAY_PACK("{0}")) AS score FROM About ORDER BY score DESC LIMIT 2 """.format(embedding)
        cursor.execute(select_query) 
        rows = cursor.fetchall() 
        conn.close()
        knowledgeBaseData=f"{rows[0][0]} and {rows[1][0]}"
        if knowledgeBaseData is None and knowledgeBaseData.strip() == "":
            return None
        return knowledgeBaseData
    except Exception as e:
        print(f"Error in similaritySearch function - rag.py file: {str(e)}")
        return None