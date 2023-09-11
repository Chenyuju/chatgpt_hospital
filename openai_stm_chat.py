import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
#from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
import os

#st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
#openai.api_key = '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'
#API_KEY = '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'
# Add your openai api key for use
os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.environ["OPENAI_API_KEY"]
st.title("챗봇")
#st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "궁금한 것이 있으면 물어보세요."}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="잠시만 기다려주세요. 1~2분 정도 걸립니다."):
        #reader = SimpleDirectoryReader(input_dir="./data", recursive=True)		
        #docs = reader.load_data()
        reader = SimpleDirectoryReader(input_dir="C:/Users/Chan/Desktop/docs/txt_hos", recursive=True)		
        docs = reader.load_data()
        #reader = TextLoader('C:/Users/Chan/Desktop/docs/txt_hos/data_no_nan.txt', encoding='utf-8')
        #docs = [reader]
        #service_context = ServiceContext.from_defaults(llm=ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0.5))
        index = VectorStoreIndex.from_documents(docs)
        return index

index = load_data()
from llama_index.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=2000)
# react, openai, context, condense_question
# chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
chat_engine = index.as_chat_engine(chat_mode="condense_question", memory=memory, verbose=True)

if prompt := st.chat_input("질문을 입력하세요."): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("검색중..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            st.write('자세한 내용은 골든나비스(010-1234-5678)에 연락주시면 됩니다.')
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history