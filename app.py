##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

import streamlit as st
import faiss
import numpy as np
import pickle
import os
import requests
from sentence_transformers import SentenceTransformer
import pdfplumber

st.set_page_config(page_title="Medical Report Explainer", page_icon="🧠")
st.title("🧠 Medical Report Explainer Chatbot")
st.markdown("Upload a medical report PDF and ask questions about it.")

# Groq API Key input
GROQ_API_KEY = st.text_input("Enter your Groq API Key", type="password")

# Load SentenceTransformer model for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and chunks from saved data
def load_index(path="data"):
    index = faiss.read_index(os.path.join(path, "faiss.index"))
    with open(os.path.join(path, "chunks.pkl"), "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def search_index(index, query_embedding, chunks, top_k=3):
    D, I = index.search(np.array([query_embedding]), top_k)
    return [chunks[i] for i in I[0]]

def query_groq(question, context, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI that explains medical reports in easy-to-understand language."
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuestion: {question}"
            }
        ],
        "temperature": 0.5
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Upload a new PDF (optional)
uploaded_file = st.file_uploader("Or upload a new PDF report to analyze", type=["pdf"])

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    st.info("Processing uploaded PDF...")

    with pdfplumber.open("temp.pdf") as pdf:
        full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])

    chunks = [" ".join(full_text.split()[i:i+500]) for i in range(0, len(full_text.split()), 500)]
    embeddings = embedding_model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(np.array(embeddings))

    st.success("PDF uploaded and processed! Ask your question below.")

else:
    # Load existing index and chunks (from Colab output)
    if os.path.exists("data/faiss.index") and os.path.exists("data/chunks.pkl"):
        index, chunks = load_index("data")
    else:
        st.warning("Please upload a PDF or place the pre-processed data in the 'data/' folder.")
        st.stop()

# Question input
query = st.text_input("💬 Ask a question about your report:")

# Submit
if st.button("Submit") and query and GROQ_API_KEY:
    q_embedding = embedding_model.encode([query])[0]
    top_chunks = search_index(index, q_embedding, chunks)
    context = "\n\n".join(top_chunks)
    try:
        answer = query_groq(query, context, GROQ_API_KEY)
        st.markdown("### 🧾 Answer")
        st.write(answer)
    except Exception as e:
        st.error(f"Groq API error: {e}")
