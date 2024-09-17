import streamlit as st
import re
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import requests
import time
from convex import ConvexClient
import convex
from pprint import pprint
from fetchPapers import extract_keywords
from webscraping_papers import getScholarData
from pygithub import searchRepos, getTopics

# Convex URL and API route for sending messages
load_dotenv("your_path_to_convex_url -> stored in a .env.local file, mostly")
CONVEX_API_URL = os.getenv("CONVEX_URL")
#print(CONVEX_API_URL)
client = convex.ConvexClient(CONVEX_API_URL)

load_dotenv("your_path_to_google_api_key_file -> stored in a .env file, mostly")
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

#print(google_api_key)

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])
    return response["output_text"]

def save_message_to_convex(sender, message_sent):
    try:
        client.mutation("messages:send", {"author": sender, "message":message_sent})
    except convex.ConvexError as err:
        print(err)
    except Exception as err:
        print("Error: " + str(err))

def get_chat_history():
    done = False
    cursor = None
    data = []

    while not done:
        result = client.query("messages:listMessages", {"paginationOpts": {"numItems": 100, "cursor": cursor}})
        #print(result)
        cursor = result['continueCursor']
        done = result["isDone"]
        data.extend(result['page'])
        #print('got', len(result['page']), 'results')    

    print('collected', len(data), 'results')
    return data

def fetch_conferences():
    return 

def save_keywords_to_convex(keywords):
    try:
        keyword_list = re.split(r",\s*|\s+", keywords)  
        for word in keyword_list:
            client.mutation("keywords:insertValues", {"keyword": word})
    except convex.ConvexError as err:
        print(err)
    except Exception as err:
        print("Error: " + str(err))

def update_keywords():
    try:
        keywords = client.query("keywords:listKeywords")
        updated_keywords = update_keywords(keywords)

        print(updated_keywords)
        print(type(updated_keywords))
    
    except Exception as err:
        print(err)

def update_keywords(keywords):
    try:
        prompt_template = """
        Use the keywords provided to you only. Don't generate any output beyond what is asked. Fetch only relevant keywords. Eliminate any irrelevant keywords. 
        Your task is to update the set of keywords given by retaining only the most relevant keywords, and deleting any irrelevant keywords (if ranked low on relevance).
        
        for example, if the keywords given to you are: autism, cognition, technology, people, IT, computer science, applications, java, software, neurodivergent, cognition, improvement, students, academia, institutions, problems, hello, 
        autistic, AAC, device, hardware
        
        Retained Keywords: autism, cognition, technology, java, students
        
        This is because all the other keywords can fall under the retained keywords as umbrella terms. Now carry out the task accordingly, please. Only output the retained keywords, and nothing more.
        Remember to include all topics mentioned
        
        Keywords:"""

        model = genai.GenerativeModel(model_name="gemini-1.0-pro")

        convo = model.start_chat(history=[])

        convo.send_message(prompt_template + str(keywords))
        print(convo.last.text)

    except Exception as err:
        print(err)

def fetch_relevant_keywords(keywords):
    try: 
        prompt_template = """
        Answer the question only by making sense of the keywords provided to you. Fetch relevant keywords and eliminate keywords that don't make any sense. Do not add anything else. 
        Do not do anything else either. Output each keyword with a comma as a separator, making sure each keyword is lowercase. 
        for example, if your question is: [hello, apply, technology, autism, cognition, improvement]
        your output should be: technology, autism, cognition, improvement.

        Remove any duplicates of the keywords. 
        
        eliminate the brackets\n\n

        Keywords:
        """

        model = genai.GenerativeModel(model_name="gemini-1.0-pro")

        convo = model.start_chat(history=[])

        #print(prompt_template + str(keywords))
        convo.send_message(prompt_template + str(keywords))

        save_keywords_to_convex(convo.last.text)
        #print("printing type of response: " + str(type(convo.last.text)))
        return convo.last.text
    
    except Exception as err:
        print(err)

def fetch_papers(user_question):
    keywords = extract_keywords(user_question)
    response = fetch_relevant_keywords(keywords)

    #sending keywords to webscraping_papers.getScholarData
    words = re.split(r",\s*|\s+", response)   
    papers, links = getScholarData(words)

    #sending list of papers to user
    for paper, link in zip(papers, links):
        html_link = f'<a href="{link}">{paper}</a>'
        st.write(html_link, unsafe_allow_html=True)

    return response

def fetch_projects(user_question):
    
    return

def main():
    st.set_page_config("LitGuide-AI")
    st.header("Discuss your projects with Gemini💁")

    chat_history = get_chat_history()
    if chat_history:
        st.subheader("Chat History")
        for entry in chat_history:
            if entry['message'] == "":

                continue
            st.write(f"{entry['author']} : {entry['message']}")

    user_question = st.text_input("Ask a Question from the PDF Files")
    save_message_to_convex("User", user_question)


    # Create a container for the action buttons and user input
    with st.container():
        st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
        }
        .stTextInput > div > div > input {
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("Choose an action and ask a question:")
        col1, col2, col3 = st.columns(3)
        with col1:
            fetch_papers_button = st.button("Fetch Papers")
        with col2:
            chat_papers_button = st.button("Chat with Papers")
        with col3:
            summarize_papers_button = st.button("Summarize Papers")

        user_question = st.text_input("Enter your question:")

    if user_question:
        if fetch_papers_button:
            fetch_papers(user_question)
        elif chat_papers_button:
            response = user_input(user_question)
        elif summarize_papers_button:
            save_message_to_convex("Gemini", response)
        else:
            response = "Please select an action before asking a question."


    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")



if __name__ == "__main__":
    main()