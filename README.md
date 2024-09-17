# LitGuide-AI
This project builds an Academic Paper Chatbot that allows users to interact with PDFs in a conversational way.

## Description
LitGuide-AI is a research tool designed to assist students in STEM and other research fields. Recognizing the challenges students often face in understanding complex academic literature, LitGuide-AI aims to:

1. Simplify technical jargon: Provide clear explanations and context for difficult terms and concepts.
2. Facilitate resource discovery: Help students locate relevant research articles, papers, and studies.
3. Empower students: Equip students with the tools and knowledge they need to conduct effective research.
4. By bridging the gap between complex academic language and student understanding, LitGuide-AI empowers students to explore their ideas and engage in meaningful research.

## Technology Stack
**Front-End**: Streamlit (Python library for creating web apps)
**Back-End**: Python & TS
**Natural Language Processing**:
1. NLTK (Python library for text processing)
2. langchain (Python library for NLP pipelines)
3. Gemini Pro-model (pre-trained generative language model)
**Information Retrieval**:
1. FAISS (efficient similarity search library)
2. Convex (Backend-as-a-Service platform for data storage and retrieval)
3. Web Scraping: BeautifulSoup

## Features
### Existing Features
1. Chat with PDFs
2. Fetch Papers using basic web-scraping

### Planned Features
1. Leveraging Convex's features to do away with databases completely
2. Developing a dedicated front-end interface

## "How do I run this project?"
### Dependencies
1. You must have npm installed onto your machine.
2. You must have Python3 or any later versions available.
3. You must have installed Convex using npm onto your local machine. [Click here to learn how.](https://docs.convex.dev/quickstart/python)
4. You can optionally create a virtual environment for this project (recommended).

  
1. Copy the repository link.
2. Clone the project onto your local machine using the 'git clone' command.
3. Once the repository has successfully been cloned onto your machine, open the main repo directory using your preferred IDE, and type 'npx convex dev' . [Click here to see more on this.](https://docs.convex.dev/get-started)
4. Once the command runs in the background, open another terminal, and activate your virtual environment (if you have created one).
5. Run the project using 'streamlit run app.py'.
