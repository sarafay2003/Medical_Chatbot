Project Summary: Medical Report Explainer
Medical Report Explainer is an AI-based system designed to simplify and explain complex medical reports for patients. Often, medical documents are filled with technical jargon that most people find difficult to understand. This tool allows users to upload a medical report (PDF) and interact with a chatbot that provides clear, simplified explanations and answers to health-related questions.

🔍 How It Works:
The user uploads a medical report PDF.

The system uses pdfplumber to extract text from the document.

The text is divided into chunks and converted into vector embeddings using SentenceTransformers (MiniLM).

These vectors are stored in a FAISS index to enable fast retrieval.

When a user asks a question, it is also embedded and compared to the stored chunks.

The most relevant chunks are selected and sent as context to a Groq-hosted LLaMA 3 LLM via API.

The model generates a simplified, context-aware response in natural language.

⚙️ Technology Stack:
Python: Core programming language

Streamlit: For building the interactive chat UI

pdfplumber: To extract text from PDF files

SentenceTransformers (MiniLM): For generating embeddings

FAISS: Vector database for fast similarity search

Groq API (LLaMA 3): Large Language Model for intelligent responses

Hugging Face Spaces: Deployment and hosting

This project offers a practical solution for improving patient health literacy by making medical data more accessible and understandable.
