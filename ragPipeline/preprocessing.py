import re

# Function to preprocess text by removing newlines, extra spaces, and trimming whitespace
def preprocess(text: str):
    try :

        # Remove newlines and extra spaces, then trim whitespace
        text = text.replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text)
        cleaned_text = text.strip()
        print(f"Preprocessed text. Length: {len(cleaned_text)} characters.")
        return cleaned_text
    except Exception as e:
        print(f"Error in preprocess: {str(e)}")
        return None
