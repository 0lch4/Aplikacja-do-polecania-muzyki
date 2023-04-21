#nie ma zwiazku z reszta zrobilem testowo

import requests
import json
import html
import os

# podaj tutaj swoja zmienna srodowiskowa ktora przechowuje api yt
api_key = os.environ.get('YouTube_api_key')

url = 'https://www.googleapis.com/youtube/v3/search'

tytul = input("podaj nazwe piosenki")
params = {
    'q': tytul,
    'key': api_key,
    'type': 'music',
    'part': 'id,snippet'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    with open('wynik.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open('wynik.json', 'r', encoding='utf-8') as f:
        plik = f.read()
        for line in plik.splitlines():
            if line.strip().startswith('"title":'):
                line = line.strip()[9:]
                line = line.strip()[1:-2]
                line = html.unescape(line)
                print(line)
                break
else:
    print(f'Błąd {response.status_code}: {response.reason}')
