import requests
import pytest
from conn import conn
from fastapi.testclient import TestClient

response = conn()

headers = {
    "Authorization": f"Bearer {response.json()['access_token']}",
    "Content-Type": "application/json",
}

with open("genres.txt") as f:
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
    ), f"Nie udało się uzyskać wyników wyszukiwania dla gatunku {genre}. Kod statusu: {response.status_code}"
    results = response.json()["tracks"]
    assert len(results) > 0, f" {genre} nie jest gatunkiem obsługiwanym na spotify"


def test_submit_form() -> None:
    from main import app

    client = TestClient(app)

    response = client.post("/submit", data={"song": "alicja", "artist": "szpaku"})
    assert response.status_code == 200
    assert "genres.html" in response.template.name # type: ignore

    response2 = client.post(
        "/submit", data={"song": "alefwqjikekcqwja", "artist": "szpafqwlslwkqku"}
    )
    assert "Nie ma takiego utworu na spotify" in response2.text

    response3 = client.post("/submit", data={"song": "", "artist": "szpaku"})
    assert "Musisz wprowadzić obie wartości" in response3.text


def test_submit_genres() -> None:
    from main import app

    client = TestClient(app)

    response = client.post("/genre", data={"genre": genres})
    assert response.status_code == 200
    assert "Utwór" in response.text
    assert "Wykonawca" in response.text
    assert "Link do utworu" in response.text
