import requests
import json
from conn import conn

#pyta uzytkownika o utwor ktorego nazwa jest wysylana w żądaniu, w przypadku bledu informuje o tym co jest nie tak
def get_song(title,artist):
    response=conn()
    if response.status_code == 200:
        access_token = response.json()['access_token']
        
        query = f"track:{title} artist:{artist}"
        search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"}
        response = requests.get(search_url, headers=headers)
        #sprawdza czy piosenka istnieje na spotify
        if response.status_code == 200:
            data = response.json()
            if len(data['tracks']['items']) == 0:
                return "Nie ma takiego utworu na spotify"
            else:
                #wysyla żądanie o dane utworu
                track_id = data['tracks']['items'][0]['id']
                features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
                popularity_url = f"https://api.spotify.com/v1/tracks/{track_id}"
                response = requests.get(features_url, headers=headers)
                popularity_response = requests.get(popularity_url, headers=headers)
                #pobiera właściwości piosenki i zapisuje do pliku wynik2.json
                data = response.json()
                popularity_data = popularity_response.json()
                with open('results.json', 'w', encoding='utf-8') as f:
                    json.dump({'tempo': data['tempo'], 'valence': data['valence'], 'loudness': data['loudness'], 'energy': data['energy'],
                            'time_signature': data['time_signature'], 'mode': data['mode'], 'key': data['key'], 'danceability': data['danceability'],
                            'speechiness': data['speechiness'], 'instrumentalness': data['instrumentalness'], 'popularity': popularity_data['popularity']}, f, indent=2, ensure_ascii=False)
    
        else: 
            return "Nie ma takiego utworu na spotify"
    else:
        return "Blad polaczenia"
        
