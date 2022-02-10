import pandas as pd
import glob
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.stem import PorterStemmer
import spacy
import re
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

nltk.download('punkt')
nlp = spacy.load('en_core_web_sm')

# finding all the data files
files = glob.glob('data[0-9].*csv')

opened = []

# reading and merging into one dataframe
for file in files:
    df = pd.read_csv(file, header=0, index_col=None, sep=',')
    opened.append(df)

frame = pd.concat(opened, axis=0, ignore_index=True)
del frame['Unnamed: 0']
frame.summary = frame.summary.astype(str)


def tokenize(df):
    """
    word/sentence tokenization
    :param df: input dataframe
    :return: returns df
"""
    df['tokenized_words'] = df.apply(lambda row: word_tokenize(row['summary'].lower()), axis=1)
    df['tokenized_sents'] = df.apply(lambda row: sent_tokenize(row['summary'].lower()), axis=1)
    return df


def stem_lemm(df):
    """
    stemming/lemmatization
    :param df: df with string 
    :return:df with stemming and lemmatizarion
    """
    ps = PorterStemmer()
    df['stemming'] = df['tokenized_words'].apply(lambda x: [ps.stem(y) for y in x])
    df['lemmatization'] = df['summary'].apply(lambda x: [y.lemma_ for y in nlp(x)])
    return df


def no_punc(df):
    """
    removing punctuation
    :param df: dataframe to remove punctuation
    :return: df
    """
    lemma_punc = []
    nlp = English()
    for i in df.lemmatization:
        text = ' '.join(i)
        text = text.lower()
        #  "nlp" Object is used to create documents with linguistic annotations.
        my_doc = nlp(text)
        token_list = []
        for token in my_doc:
            token_list.append(token.text)
        filtered_sentence = []
        for word in token_list:
            lexeme = nlp.vocab[word]
            if not lexeme.is_stop:
                filtered_sentence.append(word)
        punc = ' '.join(filtered_sentence)
        punc = re.sub(r"[\[\]();/',%$|\\:?—&\"!]|(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)", '', punc)
        lemma_punc.append(punc)
    df['lemma_punc'] = lemma_punc
    return df


frame = tokenize(frame)
frame = stem_lemm(frame)
frame = no_punc(frame)

print(frame)
# Give the filename you wish to save the file to
filename = 'preprocessed.csv'

# Use this function to search for any files which match your filename
files_present = glob.glob(filename)

if not files_present:
    frame.to_csv(filename, encoding="utf-8", header=True, sep=',')
    print(filename, "file saved successfully")
else:
    print('WARNING: This file already exists!')
