import requests
import pytest
from pathlib import Path
from app.connection.conn import conn
from fastapi.testclient import TestClient

response = conn()

headers = {
    "Authorization": f"Bearer {response.json()['access_token']}",
    "Content-Type": "application/json",
}

file_path = Path("app/data/genres/genres.txt")
with file_path.open(mode="r") as f:
    genres = [genre.strip().lower() for genre in f]


@pytest.mark.parametrize("genre", genres)
def test_recommendations(genre: str) -> None:
    params = {
        "limit": 1,
        "market": "PL",
        "seed_genres": genre,
        "target_tempo": 120,
        "target_loudness": -5,
        "target_valence": 0.5,
        "target_energy": 0.5,
        "target_time_signature": 4,
        "mode": "minor",
        "type": "track",
    }

    response = requests.get(  # noqa: S113
        "https://api.spotify.com/v1/recommendations",
        headers=headers,
        params=params,
        verify=True,
    )
    assert (
        response.status_code == 200
    ), f"Genre not found: {genre}. Error: {response.status_code}"
    results = response.json()["tracks"]
    assert len(results) > 0, f" {genre} is not supported by Spotify"


def test_submit_form() -> None:
    from app.main import app

    client = TestClient(app)

    response = client.post("/submit", data={"song": "alicja", "artist": "szpaku"})
    assert response.status_code == 200
    assert "genres.html" in response.template.name  # type: ignore

    response2 = client.post(
        "/submit", data={"song": "alefwqjikekcqwja", "artist": "szpafqwlslwkqku"}
    )
    assert "This song does not exist on Spotify" in response2.text

    response3 = client.post("/submit", data={"song": "", "artist": "szpaku"})
    assert "You have to enter both values" in response3.text


def test_submit_genres() -> None:
    from app.main import app

    client = TestClient(app)

    response = client.post("/genre", data={"genre": genres})
    assert response.status_code == 200
    assert "Song" in response.text
    assert "Artist" in response.text
    assert "Link to the song on Spotify" in response.text
