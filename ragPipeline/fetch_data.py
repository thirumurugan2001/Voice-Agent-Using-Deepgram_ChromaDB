import logging
from pypdf import PdfReader
from Config.loadConfig import load_config
logging.getLogger("pypdf").setLevel(logging.CRITICAL)
config = load_config()

# Function to load and extract text from a PDF file
def load_pdf():
    try:
        # Load the PDF file specified in the configuration and extract its text content
        reader = PdfReader(config["document"]["pdf_path"],strict=False)
        text = ""
        # Iterate through each page of the PDF and extract the text, appending it to the 'text' variable
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        print(f"Loaded PDF text successfully. Length: {len(text)} characters.")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None