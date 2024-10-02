import re
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from rake_nltk import Rake
import convex
from webscraping import getScholarData

# Load environment variables
load_dotenv("C:\\Users\\maxim\\LitGuide-AI\\my-app\\.env.local")
CONVEX_API_URL = os.getenv("VITE_CONVEX_URL")
client = convex.ConvexClient(CONVEX_API_URL)

# Load Google API Key
load_dotenv("C:\\Users\\maxim\\LitGuide-AI\\my-app\\.env")
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

def fetch_papers(query):
    keywords = extract_keywords(query)
    response = fetch_relevant_keywords(keywords)

    # Send keywords to webscraping for fetching papers
    words = re.split(r",\s*|\s+", response)
    papers, links = getScholarData(words)

    # Return the response with papers and links
    return response, papers, links

def extract_keywords(query, num_keywords=5):
    r = Rake()
    r.extract_keywords_from_text(query)
    keywords_extracted = r.get_ranked_phrases()
    print(f"Extracted Keywords: {keywords_extracted}")
    return keywords_extracted[:num_keywords]  # Return only the top 'num_keywords'

def fetch_relevant_keywords(keywords):
    try:
        prompt_template = """
        Answer the question only by making sense of the keywords provided to you. Fetch relevant keywords and eliminate keywords that don't make any sense. Do not add anything else.
        Output each keyword with a comma as a separator, making sure each keyword is lowercase.

        Keywords:
        """

        model = genai.GenerativeModel(model_name="gemini-1.0-pro")
        convo = model.start_chat(history=[])
        convo.send_message(prompt_template + str(keywords))

        # Save keywords to Convex for later use
        save_keywords_to_convex(convo.last.text)

        return convo.last.text

    except Exception as e:
        print(f"Error fetching relevant keywords: {e}")
        return ""

def save_keywords_to_convex(keywords):
    try:
        keyword_list = re.split(r",\s*|\s+", keywords)
        for word in keyword_list:
            client.mutation("keywords:insertValues", {"keyword": word})
    except convex.ConvexError as e:
        print(f"Convex Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def save_message_to_convex(sender, message_sent):
    try:
        client.mutation("messages:send", {"author": sender, "message": message_sent})
    except convex.ConvexError as e:
        print(f"Convex Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def chat_with_pdfs(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    return response["output_text"]

def get_conversational_chain():
    try:
        prompt_template = """
        Answer the question based on the provided context. If the answer is not in the context, respond with "Answer is not available in the context".
        
        Context:\n{context}\n
        Question:\n{question}\n

        Answer:
        """

        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        return chain
    except Exception as e:
        print(f"Error creating conversational chain: {e}")
        return None

def get_pdf_text(pdf_docs):
    try:
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    except Exception as e:
        print(f"Error creating vector store: {e}")

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def summarize_file(pdf_file_path):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    
    # Create an instance of ChatGoogleGenerativeAI
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    # Now pass the model instance to load_summarize_chain
    chain = load_summarize_chain(model, chain_type="map_reduce")
    summary = chain.run(docs)   
    return summary


if __name__ == "__main__":
    summarize = summarize_file("path-to-pdf")
    print(summarize)