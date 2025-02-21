import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from htmlTemplates import css, bot_template, user_template
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API key for Google Generative AI not found. Please set it in the .env file.")

# PDF Chatbot Functions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    st.warning(f"No text extracted from page in {pdf.name}")
            st.write(f"Extracted text from {pdf.name}: {len(text)} characters.")
        except Exception as e:
            st.error(f"Failed to process {pdf.name}: {e}")
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    if not chunks:
        st.error("No text chunks created. Ensure your PDF contains text.")
    st.write(f"Generated {len(chunks)} text chunks.")
    return chunks

def get_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise ValueError("No text chunks available to create FAISS index.")

        # Use API key directly
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key  # Pass your API key here
        )
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        st.success("FAISS index created and saved successfully.")
    except Exception as e:
        st.error(f"Error in creating FAISS index: {e}")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. Make sure to provide all the details. If the answer is not in the
    provided context, just say, "answer is not available in the context." Do not provide a wrong answer.

    Context:\n{context}\n
    Question:\n{question}\n

    Answer:
    """
    # Use API key directly
    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.6,
        google_api_key=api_key  # Pass your API key here
    )
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    try:
        # Use API key directly
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key  # Pass your API key here
        )
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = vector_store.similarity_search(user_question)
        
        if not docs:
            st.write("No relevant documents found for your question.")
            return

        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        
        st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", response.get("output_text", "No response generated.")), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error in processing query: {e}")

# PDF Chatbot Tab
def pdf_chatbot_tab():
    st.header("Chat with your notes 📄")
    st.write(css, unsafe_allow_html=True)

    user_question = st.text_input("Ask your questions")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload PDFs", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                if raw_text:
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("Processing complete!")
                else:
                    st.error("No text found in the uploaded PDFs.")