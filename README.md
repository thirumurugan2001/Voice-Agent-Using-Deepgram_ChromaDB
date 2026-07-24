# 🎙️ Voice Agent Using Deepgram

An intelligent **Voice-based HR Policy Assistant** that leverages **Deepgram** for speech-to-text and text-to-speech, **RAG (Retrieval-Augmented Generation)** with **ChromaDB** for knowledge retrieval, and an **OpenAI-compatible LLM** to answer HR policy questions via voice interactions.

---

## 🧠 Architecture Overview

```
User Voice (Base64 Audio)
        │
        ▼
┌─────────────────────────────┐
│   base64ToAudio (Utility)   │
│   └── Extract audio file    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   SpeechToText (Deepgram)   │
│   └── Transcribe → Text     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   similaritySearch (RAG)    │
│   └── Query ChromaDB        │
│       └── Get embedding     │
│           (Cohere)          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   ConnectChatBot (LLM)      │
│   ├── Input Guardrail       │
│   ├── LLM Response          │
│   ├── Output Guardrail      │
│   └── Conversation Memory   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   textToVoice (Deepgram)    │
│   └── Synthesize Speech     │
└──────────┬──────────────────┘
           │
           ▼
   Audio File Path (Response)
```

---

## ✨ Features

- **🎤 Speech-to-Text** — Transcribe user voice queries using Deepgram's Nova-3 model.
- **📚 Retrieval-Augmented Generation (RAG)** — Retrieve relevant HR policy content from ChromaDB using vector similarity search.
- **🤖 LLM-Powered Q&A** — Generate contextual answers using an OpenAI-compatible LLM.
- **🔊 Text-to-Speech** — Convert responses back to natural-sounding speech using Deepgram's Aura-2 model.
- **🛡️ Guardrails** — Prompt injection detection and PII (Personally Identifiable Information) filtering on both input and output.
- **💬 Conversation Memory** — Maintain conversation context across interactions using LangChain's `ConversationSummaryMemory`.
- **🐳 Docker Support** — Containerized deployment with FFmpeg for audio handling.

---

## 🏗️ Project Structure

```
Voice-Agent-Using-Deepgram/
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
├── .gitignore                     # Git ignore rules
├── LICENSE                        # License file
├── create_rag_pipeline.py         # Script to build the RAG pipeline from PDF
├── README.md                      # Project documentation
│
├── Config/
│   └── loadConfig.py              # YAML configuration loader
│
├── schema/
│   └── voiceAgent.py              # Pydantic request model
│
├── middleware/
│   ├── middleware.py              # CORS configuration
│   └── controller.py              # Voice agent request controller
│
├── ragPipeline/
│   ├── fetch_data.py              # PDF text extraction (pypdf)
│   ├── preprocessing.py           # Text cleaning & normalization
│   ├── chunking.py                # Text chunking (LangChain text splitter)
│   ├── dbConnection.py            # ChromaDB client connection
│   ├── vectorstore.py             # Chunk ingestion into ChromaDB
│   └── ragController.py           # RAG query handler
│
├── utils/
│   ├── base64ToAudio.py           # Base64 → audio file conversion
│   ├── speechToText.py            # Deepgram STT
│   ├── textToVoice.py             # Deepgram TTS
│   ├── getEmbedding.py            # Cohere embedding generation
│   ├── ConnectChatBot.py          # LLM interaction with guardrails & memory
│   ├── guardrails.py              # Input/output guardrail logic
│   └── rag.py                     # ChromaDB similarity search
│
├── Audio/                         # Generated audio responses
├── Assest/
│   └── hr_policy_details.pdf      # Sample HR policy PDF
│
└── Config/
    └── config.yaml                # App configuration (not tracked in git)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- FFmpeg (for audio processing)
- API Keys:
  - [Deepgram](https://deepgram.com/) API Key
  - [OpenAI-compatible](https://platform.openai.com/) API Key / Base URL
  - [Cohere](https://cohere.com/) API Key
  - [ChromaDB](https://www.trychroma.com/) Cloud credentials

### 1. Clone & Setup

```bash
git clone https://github.com/your-username/Voice-Agent-Using-Deepgram.git
cd Voice-Agent-Using-Deepgram
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
DEEPGRAM_API_KEY=your_deepgram_api_key
OPEN_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
CHROMA_API_KEY=your_chromadb_api_key
```

### 3. Configuration

Edit `Config/config.yaml` (create from template):

```yaml
document:
  pdf_path: "Assest/hr_policy_details.pdf"

ChromaDB:
  CHROMA_TENANT: "your-tenant"
  CHROMA_DATABASE: "your-database"
  COLLECTION_NAME: "hr_policy_collection"

OPEN_AI:
  MODEL: "gpt-4o-mini"  # or any OpenAI-compatible model
  API_BASE_URL: "https://api.openai.com/v1"
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Build the RAG Pipeline

Ingest the HR policy PDF into ChromaDB:

```bash
python create_rag_pipeline.py
```

### 6. Run the Server

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t voice-agent-deepgram .

# Run the container
docker run -p 8000:8000 \
  -e DEEPGRAM_API_KEY=your_key \
  -e OPEN_API_KEY=your_key \
  -e COHERE_API_KEY=your_key \
  -e CHROMA_API_KEY=your_key \
  voice-agent-deepgram
```

---

## 📡 API Reference

### `POST /chatbot/voice/`

Process a voice query and return an audio response.

**Request Body:**

```json
{
  "base64": "data:audio/ogg;base64,T2dnUwACAAAAAAAAAA...",
  "extension": ".wav"
}
```

| Field       | Type   | Description                                  |
|-------------|--------|----------------------------------------------|
| `base64`    | string | Base64-encoded audio data (with data URI prefix) |
| `extension` | string | Audio file extension (e.g., `.wav`, `.mp3`)  |

**Success Response (200):**

```json
{
  "message": "Successfully generated the response and stored it in the Audio folder.",
  "statusCode": 200,
  "Status": true,
  "data": [
    {
      "file_path": "C:/path/to/Audio/uuid.mp3"
    }
  ]
}
```

**Error Response (400/500):**

```json
{
  "message": "Failed to transcribe audio!",
  "statusCode": 400,
  "Status": false
}
```

---

## 🛡️ Guardrails

The system implements **dual guardrails** for security:

### Input Guardrail
- ✅ Empty/Length check (max 2000 characters)
- ✅ Prompt injection detection
- ✅ PII detection (email, phone, Aadhaar, credit card)
- ✅ Blocks harmful or out-of-scope queries

### Output Guardrail
- ✅ Prevents system prompt leakage
- ✅ Blocks PII in LLM responses
- ✅ Ensures responses are safe and appropriate

---

## 🧩 Key Technologies

| Technology          | Purpose                               |
|---------------------|---------------------------------------|
| **FastAPI**         | Web framework for REST API            |
| **Deepgram**        | Speech-to-Text (Nova-3) & Text-to-Speech (Aura-2) |
| **ChromaDB**        | Vector database for RAG               |
| **Cohere**          | Text embeddings (embed-english-v3.0)  |
| **OpenAI / LLM**    | Language model for answer generation  |
| **LangChain**       | Text splitting & conversation memory  |
| **pypdf**           | PDF text extraction                   |
| **Docker**          | Containerization                      |

---

## 🔄 Pipeline Flow (Detailed)

### RAG Pipeline (`create_rag_pipeline.py`)

```
PDF Document
    │
    ▼
load_pdf()           → Extract raw text from PDF
    │
    ▼
preprocess()         → Clean text (remove extra spaces, newlines)
    │
    ▼
chunk_text()         → Split into 500-char chunks (100-char overlap)
    │
    ▼
ingest_chunks()      → Generate Cohere embeddings & store in ChromaDB
```

### Voice Query Flow (`POST /chatbot/voice/`)

```
1. Base64 Audio → Temporary File
2. Temporary File → Text (Deepgram STT)
3. User Query → Embedding (Cohere) → ChromaDB Similarity Search
4. Retrieved Context + Query → LLM (with Input Guardrail)
5. LLM Response → Output Guardrail → Conversation Memory Update
6. Response Text → Audio File (Deepgram TTS)
7. Return Audio File Path
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Deepgram](https://deepgram.com/) for their powerful speech AI APIs
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [Cohere](https://cohere.com/) for embedding models
- [LangChain](https://langchain.com/) for LLM tooling

