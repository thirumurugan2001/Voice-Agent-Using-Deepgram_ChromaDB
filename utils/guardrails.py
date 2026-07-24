import re

# Common prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore (all|any|the|your|previous) instructions",
    r"ignore previous",
    r"forget (all|your|the) instructions",
    r"reveal (your|the) system prompt",
    r"show (your|the) system prompt",
    r"print (your|the) system prompt",
    r"what is your system prompt",
    r"developer message",
    r"reveal internal instructions",
    r"bypass (the )?(rules|policy|instructions)",
    r"override (the )?(rules|instructions|policy)",
    r"act as (an?|the)",
    r"jailbreak",
]

# Basic PII patterns
PII_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
}

# Detect basic prompt injection attempts.
def check_prompt_injection(text):
    try:
        text = text.lower()
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True
    except Exception as e:
        print(f"Error in check_prompt_injection function - Guardrails.py file: {str(e)}")
        return None
    
#  Detect sensitive information.
def check_pii(text):
    try:
        detected = []
        for pii_type, pattern in PII_PATTERNS.items():
            if re.search(pattern, text):
                detected.append(pii_type)
        return detected
    except Exception as e:
            print(f"Error in check_pii function - Guardrails.py file: {str(e)}")
            return []

# Validate user input before sending it to RAG/LLM.
def input_guardrail(question):
    if not question or not question.strip():
        return {
            "allowed": False,
            "message": "Please enter a valid HR Policy question."
        }

    # Limit input length
    if len(question) > 2000:
        return {
            "allowed": False,
            "message": "Your question is too long. Please provide a shorter question."
        }

    # Prompt injection check
    if not check_prompt_injection(question):
        return {
            "allowed": False,
            "message": "I can only assist with questions related to the HR Policy document."
        }

    # PII check
    pii = check_pii(question)
    if pii:
        return {
            "allowed": False,
            "message": "Please do not provide sensitive personal information."
        }
    return {
        "allowed": True,
        "message": None
    }
    
# Validate LLM response before returning it to user.
def output_guardrail(response):
    if not response:
        return {
            "allowed": False,
            "message": "Unable to generate a response."
        }

    # Prevent accidental system prompt exposure
    blocked_patterns = [
        "system prompt",
        "developer message",
        "internal instructions",
        "hidden instructions"
    ]

    response_lower = response.lower()
    for pattern in blocked_patterns:
        if pattern in response_lower:
            return {
                "allowed": False,
                "message": "I can only assist with questions related to the HR Policy document."
            }

    # Prevent PII leakage
    pii = check_pii(response)
    if pii:
        return {
            "allowed": False,
            "message": "The response contained sensitive information and cannot be displayed."
        }
    
    return {
        "allowed": True,
        "message": response
    }