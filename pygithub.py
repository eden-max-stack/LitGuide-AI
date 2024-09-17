from github import Github
import re
import os
from dotenv import load_dotenv

load_dotenv("your_path_to_github_api_key -> stored in a .env file, mostly")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
my_git = Github(GITHUB_API_KEY)

def getTopics(keywords):
    #print(keywords)
    topics = set()
    for el in keywords:
        topics.add(el["keyword"])
        
    return topics

def searchRepos(keywords):
    topics = []
    for el in keywords:
        topics.append(el["keyword"])

    query = " ".join(topics) + "in:description,readme,name"

    repos = my_git.search_repositories(query=query)

    repo_dict = {}
    for repo in repos:
        print(repo.full_name, repo.description, repo.topics)
        repo_dict[repo.full_name] = {
            "desc": repo.description,
            "topics": repo.topics
        }

    return repo_dict