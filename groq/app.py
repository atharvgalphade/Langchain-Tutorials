import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY=os.environ["GROQ_API_KEY"]

if "vector" not in st.session_state:
    st.session_state.embeddings=OllamaEmbeddings()
    st.session_state.loader=WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs=st.session_state.loader.load()
    
    st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs[:30])
    st.session_state.vectors=FAISS.from_documents(documents=st.session_state.final_documents, embedding=st.session_state.embeddings)
    
    st.title("Chatbot using Groq")
    llm=ChatGroq(groq_api_key=GROQ_API_KEY,
                 model_name="Gemma2-9b-It")
    
    prompt=ChatPromptTemplate.from_template(
        """
        Answer the questions based on the provided context only.
        Please provide the most accurate response, based on the question
        <context>
        {context}
        <context>
        Questions:{input}
        """
    )
    
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    
    prompt=st.text_input("Input your prompt here")
    
    if prompt:
        response=retrieval_chain.invoke({"input":prompt})
        st.write(response['answer'])