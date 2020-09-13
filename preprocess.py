import numpy as np
import pandas as pd
import pickle
import MeCab
import neologdn
import itertools
import emoji
import re
import sys
import os
from constant import *
from collections import Counter


#---------------------------------------------------------------
# eliminate emoji and some noises
#---------------------------------------------------------------
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')
def normalize(tweets):
    normalized_tweets = []
    for tweet in tweets:
        normalized_tweets.append(neologdn.normalize(tweet))
    return normalized_tweets

def eliminate_emoji(tweets):
    tweets_without_emoji = []
    for tweet in tweets:
        tweet.translate(non_bmp_map)
        tweets_without_emoji.append(''.join(['' if c in emoji.UNICODE_EMOJI else c for c in tweet]))
    return tweets_without_emoji

def eliminate_noise(tweets):
    tweets_without_noise = []
    for tweet in tweets:
        tweet = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "", tweet)
        tweet = re.sub(r"　", " ", tweet)
        tweets_without_noise.append(tweet)
    return tweets_without_noise

def clean(tweets):
    cleaned_tweets = eliminate_emoji(tweets)
    cleaned_tweets = normalize(cleaned_tweets)
    cleaned_tweets = eliminate_noise(cleaned_tweets)
    return cleaned_tweets


#---------------------------------------------------------------
# digitize tweets to train
#---------------------------------------------------------------
# split tweets using neologd
def split_word(tagger, t):
    tagger.parse("")
    words = tagger.parse(t).split(" ")
    return words

# padding
def padding(tweets):
    padded_tweets = []
    for i in range(len(tweets)):
        t = tweets[i]
        if len(t) > MAX_LENGTH_OF_TWEETS:
            padded_tweets.append(t[0:MAX_LENGTH_OF_TWEETS])
        else:
            padded_tweets.append(t + ["<PAD/>"] * (MAX_LENGTH_OF_TWEETS - len(t)))
    return padded_tweets

# digitization
def tweets_digitization_to_train(tweets):
    mt = MeCab.Tagger("-Owakati -d " + MECAB_DICT_PATH)
    tweets = [split_word(mt, t) for t in tweets]
    tweets = padding(tweets)

    ctr = Counter(itertools.chain(*tweets))
    dictionaries = [c[0] for c in ctr.most_common() if c[1] > 2]
    dictionaries_inv = {c:i for i,c in enumerate(dictionaries)}
    vocab_size = len(dictionaries)+1
    
    data = []
    for t in tweets:
        words = []
        for w in t:
            try:
                words.append(dictionaries_inv[w])
            except KeyError:
                words.append(len(dictionaries))
        data.append(words)

    data = np.array(data)

    with open(VOCAB_DICT_PATH, "wb") as f:
        pickle.dump(dictionaries, f)
    
    return data, vocab_size

#---------------------------------------------------------------
# digitize tweets to predict using the above dictionary
#---------------------------------------------------------------
def tweets_digitization_to_predict(tweets):
    mt = MeCab.Tagger("-Owakati -d " + MECAB_DICT_PATH)
    tweets = clean(tweets)
    tweets = [split_word(mt, t) for t in tweets]
    tweets = padding(tweets)

    f = open(VOCAB_DICT_PATH, "rb")
    dictionaries = pickle.load(f)
    f.close()
    dictionaries_inv = {c:i for i,c in enumerate(dictionaries)}
    data = []
    for t in tweets:
        word = []
        for w in t:
            try:
                word.append(dictionaries_inv[w])
            except KeyError:
                word.append(len(dictionaries))
        data.append(word)

    data = np.array(data)

    return data


#---------------------------------------------------------------
# load data with labels from other scripts
#---------------------------------------------------------------
def load_data_with_labels(pklname):
    df = pickle.load(open(pklname, "rb"))
    tweets = df["tweet"].values
    tweets = clean(tweets)
    tweets, vocab_size = tweets_digitization_to_train(tweets)
    tweets = tweets.astype(np.float32)
    labels = np.array(df["label"].values).astype(np.float32)
    return tweets, labels, vocab_size

