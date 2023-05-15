import base64
import requests
import os
from dotenv import load_dotenv
def conn():
    load_dotenv()
    client_id = os.getenv('SPOTIFY_ID')
    client_secret = os.getenv('SPOTIFY_SECRET')

    #polaczenie ze spotify
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials"}
    token_headers = {
        "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"}
    response = requests.post(token_url, data=token_data, headers=token_headers)
    return response