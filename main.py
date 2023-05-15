from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from song_analize import get_song
from fastapi.responses import JSONResponse
from AI import neural
from new_parameters import new_song

#utworzenie aplikacji
app = FastAPI()

#polaczenie z katalogiem z widokami
templates = Jinja2Templates(directory="templates")

#polaczenie ze stylami
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, song: str = Form(None), artist: str=Form(None)):
    if song is None or artist is None:
        text = "Musisz wprowadzić obie wartości"
        return templates.TemplateResponse("main.html", {"request": request, "text":text})
    else:
        error = get_song(song,artist)
        if error==None:
            neural()
            return templates.TemplateResponse("genres.html", {"request": request, "song": song, "artist":artist})
        else:
            return templates.TemplateResponse("main.html", {"request": request, "error": error})
            

@app.get("/genre")
async def get_genres():
    with open('genres.txt', 'r') as f:
        genres = f.read().splitlines()
    return JSONResponse(content=genres)

@app.post("/genre", response_class=HTMLResponse)
async def submit_genres(request: Request,genre: str = Form(...)):
    results = new_song(genre)
    return templates.TemplateResponse("result.html",{"request": request, "results": results})