# LitGuide-AI

This project builds an Academic Paper Chatbot that allows users to interact with PDFs in a conversational way.

## IMPORTANT NOTE

This project won the the first runner-up for the 'HackRush 1.0' Hackathon hosted by Qwiklabs under the 'EdTech Track' at SRMIST, KTR.

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
4. FAISS (efficient similarity search library)
5. Convex (Backend-as-a-Service platform for data storage and retrieval)
6. Web Scraping: BeautifulSoup
7. GitHub API: Recommending Tech Stack for similar projects.

## Features

### Existing Features

1. Chat with PDFs
2. Fetch Papers using basic web-scraping
3. Summarize PDFs
4. Recommend Popularly used Technology Stack from GitHub Repos

### Planned Features

1. Leveraging Convex's features to do away with databases completely
2. Developing a dedicated front-end interface
3. Improving recommendation of tech stack
4. Improving performance of 'Chat with PDFs' and 'Summarize PDFs' options

## "How do I run this project?"

### Dependencies

1. You must have npm installed onto your machine.
2. You must have Python3 or any later versions available.
3. You must have installed Convex using npm onto your local machine. [Click here to learn how.](https://docs.convex.dev/quickstart/python)
4. You can optionally create a virtual environment for this project (recommended).
5. You have to fetch 3 API Keys: [Gemini API KEY](https://www.youtube.com/watch?v=OVnnVnLZPEo&pp=ygUSZ2V0IGdlbWluaSBhcGkga2V5), GitHub API Key (navigate to Settings -> Personal Access Tokens -> Tokens (Classics) -> Generate New Token -> Check relevant scopes -> Generate) & a [Convex URL Key: generated using command](https://docs.convex.dev/get-started)

### Steps

1. Copy the repository link.
2. Clone the project onto your local machine using the 'git clone' command.
3. Once the repository has successfully been cloned onto your machine, open the main repo directory using your preferred IDE, and type 'npx convex dev' . [Click here to see more on this.](https://docs.convex.dev/get-started)
4. Once the command runs in the background, open another terminal, and activate your virtual environment (if you have created one).
5. Make sure to move keywords.ts, messages.ts and schema.ts into the folder created by generating 'convex url key'.
6. Update paths to .env and .env.local correctly.
7. Run the project using 'streamlit run app.py'.
