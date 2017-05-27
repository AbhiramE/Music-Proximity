import numpy as np

from last_fm import user_history
from spotify import track_details
from genius import filter


def build_features():
    top_tracks = user_history.get_top_tracks()
    track_ids = track_details.get_track_info(top_tracks)
    track_features = track_details.get_audio_features(track_ids)
    track_features = np.around(track_features, decimals=5)
    filter.get_all_sadness(top_tracks)
    np.savetxt("features.csv", track_features, delimiter=",")

build_features()