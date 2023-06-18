import requests
import json
from app.connection.conn import conn
from typing import Any
from pathlib import Path


def new_song(genre: str) -> Any:
    response = conn()
    genre = genre.lower()
    if response.status_code != 200:
        return f"Error: {response.status_code}"

    access_token = response.json()["access_token"]
    file_path = Path("app/data/results/new_results.json")
    with file_path.open(mode="r") as f:
        new_data = json.load(f)

    tempo = new_data["tempo"]
    valence = new_data["valence"]
    loudness = new_data["loudness"]
    energy = new_data["energy"]
    danceability = new_data["danceability"]
    speechiness = new_data["speechiness"]
    time_signature = new_data["time_signature"]
    mode = new_data["mode"]
    key = new_data["key"]
    instrumentalness = new_data["instrumentalness"]
    popularity = new_data["popularity"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # trying find matching songs
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
        if not results:
            return "No songs matching for these parameters"

        return results

    return f"Error: {response.status_code}"
