import base64
import requests
import os
from dotenv import load_dotenv
from requests.models import Response


# polaczenie z api spotify
def conn() -> Response:
    load_dotenv()
    client_id = os.getenv("SPOTIFY_ID")
    client_secret = os.getenv("SPOTIFY_SECRET")

    # polaczenie ze spotify
    token_url = "https://accounts.spotify.com/api/token"  # noqa: S105
    token_data = {"grant_type": "client_credentials"}
    token_headers = {
        "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}"  # noqa: E501 # type: ignore
    }
    return requests.post(  # noqa: S113
        token_url, data=token_data, headers=token_headers
    )
