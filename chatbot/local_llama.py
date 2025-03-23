from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #Used to create a prompt template
from langchain_core.output_parsers import StrOutputParser  #Default output parser to parse the output
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true" #Feature for langsmith#Enables LangChain's new tracing system for better debugging and observability.
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY") #gets key from .env file

#Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

##streamlit framework

st.title("Langchain Demo with Ollama API")
input_text=st.text_input("What do you want to learn today?")

##openAI LLM
llm=Ollama(model="llama2")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))

