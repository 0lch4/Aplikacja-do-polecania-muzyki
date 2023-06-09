import requests
import json
from conn import conn
from typing import Any


def new_song(genre: str) -> Any:
    response = conn()
    genre = genre.lower()
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        with open("results2.json") as f:
            new_data = json.load(f)

        tempo = new_data["tempo"]
        loudness = new_data["loudness"]
        valence = new_data["valence"]
        energy = new_data["energy"]
        time_signature = new_data["time_signature"]
        mode = new_data["mode"]
        key = new_data["key"]
        danceability = new_data["danceability"]
        speechiness = new_data["speechiness"]
        instrumentalness = new_data["instrumentalness"]
        popularity = new_data["popularity"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        params = {
            "limit": 3,
            "market": "PL",
            "q": "lang:pl",
            "seed_genres": genre,
            "target_tempo": tempo,
            "target_loudness": loudness,
            "target_valence": valence,
            "target_energy": energy,
            "target_time_signature": time_signature,
            "mode": mode,
            "key": key,
            "danceability": danceability,
            "speechiness": speechiness,
            "instrumentalness": instrumentalness,
            "popularity": popularity,
            "type": "track",
        }
        response = requests.get(  # noqa: S113
            "https://api.spotify.com/v1/recommendations",
            headers=headers,
            params=params,
            verify=True,
        )
        if response.status_code == 200:
            results = response.json()["tracks"]
            if len(results) == 0:
                return "Nie znaleziono utworów o podanych parametrach"
        else:
            return "Błąd połączenia"
    else:
        return "Błąd połączenia"

    return results
