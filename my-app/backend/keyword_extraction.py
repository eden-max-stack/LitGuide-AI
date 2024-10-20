import nltk
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import math
import numpy as np

# cleaning data

def clean(text):
    text = text.lower()
    printable = set(string.printable)
    text = filter(lambda x: x in printable, text) #filter funny characters, if any.
    return text

# POS tagging data

def pos_tagging(text):
  POS_tag = nltk.pos_tag(text)

  print(f"Tokenized Text with POS tags: {POS_tag}")

# lemmatization

wordnet_lemmatizer = WordNetLemmatizer()

adjective_tags = ['JJ','JJR','JJS']

lemmatized_text = []

def POS_tagging(POS_tag):
  for word in POS_tag:
      if word[1] in adjective_tags:
          lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0],pos="a")))
      else:
          lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0]))) #default POS = noun
          
      print(f"Text tokens after lemmatization of adjectives and nouns: {lemmatized_text}")

# POS based filtering

stopwords = []

wanted_POS = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS','VBG','FW'] 

def POS_filtering(POS_tag):
  for word in POS_tag:
    if word[1] not in wanted_POS:
        stopwords.append(word[0])

  punctuations = list(str(string.punctuation))

  stopwords = stopwords + punctuations

# complete stopword generation

stopword_file = open("/content/drive/MyDrive/Colab Notebooks/long_stopwords.txt", "r")

lots_of_stopwords = []
for line in stopword_file.readlines():
  lots_of_stopwords.append(str(line.strip()))


lots_of_stopwords += stopwords

# removing stopwords

processed_text = []

def remove_stopwords(lemmatized_text):
  for word in lemmatized_text:
    if word not in lots_of_stopwords:
      processed_text.append(word)

processed_text = set(processed_text)
print(processed_text)

# building graph

import math

def build_graph(vocab):

  vocab_len = len(vocab)
  weighted_edge = np.zeros((vocab_len,vocab_len),dtype=np.float32)

  score = np.zeros((vocab_len),dtype=np.float32)
  window_size = 3
  covered_coocurrences = []

  for i in range(0,vocab_len):
      score[i]=1
      for j in range(0,vocab_len):
          if j==i:
              weighted_edge[i][j]=0
          else:
              for window_start in range(0,(len(processed_text)-window_size+1)):
                  
                  window_end = window_start+window_size
                  
                  window = processed_text[window_start:window_end]
                  
                  if (vocab[i] in window) and (vocab[j] in window):
                      
                      index_of_i = window_start + window.index(vocab[i])
                      index_of_j = window_start + window.index(vocab[j])
                      
                      # index_of_x is the absolute position of the xth term in the window 
                      # (counting from 0) 
                      # in the processed_text
                        
                      if [index_of_i,index_of_j] not in covered_coocurrences:
                          weighted_edge[i][j]+=1/math.fabs(index_of_i-index_of_j)
                          covered_coocurrences.append([index_of_i,index_of_j])


  # calculating weighted sum
  inout = np.zeros((vocab_len),dtype=np.float32)

  for i in range(0,vocab_len):
      for j in range(0,vocab_len):
          inout[i]+=weighted_edge[i][j]

  print(inout)

  # scoring vertices

  MAX_ITERATIONS = 50
  d=0.85
  threshold = 0.0001 #convergence threshold

  for iter in range(0,MAX_ITERATIONS):
      prev_score = np.copy(score)
      
      for i in range(0,vocab_len):
          
          summation = 0
          for j in range(0,vocab_len):
              if weighted_edge[i][j] != 0:
                  summation += (weighted_edge[i][j]/inout[j])*score[j]
                  
          score[i] = (1-d) + d*(summation)
      
      if np.sum(np.fabs(prev_score-score)) <= threshold: #convergence condition
          print(f"Converging at iteration {iter}....")
          break

  for i in range(0,vocab_len):
    print(f"Score of {vocab[i]} : {score[i]}")