import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate


# 1. Initialize embeddings

def get_embeddings():
    
    return HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "token": False
        }
    )
    
# 2. Load Multiple PDFs


def load_pdfs(uploaded_files):

    documents = []

    # Ensure we have a flat list of uploaded files
    if not isinstance(uploaded_files, (list, tuple)):
        uploaded_files = [uploaded_files]

    flattened_files = []

    for item in uploaded_files:
        if isinstance(item, (list, tuple)):
            flattened_files.extend(item)
        else:
            flattened_files.append(item)

    for uploaded_file in flattened_files:

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            loader = PyPDFLoader(temp_path)
            pdf_documents = loader.load()

            for doc in pdf_documents:
                doc.metadata["source"] = uploaded_file.name
                doc.metadata["page"] += 1

            documents.extend(pdf_documents)

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    return documents


# Split documents into chunks

def split_documents(documents):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    
    return splitter.split_documents(documents)

#  Create FAISS vector database

def create_vector_store(uploaded_files):
    
    documents = load_pdfs(uploaded_files)
    
    if not documents:
        raise ValueError("No readable text found in uploaded PDFs.")
    
    chunks = split_documents(documents)
    
    embeddings = get_embeddings()
    
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )
    
    return vector_store

# Answer questions using Gemini

def answer_question(vector_store,question,api_key):
    
    retriever = vector_store.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            "k":4,
            "fetch_k" : 20,
            "lambda_mult" : 0.7
        }
    )
    
    relevant_docs = retriever.invoke(question)
    
    context = "\n\n".join(
        [
            f"Source : {doc.metadata['source']},"
            f"Page : {doc.metadata['page']}\n"
            f"{doc.page_content}"
            for doc in relevant_docs
        ]
    )
    
    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        temperature = 0,
        google_api_key = api_key
    )
    
    prompt = ChatPromptTemplate.from_template(
    """
    You are Vedi, an intelligent and friendly AI tutor.

    Your job is to help students understand the topics
    explained in their uploaded PDFs.

    USER QUESTION:
    {question}

    RETRIEVED PDF CONTEXT:
    {context}

    INSTRUCTIONS:

    1. Understand the question before answering.

    2. Use the PDF context as your primary source of information.

    3. Do not simply copy paragraphs from the PDF.
       Explain the concepts in your own words.

    4. If the user asks for a simple explanation:
       - Use easy English.
       - Break complicated ideas into smaller parts.
       - Give relatable real-world examples.
       - Explain technical terms.

    5. If the user asks how something works:
       Explain the process step by step.

    6. If the user asks for a definition:
       Give a clear definition followed by an explanation.

    7. You may use your general knowledge to simplify,
       explain and illustrate concepts, but do not present
       unsupported facts as if they came from the PDF.

    8. If the PDF does not contain enough information
       to answer the question, clearly say so.
       You may offer additional general knowledge,
       but label it as additional explanation.

    9. Never invent information or pretend that a claim
       is supported by the PDF when it is not.

    10. Keep answers structured with headings, bullet points
        and examples whenever useful.

    Give an answer that helps the student actually
    understand the concept, not just memorize it.

    ANSWER:
    """
    )
    
    chain = prompt | llm 
    
    response = chain.invoke({
        "context": context,
        "question" : question
    })
    
    return response.content, relevant_docs