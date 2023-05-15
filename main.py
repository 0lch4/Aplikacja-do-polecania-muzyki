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

#glowna strona z mozliwoscia wpisania artysty i utworu
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

"""strona obslugujaca formularz z glownej, jesli beda bledne dane strona glowa zostanie ponownie wczytana
a uzytkownik powiadomiony co zrobil zle"""
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, song: str = Form(None), artist: str=Form(None)):
    if song is None or artist is None:
        text = "Musisz wprowadzic obie wartosci"
        return templates.TemplateResponse("main.html", {"request": request, "text":text})
    else:
        error = get_song(song,artist)
        """funckaj get_song nic nie zwraca, wiec jesli zwroci jaki napis ktory powstaje po bledach,
        ktore przewidzialem to uzytkownik zostanie o tym poinformowany i bedzie mial
        nastepna szanse, w przeciwnym wypadku wczyta sie nastepna strona"""
        if error==None:
            #aktywacja sieci neuronowej z pliku AI
            neural()
            return templates.TemplateResponse("genres.html", {"request": request, "song": song, "artist":artist})
        else:
            return templates.TemplateResponse("main.html", {"request": request, "error": error})
            
#obsluguje stworzenie przyciskow z nazwami mozliwych gatunkow do wybrania
@app.get("/genre")
async def get_genres():
    with open('genres.txt', 'r') as f:
        genres = f.read().splitlines()
    return JSONResponse(content=genres)

"""z wybranego przycisku odczytuje jego nazwe jako formularz i zwraca nowe piosenki z aplikacji new songs
w przeciwienstwie do submit_form zwraca nazwy utworow wiec gdyby nie bylo takiego utworu uzytkownik
zostanie poinformowany za pomoca funkcji"""
@app.post("/genre", response_class=HTMLResponse)
async def submit_genres(request: Request,genre: str = Form(...)):
    results = new_song(genre)
    return templates.TemplateResponse("result.html",{"request": request, "results": results})
