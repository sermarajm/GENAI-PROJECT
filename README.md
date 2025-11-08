🧠 GENAI-PROJECT — Generative AI Knowledge Base Chatbot
📘 Overview

The GenAI Project is a Flask-based Generative AI system designed to:

Ingest and extract knowledge from PDF files

Store embeddings in a PostgreSQL database using vector similarity

Answer user queries via semantic search and large language models (LLMs)

Provide REST APIs for interaction and integration

This setup supports a Knowledge Base creation workflow and LLM-powered question answering.

🏗️ Project Structure
GenAI_PJ/
│
├── docker-compose.yml              # Docker setup (Flask API + PostgreSQL + pgvector)
│
├── api/
│   ├── main.py                     # Flask API entry point
│   ├── aiservice.py                # Handles LLM and intent classification
│   ├── contants.py                 # System prompt and configuration constants
│   ├── utils.py                    # JSON and data extraction helpers
│   │
│   ├── kb_service/                 # Knowledge Base Service Layer
│   │   ├── DBService.py            # PostgreSQL database connection manager
│   │   ├── Embedding.py            # Embedding generation and database insertion
│   │   ├── pdf_extraction.py       # Extracts text content from PDFs
│   │   ├── similarity_search.py    # Vector-based similarity search in the DB
│   │   ├── Requirement.txt         # Dependencies for the KB service
│   │   ├── assets/                 # Sample extracted text data
│   │   └── __init__.py
│   │
│   └── kb_info/                    # Uploaded knowledge base text data
│       ├── <UUID>_share price.pdf.txt
│       ├── <UUID>_Data Science.pdf.txt
│
└── .env                            # Environment variables (API keys, DB creds)

⚙️ Setup Instructions
1️⃣ Prerequisites

Make sure you have:

Python 3.10+

Docker & Docker Compose

PostgreSQL with pgvector extension

Google Generative AI SDK (google-genai)

2️⃣ Environment Variables (.env)

Create a .env file in the project root with the following:

POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=genai_db
GOOGLE_API_KEY=your_google_api_key
EMBEDDING_MODEL=models/embedding-001
GENAI_MODEL=gemini-1.5-flash

3️⃣ Install Dependencies
cd api/kb_service
pip install -r Requirement.txt

4️⃣ Run with Docker

To spin up the full environment (Flask + PostgreSQL + pgvector):

docker-compose up --build

🚀 API Endpoints
Endpoint	Method	Description
/upload	POST	Uploads a PDF and extracts its text
/create_kb	POST	Generates embeddings and stores them in DB
/ask	POST	Sends a query, performs similarity search, and returns LLM-generated answer

Example request:

POST /ask
{
  "question": "What is the CGPA of Sermaraj?",
  "session_id": "123"
}

🧩 Core Components
🔹 aiservice.py

Handles LLM calls:

Uses Google Generative AI for text embeddings and chat completions.

Functions: call_llm(), intent_classifier()

🔹 Embedding.py

Generates embeddings for text chunks using Google Embedding API.

Stores them in PostgreSQL with vector columns (pgvector).

🔹 pdf_extraction.py

Extracts clean text from PDF uploads.

Saves extracted text in /kb_info/.

🔹 similarity_search.py

Fetches semantically similar text chunks from DB.

Used to find context for answering user queries.

🔹 main.py

Flask server routes for uploading, embedding creation, and query handling.

Integrates all other modules.

🧠 Knowledge Flow Diagram
PDF → Extract Text → Create Embeddings → Store in DB → User Query → Similarity Search → LLM Answer

🧪 Example Workflow

Upload a PDF via /upload

Call /create_kb to store embeddings

Query the knowledge base using /ask

🧰 Tech Stack
Category	Tool
Framework	Flask
Database	PostgreSQL + pgvector
LLM API	Google Generative AI
Containerization	Docker
Language	Python 3.10+
👨‍💻 Development Notes

Use flask run for local development (inside api/).

You can update .env to switch between local and cloud databases.

To reset KB data, clear the embeddings_store table.

📄 License

This project is licensed under the MIT License.
