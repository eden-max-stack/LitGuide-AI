import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download stopwords if not already available
nltk.download('punkt')
nltk.download('stopwords')

tech_stack_keywords = [
    'python', 'java', 'javascript', 'html', 'css', 'sql', 'nodejs',
    'react', 'angular', 'vue', 'docker', 'kubernetes', 'aws', 'azure',
    'gcp', 'mysql', 'postgresql', 'mongodb', 'redis', 'django', 'flask', 'R'
    # Add more as needed
]

# Function to filter technology stack keywords from descriptions
def filter_tech_stack_keywords(tokenized_words):
    return [word for word in tokenized_words if word in tech_stack_keywords]


# Function to clean and tokenize text
def clean_and_tokenize(text):
    # Convert to lowercase
    text = text.lower()

    # Remove non-alphabetic characters
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]

    return tokens

# Function to extract popular keywords from descriptions
def extract_popular_keywords(repo_data, tech_stack_keywords = tech_stack_keywords):
    #repo_data = searchRepos(keywords)
    all_tokens = []

    for repo, data in repo_data.items():
        description = data['desc'] or ""
        # Clean and tokenize the description
        tokens = clean_and_tokenize(description)
        tech_stack_tokens = filter_tech_stack_keywords(tokens)
        all_tokens.extend(tech_stack_tokens)

    # Count the frequency of each token
    keyword_counter = Counter(all_tokens)

    #for keyword, count in keyword_counter.most_common(10):
     #   print(f"{keyword}: {count}")

    return keyword_counter

