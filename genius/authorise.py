from requests_oauthlib import OAuth2Session
import requests
import config

client_id = config.genius_client_id
client_secret = config.genius_secret_id
redirect_uri = 'https://abhirame.github.io'
token_url = 'https://api.genius.com/oauth/token'
scope = ['me']
oauth = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)


def authorise():
    authorization_url, state = oauth.authorization_url(url='https://api.genius.com/oauth/authorize')

    print 'Please go to %s and authorize access.' % authorization_url
    authorization_response = raw_input('Enter the full callback URL')

    oauth.fetch_token(token_url=token_url, authorization_response=authorization_response,
                      client_secret=client_secret)

    with open('access_tokens.txt', 'w') as f:
        print oauth.token['access_token']
        f.write(oauth.token['access_token'])


authorise()
