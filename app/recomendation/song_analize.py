import requests
import json
from app.connection.conn import conn
from pathlib import Path


def get_song(title: str, artist: str) -> str | None:
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

        if response.status_code != 200:
            return f"Can't connect to Spotify Error code:{response.status_code}"
        data = response.json()

        if not data["tracks"]["items"]:
            return "This song does not exist on Spotify"

        track_id = data["tracks"]["items"][0]["id"]
        features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        popularity_url = f"https://api.spotify.com/v1/tracks/{track_id}"
        response = requests.get(features_url, headers=headers)  # noqa: S113
        popularity_response = requests.get(  # noqa: S113
            popularity_url, headers=headers
        )
        # gets song parameters and saves it to json file
        data = response.json()
        popularity_data = popularity_response.json()
        file_path = Path("app/data/results/old_results.json")
        with file_path.open(mode="w", encoding="utf-8") as f:
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

    return f"Can't get replay from Spotify:{response.status_code}"
