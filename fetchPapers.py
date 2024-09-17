import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from rake_nltk import Rake

def extract_keywords(query, num_keywords = 5):

    r = Rake()
    r.extract_keywords_from_text(query)
    keywords_extracted = r.get_ranked_phrases()
    #print(keywords_extracted)
    return keywords_extracted
