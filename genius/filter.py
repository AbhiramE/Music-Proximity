import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

ps = PorterStemmer()


def filter_words():
    f = open('word_emotions.txt', 'r')
    lines = f.readlines()
    sad_words = []
    for line in lines:
        words = line.strip('\n').split('\t')
        # print words
        if 'sadness' in words and words[2] == str(1):
            sad_words.append(words[0])
    pd.DataFrame(np.array(sad_words)).to_csv('sad_words.csv', sep=',')


def get_sadness_ratio(lyrics):
    filtered_words = [word for word in lyrics if word not in stopwords.words('english')]

    # Read Sad Words
    df = pd.read_csv('sad_words.csv')
    df = df.drop(df.columns[[0]], axis=1)
    sad_words = df.as_matrix().reshape(1, len(df))[0]

    stemmed_words = [ps.stem(word).encode('utf-8') for word in filtered_words]
    sad_words = [ps.stem(word).encode('utf-8') for word in sad_words]

    sad_count = 0
    for word in stemmed_words:
        if word in sad_words:
            sad_count += 1
    return float(sad_count)/len(stemmed_words)


print get_sadness_ratio(['absent', 'so', 'low', 'get', 'bad', 'kill', 'cry'])
# filter_words()
