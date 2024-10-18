import pandas as pd
from keyphrase_vectorizers import KeyphraseCountVectorizer
from tqdm.auto import tqdm
import textacy
from textacy.extract.keyterms import scake
from datasets import load_dataset
import numpy as np
from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer
from transformers import DataCollatorForTokenClassification
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
import torch
import json

# keyword extraction using scake

# %%
with open('sampleText.txt', 'r') as file:
  data = file.readlines()

print(data)

# %%
scake_keywords_dict = dict()
for line in data:
  scake_keywords_dict[line] = list()

# %%
for text in tqdm(data):
    doc = textacy.make_spacy_doc(text, lang='en_core_web_sm')
    doc_str = str(doc)
    keywords_with_scores = scake(doc, normalize='lower', topn=10)
    keywords = ', '.join([kw[0] for kw in keywords_with_scores])
    scake_keywords_dict[doc_str] = keywords

# %%
scake_keywords_df = pd.DataFrame(list(scake_keywords_dict.items()), columns=["text", "keywords"])
scake_keywords_df.head()