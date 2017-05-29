import numpy as np
import pandas as pd

from last_fm import user_history
from spotify import track_details
from genius import filter
import math

dictionary = {}


def build_features():
    top_tracks = user_history.get_top_tracks()
    track_ids = track_details.get_track_info(top_tracks)
    track_features = track_details.get_audio_features(track_ids)
    track_features = np.around(track_features, decimals=5)
    sadness = filter.get_all_sadness(top_tracks)
    print track_features.shape, sadness.shape
    track_features = np.hstack((track_features, sadness))

    for i in range(0, len(top_tracks)):
        dictionary[top_tracks[i][0]] = track_features[i]

    pd.DataFrame(track_features).to_csv("features.csv", sep=",")


def compute_gloominess():
    df = pd.read_csv("features.csv")
    old_df = df.drop(df.columns[[4, 5, 6, 7]], axis=1)
    new_df = df.drop(df.columns[[0, 1, 2, 3]], axis=1)
    matrix = new_df.as_matrix()
    gloom = []
    for row in matrix:
        lyrical_density = row[3] * 1000 / row[1]

        gloom.append(((1 - row[0]) + (row[2] * (1 + lyrical_density))) / 2)
    old_df.drop(df.columns[0], axis=1, inplace=True)
    old_df[3] = np.array(gloom).reshape(len(gloom), 1)
    return np.sum(old_df.as_matrix(), axis=0)


def compute_closeness(a, b):
    distance = 0
    for i in range(0, len(a)):
        distance += math.pow(a[i] - b[i], 2)

    distance = math.sqrt(distance)
    total_distance = 3 * math.pow(50, 2) + math.pow(max(a[len(a) - 1], b[len(a) - 1]), 2)
    total_distance = math.sqrt(total_distance)
    return 1 - (distance / total_distance)


# build_features()
print compute_gloominess()
