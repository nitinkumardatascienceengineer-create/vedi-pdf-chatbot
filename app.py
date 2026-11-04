
import streamlit as st

from rag_pipeline import create_vector_store, answer_question


# -------------------------------
# 1. Page configuration
# -------------------------------

st.set_page_config(
    page_title="Vedi - Chat with Your PDFs",
    page_icon="📚",
    layout="wide"
)

st.title("Vedi - Chat with Your PDFs")
st.caption("Upload your documents and ask questions about their content.")


# -------------------------------
# 2. Initialize session state
# -------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []


# -------------------------------
# 3. Sidebar - PDF upload
# -------------------------------

with st.sidebar:

    st.header("Your Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process PDFs", use_container_width=True):

        if not uploaded_files:
            st.warning("Please upload at least one PDF.")

        else:
            try:
                with st.spinner(
                    "Reading PDFs and creating vector database..."
                ):

                    vector_store = create_vector_store(
                        uploaded_files
                    )

                    st.session_state.vector_store = vector_store

                    st.session_state.processed_files = [
                        file.name for file in uploaded_files
                    ]

                    st.session_state.messages = []

                st.success("PDFs processed successfully!")

            except Exception as e:
                st.error(f"Processing failed: {e}")

    if st.session_state.processed_files:

        st.subheader("Processed files")

        for file_name in st.session_state.processed_files:
            st.write(f"📄 {file_name}")

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -------------------------------
# 4. Display chat history
# -------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            sources = message.get("sources", [])

            if sources:
                with st.expander("View sources"):
                    for doc in sources:
                        st.write(
                            f"📄 {doc.metadata.get('source', 'Unknown')} "
                            f"| Page {doc.metadata.get('page', 'N/A')}"
                        )


# -------------------------------
# 5. Chat input
# -------------------------------

question = st.chat_input(
    "Ask something about your PDFs..."
)

if question:

    if st.session_state.vector_store is None:
        st.warning("Please upload and process PDFs first.")

    else:

        # Display user question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Generate answer
        try:
            with st.chat_message("assistant"):

                with st.spinner("Vedi is thinking..."):

                    api_key = st.secrets["GOOGLE_API_KEY"]

                    answer, sources = answer_question(
                        st.session_state.vector_store,
                        question,
                        api_key
                    )

                st.markdown(answer)

                if sources:
                    with st.expander("View sources"):
                        for doc in sources:
                            st.write(
                                f"📄 {doc.metadata.get('source', 'Unknown')} "
                                f"| Page {doc.metadata.get('page', 'N/A')}"
                            )

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

        except Exception as e:
            st.error(f"Something went wrong: {e}")
