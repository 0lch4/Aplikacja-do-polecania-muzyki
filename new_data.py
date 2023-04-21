import os
import requests
import base64
import json

# wpisz tutaj zmienne srodowiskowe ktore przechowuja id klienta i sekret na api spotify
client_id = os.environ.get('Spotify_client_id')
client_secret = os.environ.get('Spotify_client_secret')

token_url = "https://accounts.spotify.com/api/token"
token_data = {
    "grant_type": "client_credentials"
}
token_headers = {
    "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"
}
response = requests.post(token_url, data=token_data, headers=token_headers)

with open('wynik2.json') as f:
    new_data = f.read()

if response.status_code == 200:
    access_token = response.json()['access_token']
    query =
    search_url = 'https://api.spotify.com/v1/audio-analysis/11dFghVXANMlKmJXsNCbNl'
    