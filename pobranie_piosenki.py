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
    print("Witaj :) podaj mi utwor a podam ci inny o podobnym brzmieniu")
    while True:
        title = input("Podaj tytuł piosenki: ")
        artist = input("Podaj wykonawcę: ")
        query = f"track:{title} artist:{artist}"
        search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"}
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if len(data['tracks']['items']) == 0:
                print("Nie widze takiego utworu spróbuj jeszcze raz :)")
            else:
                track_id = data['tracks']['items'][0]['id']
                features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
                response = requests.get(features_url, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    with open('wynik2.json', 'w', encoding='utf-8') as f:
                        json.dump({'tempo': data['tempo'], 'valence': data['valence'], 'loudness': data['loudness'], 'energy': data['energy'],
                                  'time_signature': data['time_signature'], 'mode': data['mode'],'key':data['key'] }, f, indent=2, ensure_ascii=False)
                    break
                else:
                    print(f"Błąd {response.status_code}: {response.reason}")
                    break
        else:
            print(f"Błąd {response.status_code}: {response.reason}")
            break
else:
    print(f"Błąd {response.status_code}: {response.reason}")