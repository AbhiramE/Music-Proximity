import numpy as np
import pandas
import user_history
import track_details


def build_features():
    top_tracks = user_history.get_top_tracks()
    track_ids = track_details.get_track_info(top_tracks)
    track_features = track_details.get_audio_features(track_ids)
    track_features = np.around(track_features, decimals=5)
    np.savetxt("features.csv", track_features, delimiter=",")

build_features()