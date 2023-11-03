from typing import List, Union
from langchain.vectorstores.chroma import Chroma


from langchain.callbacks import get_openai_callback
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import streamlit as st
from langchain.schema import Memory as StreamlitChatMessageHistory
from langchain.llms import CTransformers
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate

########################################

import os
import requests
from time import sleep

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DeepLake, VectorStore
from streamlit.runtime.uploaded_file_manager import UploadedFile


import warnings

from langchain.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate, LLMChain

import os
import tempfile

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

import openai

from langchain.document_loaders import (PyPDFLoader, Docx2txtLoader, CSVLoader,
    DirectoryLoader,
    GitLoader,
    NotebookLoader,
    OnlinePDFLoader,
    PythonLoader,
    TextLoader,
    UnstructuredFileLoader,
    UnstructuredHTMLLoader,
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
    WebBaseLoader,
)


warnings.filterwarnings("ignore", category=UserWarning)

APP_NAME = "ValonyLabsz"
MODEL = "gpt-3.5-turbo"
PAGE_ICON = ":rocket:"

st.set_option("client.showErrorDetails", True)
st.set_page_config(
    page_title=APP_NAME, page_icon=PAGE_ICON, initial_sidebar_state="expanded"
)

#AVATARS
av_us = '/home/ataliba/Documents/Ataliba.png' 
av_ass = '/home/ataliba/Documents/Robot.png'


st.title(":rocket: Agent Lirio :rocket:")
st.markdown("I am your Subsea Technical Assistant ready to do all of the leg work on your documents, emails, procedures, etc.\
    I am capable to extract relevant info and domain knowledge!")

from rebuff import Rebuff

# For a quick start, use our hosted rebuff server with your user's specific API token
# Your `<your_rebuff_api_token>` can be found here: https://www.rebuff.ai/playground#add-to-app

# Alternatively, you can self host your own rebuff server: https://github.com/protectai/rebuff#self-hosting




@st.cache_resource(ttl="1h")

def init_page() -> None:

    st.sidebar.title("Options")

def init_messages() -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="""You are a skilled Subsea Engineer, your task is to answer \
            within the provided documentation information specifically to the text in the {context} \
            Provide a conversational answer. If you don't know the answer, \
            just say 'Sorry, I don't have the info right now at hand \
            let me work it out and get back to you asap... 😔.\ 
            Don't try to make up an answer.
            If the question is not about the {context}}, politely inform them that you are tuned to \
            answer each of the questions at at the time based on the {context} given. \
            Reply your answer in markdown format.\
            {context} \
            Question: {question} \
            Helpful Answer:""")  
            ]
            
            
user_query = st.chat_input(placeholder="Ask me Anything!")

def select_llm() -> Union[ChatOpenAI, LlamaCpp]:
    
   # os.environ['REPLICATE_API_TOKEN'] = "r8_DrLQ8zg0vH0yG5Hdvw7CFUfrzHgjQ8M1nHpak"
    
    model_name = st.sidebar.radio("Choose LLM:", ("gpt-3.5-turbo-0613", "gpt-4", "llama-2"), key="llm_choice")
    
    temperature = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    
    if model_name.startswith("gpt-"):
                    
      
        return ChatOpenAI(temperature=temperature, model_name=model_name, streaming=True
)
        
    
    elif model_name.startswith("llama-2-"):
	    
	API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-hf"
        headers = {"Authorization": "Bearer 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"}
	    
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        
        return CTransformers(model=API_URL,
                                model_type="llama",
                                max_new_tokens=512,
                                temperature=temperature)

        
openai_api_key = "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"



def configure_qa_chain(uploaded_files):
       
    # Read documents
    docs = []
    #temp_dir = tempfile.TemporaryDirectory()
    
    if uploaded_files:
        
        
    # Load the data and perform preprocessing only if it hasn't been loaded before
      if "processed_data" not in st.session_state:
        # Load the data from uploaded files
          documents = []
        
      for file in uploaded_files:
        
         # Get file extension
           #_, file_extension = os.path.splitext(file.name)
        
           temp_filepath = os.path.join(os.getcwd(), file.name) # os.path.join(temp_dir.name, file.name)
        
           with open(temp_filepath, "wb") as f:
             f.write(file.getvalue())
            
        
        
        
        # Handling PDF files
           if temp_filepath.endswith((".pdf", ".docx", ".txt")):  #if temp_filepath.lower() == (".pdf", ".docx", ".txt"):
              loader = UnstructuredFileLoader(temp_filepath)
              loaded_documents = loader.load() #loader = PyPDFLoader(temp_filepath)
              docs.extend(loaded_documents) #loader.load_and_split())
        # Handling DOCX files
        #elif file_extension.lower() == ".docx": # or file_extension.lower() == ".doc":
        #    loader = UnstructuredFileLoader(temp_filepath)
        #    docs.extend(loader.load_and_split())
            
        #else:
        #    print(f"Unsupported file type: {file_extension}")
            # Handle or log the unsupported file type as per your application's needs
           
       


    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create embeddings and store in vectordb
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# load vector database, uncomment below two lines if you'd like to create it
    persist_directory = "/home/ataliba/LLM_Workshop/Experimental_Lama_QA_Retrieval/db/"
#################### run only once at beginning ####################
    db = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_directory)
    db.persist()
####################################################################
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    memory = ConversationBufferMemory(
    memory_key="chat_history", output_key='answer', return_messages=False)    
         
    #openai_api_key = os.environ['OPENAI_API_KEY']
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    #memory = ConversationBufferMemory(
    #memory_key="chat_history", output_key='answer', return_messages=False)
      
    #embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)

    # Define retriever
    #retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
        
    return retriever

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)

class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container.expander("Context Retrieval")

    def on_retriever_start(self, query: str):  #def on_retriever_start(self, query: str, **kwargs):
        self.container.write(f"**Question:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        # self.container.write(documents)
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.container.write(f"**Document {idx} from {source}**")
            self.container.markdown(doc.page_content)

uploaded_files = st.sidebar.file_uploader(
    label="Upload your files", accept_multiple_files=True,type=None
)
if not uploaded_files:
    st.info("Please upload your documents to continue.")
    st.stop()

retriever = configure_qa_chain(uploaded_files)

# Setup memory for contextual conversation
#msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", output_key='answer', return_messages=True)

# Setup LLM and QA chain
llm = select_llm() # model_name="gpt-3.5-turbo"

 # Create system prompt

qa_chain = ConversationalRetrievalChain.from_llm(
        llm, retriever=retriever, memory=memory) #retriever=retriever, memory=memory)#, verbose=False
    #)
#QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)
#qa_chain = SystemMessagePromptTemplate(prompt=QA_CHAIN_PROMPT)
		
		

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "Please let me know how can I be of a help today?"}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message(msg["role"],avatar=av_us):
            st.markdown(msg["content"])
    else:
        with st.chat_message(msg["role"],avatar=av_ass):
            st.markdown(msg["content"])
if user_query: #
 
    st.session_state.messages.append({"role": "user", "content": user_query})
  
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        message_placeholder =  st.empty()
        full_response = ""
        
        cb = PrintRetrievalHandler(st.container())
         # Get the selected model or prompt template
        
        

        response = qa_chain.run(user_query, callbacks=[cb])
        
        resp = response.split(" ")
        
        for r in resp:
             full_response = full_response + r + " "
             message_placeholder.markdown(full_response + "▌")
             sleep(0.1)
        
        message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        #st.write(response)
        
        
        
    
 
        


