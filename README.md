# Aplikacja-do-polecania-muzyki

![GitHub forks](https://img.shields.io/badge/Version-1.0.1-red)

Interface in Polish lang

instalacja bibliotek:

pip install -r requirements.txt

Wymagane api keye znajdują się w pliku .env.example należy utworzyć plik .env i podać tam swoje klucze według wzoru

Opis:
Znajduje piosenkę o podobnym brzmieniu na podstawie takich danych jak tempo nastrój energia itd
polecenie_muzyki to główna aplikacja która uruchamia trzy mniejsze

Aplikacja song_analize pobiera od użytkownika nazwę oraz autora piosenki a nastęnie pobiera ze spotify i zapisuje informacje o piosence do pliku results.json

Aplikacja AI to prosta sieć neuronowa która pobiera parametry z wynik2.json, przetwarza dane i zapisuje do pliku results2.json dane piosenki która według niej jest podobna do pobranej

Aplikacja new_parameters pobiera dane z pliku wynik3.json, prosi użytkownika o wybranie gatunku piosenki z tych które znajdują się na liście, wysyła dane do spotify o wymaganiach utworu i następnie sciąga nam odpowiednią piosenkę

Podany gatunek nie musi się równać gatunkowi piosenki którą podaliśmy wcześniej! Jeśli podamy inny gatunek to dostaniemy piosenkę brzmiącą podobnie do orginału w tym gatunku który podaliśmy na koniec.

Tests zawiera test który sprawdza czy gatunki na liscie gatunki.txt rzeczywiście istnieją na spotify. Jeśli brakuje tam twojego ulubionego można go dopisać a następnie uruchomić test.
  

Aby zbudować obraz Docker zakładając, że Dockerfile znajduje się z resztą plików jak w repozytorium należy wpisać:

docker build -t main .

gdzie main można zmienić według własnych preferencji

Następnie aby uruchomić kontener:

docker run -it --env-file .env main

Zakładając, że w pliku .env są prawidłowe wartości i znajduje się z resztą plików jak w repozytorium plik .env.example

flaga -it pozwoli na wprowadzanie danych z konsoli w ktorej kontener zostanie uruchomiony 

