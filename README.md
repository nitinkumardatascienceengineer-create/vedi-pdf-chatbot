Vedi – AI-Powered PDF Chatbot

Live Demo: [Try Vedi](https://vedi-pdf-chatbot-xznynlhuq6vjxmsr6bibwb.streamlit.app/)

Vedi is an AI-powered PDF chatbot that allows users to upload PDF documents and ask questions about their content. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate contextual, easy-to-understand answers using Google's Gemini model.

Features

Multiple PDF Uploads: Upload and process multiple PDF documents.

Document Processing: Extract text from PDFs and split it into manageable chunks.

Semantic Search: Find relevant information using vector embeddings and FAISS.

AI-Powered Answers: Generate contextual responses using Gemini 2.5 Flash.

Source References: Display source PDF filenames and page numbers.

Interactive Chat Interface: Ask questions and explore document content.

Student-Friendly Explanations: Understand technical concepts through simple explanations, examples, and step-by-step guidance.

Technology Stack

Technology

Purpose

Python

Core programming language

Streamlit

Web application interface

LangChain

RAG pipeline orchestration

Google Gemini 2.5 Flash

Language model

Hugging Face

Embedding model integration

Sentence Transformers

Text embeddings

FAISS

Vector database

PyPDF

PDF text extraction

How It Works

Vedi follows a Retrieval-Augmented Generation (RAG) workflow.

PDF Upload: Users upload one or more PDF documents.

Text Extraction: PyPDFLoader extracts text from uploaded documents.

Text Chunking: RecursiveCharacterTextSplitter divides documents into smaller chunks.

Embedding Generation: The all-MiniLM-L6-v2 model converts text chunks into numerical embeddings.

Vector Storage: FAISS stores the embeddings for efficient similarity search.

Information Retrieval: When a user asks a question, Vedi retrieves relevant document chunks using Maximum Marginal Relevance (MMR).

Answer Generation: Gemini 2.5 Flash uses the retrieved context to generate an informative response.

Source Display: Vedi displays the source document and corresponding page numbers.

Project Structure

vedi-pdf-chatbot/
│
├── app.py                  # Streamlit application
├── rag_pipeline.py         # RAG pipeline implementation
├── requirements.txt        # Project dependencies
├── .gitignore              # Git ignored files
│
└── .streamlit/
    └── secrets.toml        # API key configuration

Installation and Setup

1. Clone the Repository

git clone https://github.com/nitinkumardatascienceengineer-create/vedi-pdf-chatbot.git

2. Navigate to the Project Directory

cd vedi-pdf-chatbot

3. Create a Virtual Environment

python -m venv .venv

Activate the environment on Windows:

.venv\Scripts\activate

4. Install Dependencies

pip install -r requirements.txt

5. Configure the Gemini API Key

Create a .streamlit folder in the project directory and create a secrets.toml file inside it.

Add your Gemini API key:

GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"

6. Run the Application

streamlit run app.py

The application will open in your default web browser.

API Configuration

Vedi requires a Google Gemini API key.

For local development, configure the key in .streamlit/secrets.toml.

For Streamlit Community Cloud, add the key through the application's Secrets settings.

Never upload API keys or secret files to GitHub.

Future Improvements

Conversation memory for contextual follow-up questions.

Persistent vector database storage.

Support for additional document formats.

Improved document retrieval and reranking.

Chat history export.

User authentication.

Author

Nitin Kumar

GitHub: nitinkumardatascienceengineer-create

Vedi – Making Document Understanding Easier with AI.
