import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# read csv file
frame = pd.read_csv('preprocessed.csv', header=0, index_col=None, sep=',')
del frame['Unnamed: 0']


def word_count(df):
    """
    returns word count
    :param df: input dataframe
    :return: return a dataframe with word count
    """
    counter_list = []
    for i in frame['lemma_punc']:
        new_tokens = word_tokenize(str(i))
        counted = Counter(new_tokens)
        counter_list.append(counted)
    df['words_count'] = counter_list
    return df


def sent_count(df):
    """
    Sentence count
    :param df:dataframe
    :return:dataframe
    """
    counter_list = []
    for i in frame['lemma_punc']:
        sent_token = sent_tokenize(str(i))
        counts = len(sent_token)
        counter_list.append(counts)
    df['sent_counts'] = counter_list
    return df


def sentiment_analysis(df):
    """
    does sentiment analysis and returns dataframe with positive negative and neutral score (Vader Sentiment)
    :param df: dataframe
    :return: returns a dataframe with scores
    """
    pos = []
    neg = []
    neu = []
    for i in df['lemma_punc']:
        vs = analyzer.polarity_scores(str(i))
        pos.append(vs['pos'])
        neg.append(vs['neg'])
        neu.append(vs['neu'])
    df['positive_score'] = pos
    df['negative_score'] = neg
    df['neutral_score'] = neu
    return df


frame = word_count(frame)
frame = sent_count(frame)
frame = sentiment_analysis(frame)
print(frame['words_count'])
print(frame['sent_counts'])
frame.to_csv('fengineering.csv', encoding="utf-8", header=True, sep=',')
