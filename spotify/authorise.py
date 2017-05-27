from requests_oauthlib import OAuth2Session
import requests
import json
import config

client_id = config.spotify_client_id
client_secret = config.spotify_client_secret
token_url = 'https://accounts.spotify.com/api/token'
redirect_uri = 'https://abhirame.github.io'
scope = ['user-top-read']
oauth = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)


def authorise():
    authorization_url, state = oauth.authorization_url(url='https://accounts.spotify.com/authorize')

    print 'Please go to %s and authorize access.' % authorization_url
    authorization_response = raw_input('Enter the full callback URL')

    oauth.fetch_token(token_url=token_url, authorization_response=authorization_response,
                      client_secret=client_secret)

    with open('access_tokens.txt', 'w') as f:
        f.write(oauth.token['access_token'])

    with open('refresh_tokens.txt', 'w') as f:
        f.write(oauth.token['refresh_token'])


def refresh_token(access_token, refresh_token):
    print access_token

    data = {'grant_type': 'refresh_token',
              'refresh_token': refresh_token}
    url = 'https://accounts.spotify.com/api/token'
    response = requests.post(url=url, headers={'Authorization': 'Basic '+access_token}, data=data).json()
    print response
    with open('access_tokens.txt', 'w') as f:
        f.write(response['access_token'])
