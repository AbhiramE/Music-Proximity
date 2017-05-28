import numpy as np

from last_fm import user_history
from spotify import track_details
from genius import filter


def build_features():
    top_tracks = user_history.get_top_tracks()
    track_ids = track_details.get_track_info(top_tracks)
    track_features = track_details.get_audio_features(track_ids)
    track_features = np.around(track_features, decimals=5)
    sadness = filter.get_all_sadness(top_tracks)
    print track_features.shape, sadness.shape
    track_features = np.hstack((track_features, sadness.reshape(len(sadness), 1)))
    print track_features
    np.savetxt("features.csv", track_features, delimiter=",")


build_features()
