# coding=utf-8
from genius import config
import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from BeautifulSoup import BeautifulSoup
import requests
import re

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
    print filtered_words
    # Read Sad Words
    df = pd.read_csv('/home/abhis3798/codebase/Projects/Sinder/genius/sad_words.csv')
    df = df.drop(df.columns[[0]], axis=1)
    sad_words = df.as_matrix().reshape(1, len(df))[0]

    stemmed_words = [ps.stem(word).encode('utf-8') for word in filtered_words]
    sad_words = [ps.stem(word).encode('utf-8') for word in sad_words]

    sad_count = 0
    for word in stemmed_words:
        if word in sad_words:
            sad_count += 1
    return float(sad_count) / len(stemmed_words)


def get_lyrics(track):
    url = 'http://genius.com/'
    track[0] = track[0].replace("-", "").replace('\xc3\xbc', 'u').replace("\xe2\x80\x99", "") \
        .replace("'", "")
    track[0] = ' '.join(track[0].split()).split("(")[0].rstrip('. ').replace(" ", "-")
    track[1] = track[1].replace("-", "").replace('\xc3\xbc', 'u').replace("\xe2\x80\x99", "") \
        .replace("'", "")
    track[1] = ' '.join(track[1].split()).split("(")[0].rstrip('. ').replace(" ", "-")
    url += track[1] + "-" + track[0] + "-" + "lyrics"
    print url

    page = requests.get(url)
    lyrics = ""
    if page.status_code == 200:
        html = BeautifulSoup(page.text)
        [h.extract() for h in html('script')]
        for a in html.find("div", {"class": "lyrics"}).findAll("p")[0].findAll("a"):
            lyrics += a.getText(separator=u' ').lower()
    return lyrics


def get_all_sadness(tracks):
    all_sadness = []
    for track in tracks:
        lyrics = get_lyrics(track)
        words = lyrics.split(" ")
        if lyrics != "":
            all_sadness.append(np.array([get_sadness_ratio(words), len(lyrics)]))
        else:
            all_sadness.append(np.array([0, len(lyrics)]))
    return np.array(all_sadness)
