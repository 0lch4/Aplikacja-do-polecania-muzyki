import os
import requests
import base64
import json

# wpisz tutaj zmienne srodowiskowe ktore przechowuja id klienta i sekret na api spotify
client_id = os.environ.get('Spotify_client_id')
client_secret = os.environ.get('Spotify_client_secret')

token_url = "https://accounts.spotify.com/api/token"
token_data = {
    "grant_type": "client_credentials"}
token_headers = {
    "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"}

response = requests.post(token_url, data=token_data, headers=token_headers)

if response.status_code == 200:
    access_token = response.json()['access_token']
    with open('wynik2.json') as f:
        new_data = json.load(f)
       
    tempo = new_data['tempo']
    loudness = new_data['loudness']
    valence = new_data['valence']
    energy = new_data['energy']
    time_signature = new_data['time_signature']

    headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"}

    params = {
        'q': f'tempo:{tempo} AND loudness:{loudness} AND valence:{valence} AND energy:{energy} AND time_signature:{time_signature}',
        'type': 'track',
        'limit': 1  }
    
    response = requests.get("https://api.spotify.com/v1/", headers=headers, params=params,verify=True)
    print(response.url)
    if response.status_code == 200:
        results = response.json()['tracks']['items']
        if len(results) == 0:
            print("Nie znaleziono utworów dla podanych parametrów wyszukiwania.")
        else:
            for track in results:
                print(f"Utwór: {track['name']}")
                print(f"Wykonawca: {track['artists'][0]['name']}")
                print(f"Link do utworu: {track['external_urls']['spotify']}")
    else:
        print(f"Nie udało się uzyskać wyników wyszukiwania. Kod statusu: {response.status_code}")
print(response.json())
