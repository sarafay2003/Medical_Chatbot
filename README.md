Medical Report Explainer is an AI-powered Streamlit application that helps patients understand complex medical reports. By uploading a medical PDF, users can interact with a chatbot that simplifies the content and answers health-related questions using large language models (LLMs) and a vector database (FAISS). Built with Python , the system empowers patients with clear, personalized explanations of their medical data.

How It Works:
The user uploads a medical report PDF.
The system uses pdfplumber to extract text from the document.
The text is divided into chunks and converted into vector embeddings using SentenceTransformers (MiniLM).
These vectors are stored in a FAISS index to enable fast retrieval.
When a user asks a question, it is also embedded and compared to the stored chunks.
The most relevant chunks are selected and sent as context to a Groq-hosted LLaMA 3 LLM via API.
The model generates a simplified, context-aware response in natural language.

Technology Stack:
Python: Core programming language
Streamlit: For building the interactive chat UI
pdfplumber: To extract text from PDF files
SentenceTransformers (MiniLM): For generating embeddings
FAISS: Vector database for fast similarity search
Groq API (LLaMA 3): Large Language Model for intelligent responses

This project offers a practical solution for improving patient health literacy by making medical data more accessible and understandable.
