from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Any
from pathlib import Path
from app.recomendation.song_analize import get_song
from fastapi.responses import JSONResponse
from app.recomendation.neural import neural
from app.recomendation.new_parameters import new_song

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")


# main site to enter artist and song name
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request) -> Any:
    return templates.TemplateResponse("main.html", {"request": request})


# if user enter bad values back to the main site
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request, song: str = Form(None), artist: str = Form(None)  # noqa: B008
) -> Any:
    if song is None or artist is None:
        text = "You have to enter both values"
        return templates.TemplateResponse(
            "main.html", {"request": request, "text": text}
        )
    error = get_song(song, artist)
    # get_cong dont return values, so if return someting this is expected error
    if error is None:
        neural()
        return templates.TemplateResponse(
            "genres.html", {"request": request, "song": song, "artist": artist}
        )
    return templates.TemplateResponse("main.html", {"request": request, "error": error})


# creating buttons with genres to choose
@app.get("/genre")
async def get_genres() -> JSONResponse:
    file_path = Path("app/data/genres/genres.txt")
    with file_path.open(mode="r") as f:
        genres = f.read().splitlines()
    return JSONResponse(content=genres)


# reads buttons like a form and returns new songs
@app.post("/genre", response_class=HTMLResponse)
async def submit_genres(request: Request, genre: str = Form(...)) -> Any:  # noqa: B008
    results = new_song(genre)
    print(results)
    return templates.TemplateResponse(
        "result.html", {"request": request, "results": results}
    )
