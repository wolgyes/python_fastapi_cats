# Állatmentő API
Ez az API lehetővé teszi, hogy az állatmentő szervezet kezelhesse az általuk mentett macskákat.

## Telepítés
Az alkalmazás telepítéséhez először telepítenünk kell a szükséges dependecy-ket.<br>Ehhez használjuk a pip csomagkezelőt:
```
pip install -r requirements.txt
```
(de inkább pipenv: https://pipenv-fork.readthedocs.io/en/latest/basics.html)

## Futtatás
Az alkalmazás futtatásához a több fajta futtatási lehetőség van, az egyik opció ezek közül:
```bash
uvicorn main:app --reload
```
Az alkalmazás ezt követően elérhető lesz a http://127.0.0.1:8000/ címen.

## Elérhető végpontok
Az API az alábbi végpontokat kínálja:
``` http request
GET /cats
A mentett macskák lekérdezése.

POST /cats
Új macska hozzáadása a rendszerhez.

PUT /cats/{cat_id}
A megadott azonosítójú macska adatainak frissítése.

DELETE /cats/{cat_id}
A megadott azonosítójú macska törlése.
```

Modell
Az API a következő adatmodellt használja:


```json
{
    "id": 1,
    "name": "Mr. Whiskers",
    "breed": "Persian",
    "age": 2
}
```
Engedélyezett eredetek
Az API csak bizonyos CORS-tól fogadja el a kéréseket. Az engedélyezett CORS-ok konfigurálása az origins tömbben történik a main.py fájlban. Alapértelmezés szerint az alábbi eredetek engedélyezettek:
```
http://localhost
http://localhost:3000
http://192.168.1.150:3000
http://127.0.0.1:3000
```
Felhasznált technológiák
Az API a következő technológiákat használja:


- FastAPI
- Pydantic
- uvicorn
- CORS Middleware

## Frontend

Az applikációhoz tartozó frontend az alábbi linken érhető el:
https://github.com/wolgyes/react-cats


## Update: 2023.05.08
- Kapott egy buta klienst
- buta backend testek
- képfeltöltés
- nincs hozzá react update (nem is lesz :D)