import requests
import json
from conn import conn
from typing import Literal


def get_song(
    title: str, artist: str
) -> Literal["Nie ma takiego utworu na spotify", "Blad polaczenia"] | None:
    response = conn()
    if response.status_code == 200:
        access_token = response.json()["access_token"]

        query = f"track:{title} artist:{artist}"
        search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(search_url, headers=headers)  # noqa: S113
        # sprawdza czy piosenka istnieje na spotify
        if response.status_code == 200:
            data = response.json()
            if len(data["tracks"]["items"]) == 0:
                return "Nie ma takiego utworu na spotify"
            # wysyla żądanie o dane utworu
            track_id = data["tracks"]["items"][0]["id"]
            features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
            popularity_url = f"https://api.spotify.com/v1/tracks/{track_id}"
            response = requests.get(features_url, headers=headers)  # noqa: S113
            popularity_response = requests.get(
                popularity_url, headers=headers
            )  # noqa: S113, E501
            # pobiera właściwości piosenki i zapisuje do pliku wynik2.json
            data = response.json()
            popularity_data = popularity_response.json()
            with open("results.json", "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "tempo": data["tempo"],
                        "valence": data["valence"],
                        "loudness": data["loudness"],
                        "energy": data["energy"],
                        "time_signature": data["time_signature"],
                        "mode": data["mode"],
                        "key": data["key"],
                        "danceability": data["danceability"],
                        "speechiness": data["speechiness"],
                        "instrumentalness": data["instrumentalness"],
                        "popularity": popularity_data["popularity"],
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
                return None
        else:
            return "Nie ma takiego utworu na spotify"
    else:
        return "Blad polaczenia"
