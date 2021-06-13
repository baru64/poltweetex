# Twitter scrapper 
## Funkcje Front 
- słowo per sejm
- słowo per partia
- słowo per polityk
- ostatnie tweety z danym słowem ogólnie/polityk/partia

## Model Bazy
- party
  - name
  - logo
- politician
  - twitter id
  - last update
  - party id
- word
  - date
  - word
  - politician id
  - tweet id <---- Tylko dla dni ?
  - count
- wordindex - tabela przechowująca słowa, które wystąpiły chociaż raz
  - word

## Architecture 
- ściagamy dane polityka P z dnia D  > word
infra - azure:
- app service dla frontend
- lambda z timerem do ściągania wpisów polityków - wpisuje do db
- baza danych sql
- lambda per endpoint - ściąga dane z db


## Azure funkcje 

#### Ściąganie danych
-  Odpytuje bazę o wszystkie ID polityków
-  Ściagam ich najnowsze tweety (Czy tweety maja date? Jak tak to trzymac lastTT w bazie z ID polityka i analizowac tylko te pozniejsze)
 - Dziele tekst na pojedyncze slowa
    - Wywalam ze slow polskie znaki
    - Wywalam spókniki typu 'a','i' itp i wywalam znaki interpunkcyjne 
    - Dziele słowa na klucz wartosc wraz z sumowaniem duplikatów w jednym tt
    - Odpytuję bazę odnosnie kazdego słowa czy występuje ono  w tablei index word
        - Jezeli nie istnieje to dopisuje to słowo
        - Jeżeli istnieje to nic nie robie z tmy
    - Dopisuje każde słowo do tabeli word

Możliwe udoskonalenia 
- Zamiast wywoływać funkcji dla wszystkich polityków dodajemy funckję która ściąga wszystkie ID polityków i wywołuje po funkcję dla każdego pojedynczego ID. Ew. można by zrobić wersję z wywoływaniem funkcji dla kilku ID w zależności od częstotliwości dodawanie tweetów danego ID. 
    - Funkcja która wywołuje funkcje dla batchy Idków dostawała by wraz z nimi ilość twettów z ostatniego tygodnia (zakładamy że to może być średnia wartość) i wywołuje batch ID by ilość tweetów na przykłąd wynosiła 50. (Ta opcja byłaby spoko jakby Azure kasował dużo za ilość użytych funckji nie ważne co robią, to wlaczenie funkcji tylko dla użytkownika co ma 0 tweetów nie ma sensu).


####  Update id polityków na podstawie ich nickow
Odpalam tę funkcję z argumentem jakim jest ID polityka i inne jego opcje jak partia i dopisuje go do bazy by w nastepnych odpaleniach on był uruchamiany. 


#### Funkcje sumujące 
Raz w tygodniu odpalać funkcję która sumuje tweety z ostatniego tygodnia, miesiaca. 
- Chodzi tu o to by nie trzymać aż tak dużo słów w bazie więc po tygodniu ich istnieja z informacją dokładną do dnia sumować słowa z danego tygodnia i trzymać je z informacją dokładną do tygodnia. Po 4 tygodniach trzymać je tylko z inforacją dokładną do miesiaca. 


## API
| url    |      methods     |   description |
|----------|:-------------:|------:|
| /api/v1/politicians     |  GET, POST   | retrieve list of politician |
| /api/v1/politicians/{politicianId}/summary?interval=-1d  |    GET     |  retrieve summary of words by specific politician |
| /api/v1/parties |  GET, POST  |   retrieve list of parties |
| /api/v1/parties/{partyId}/summary?interval=-1d   | GET | retrieve summary of words by specific party |
| /api/v1/words?politicianId=  |  GET  |    retrieve list of words|
| /api/v1/words/{word}/summary?interval=-1d  | GET   |    retrieve summary of specific word |



## Possible improvements
- Cashing requests(summaries by summary parameters checksum) on Redis-like DB 
- Add more politicains 
- Add poltics commentators xD
- Możliwość dodania na froncie/wywolania funkcji ktora doda to do bazy nowego polityka po jego nicku z tt 
