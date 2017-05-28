# coding=utf-8
import urllib

import numpy as np
import requests
import config
import authorise

client_id = config.spotify_client_id
token_url = 'https://accounts.spotify.com/api/token'
scope = ['user-top-read']
redirect_uri = 'https://abhirame.github.io'


def get_access_token():
    f = open('access_tokens.txt', 'r')
    line = f.readline()
    if line is not None:
        return line.strip('\n')
    else:
        authorise.authorise()
        get_access_token()


def get_refresh_token():
    f = open('refresh_tokens.txt', 'r')
    line = f.readline()
    if line is not None:
        return line.strip('\n')


def refresh_token():
    authorise.refresh_token(get_access_token(), get_refresh_token())


def get_user_info():
    response = requests.get(url='https://api.spotify.com/v1/me',
                            headers={'Authorization': 'Bearer ' + get_access_token()})
    if response.status_code != 200:
        refresh_token()
        response = requests.get(url='https://api.spotify.com/v1/me',
                                headers={'Authorization': 'Bearer ' + get_access_token()})

    return response.json()


def get_track_info(track_names):
    url = 'https://api.spotify.com/v1/search'
    track_ids = []
    print track_names
    for track_name in track_names:
        name = track_name[0].split('(')[0].replace('\'', '').replace('\"', "").replace('’', '')
        params = {
            'q': urllib.quote_plus(name),
            'type': 'track'
        }
        results = requests.get(url=url, params=params).json()['tracks']['items']
        if len(results) > 0:
            track_ids.append(results[0]['id'])
        else:
            print name
    return track_ids


def get_audio_features(track_ids):
    url = 'https://api.spotify.com/v1/audio-features'
    params = {'ids': ",".join(track_ids)}
    response = requests.get(url=url,
                            headers={'Authorization': 'Bearer ' + get_access_token()},
                            params=params)

    if response.status_code != 200:
        refresh_token()
        get_audio_features(track_ids)

    print response.json()
    track_features = []
    tracks = response.json()['audio_features']

    for track in tracks:
        track_features.append(np.array([track['danceability'], track['energy'], track['acousticness'],
                                        track['valence']]))

    return np.array(track_features)
