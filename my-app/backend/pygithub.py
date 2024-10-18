from github import Github
import re
import os
from dotenv import load_dotenv

load_dotenv("C:\\Users\\maxim\\LitGuide-AI\\my-app\\.env")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
github_client = Github(GITHUB_API_KEY)

def get_topics(keywords):
    #print(keywords)
    topics = set()
    for el in keywords:
        topics.add(el["keyword"])
        
    return topics

def search_repos(keywords):
    print(f"Keywords to be searched are: {keywords}")
    print(type(keywords))
    print(github_client.get_rate_limit())

    keyword_list = [kw.strip() for kw in keywords.split(',')]

    query = ", ".join(keyword_list) + " in:description,readme,name"
    print(f"Constructed query: {query}")


    repos = github_client.search_repositories(query=query)
    if repos == None:
        print("search results are None.")

    repo_dict = {}
    for i, repo in enumerate(repos):
        if i >= 100:
            break

        #print(repo.full_name, repo.description, repo.topics)
        repo_dict[repo.full_name] = {
            "desc": repo.description,
            "topics": repo.topics
        }


    if len(repo_dict)==0:
        print("searched results: 0")
    print(repo_dict)

    return repo_dict