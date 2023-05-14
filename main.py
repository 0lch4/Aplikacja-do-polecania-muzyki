from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#utworzenie aplikacji
app = FastAPI()

#polaczenie z katalogiem z widokami
templates = Jinja2Templates(directory="templates")

#polaczenie ze stylami
app.mount("/static", StaticFiles(directory="static"), name="static")

#widok glowny ktory wyswietla sie pod adresem strony
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, songs: str = Form(...)):
     return templates.TemplateResponse("genres.html", {"request": request, "songs": songs})
        