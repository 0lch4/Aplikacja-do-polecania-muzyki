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

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Witaj :) podaj mi utwor a podam ci inny o podobnym brzmieniu")
    title = input("Podaj tytuł piosenki: ")
    artist = input("Podaj wykonawcę: ")
    query = f"track:{title} artist:{artist}"
    query = f"track:{title}"
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            track_id = data['tracks']['items'][0]['id']
        except:
            print(
                "Nie znalazlem takiej piosenki przykro mi, spróbuj ją wpisać inaczej:)")
            quit()
        features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        response = requests.get(features_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open('wynik2.json', 'w', encoding='utf-8') as f:
            json.dump({'tempo': data['tempo'], 'valence': data['valence'], 'loudness': data['loudness'], 'energy': data['energy'],
                      'time_signature': data['time_signature'], 'mode': data['mode']}, f, indent=2, ensure_ascii=False)

        if response.status_code == 200:
            data = response.json()
            print(f"Cechy piosenki '{title}':")
            print(f"Tempo: {data['tempo']}")
            print(f"Nastroj: {data['valence']}")
            print(f"Ogólna głośność: {data['loudness']}")
            print(f"time_signature: {data['time_signature']}")
            print(f"mode: {data['mode']}")
            print(f"Energia: {data['energy']}")
        else:
            print(f"Błąd {response.status_code}: {response.reason}")
    else:
        print(f"Błąd {response.status_code}: {response.reason}")
else:
    print(f"Błąd {response.status_code}: {response.reason}")
