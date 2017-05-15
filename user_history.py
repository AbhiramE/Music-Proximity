from requests_oauthlib import OAuth2Session
import authorise
import requests
import json


redirect_uri = 'https://abhirame.github.io'


def get_top_tracks():
    params = {
        'user': 'Abhis3798',
        'api_key': api_key,
        'format': 'json',
    }

    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks'
    tracks = requests.get(url, params=params).json()['toptracks']['track']

    track_names = []
    for track in tracks:
        track_names.append([track['name'].encode('utf-8'),track['artist']['name'].encode('utf-8')])

    return track_names
