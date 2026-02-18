# Rollercoaster Park

![Rollercoaster Park](assets/banner.png)

API REST per la gestione di un parco divertimenti costruita con **FastAPI**, **SQLAlchemy** e **PostgreSQL**.

Il progetto include anche un simulatore standalone (`app/main.py`) che dimostra la logica OOP del parco (attrazioni, famiglie, code e giri).

## Requisiti

- Python 3.12
- Docker (per PostgreSQL)

## Installazione

```bash
git clone <url-del-repo>
cd RollercoasterPark-OOP

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Avvio

Avvia il database PostgreSQL con Docker:

```bash
docker compose -f docker/docker-compose.yml up -d
```

Crea un file `.env` nella root del progetto con la stringa di connessione (vedi `.env.example` o il `docker-compose.yml` per i valori).

Avvia l'applicazione:

```bash
uvicorn app.app:app --reload
```

La documentazione interattiva delle API sarà disponibile su [http://localhost:8000/docs](http://localhost:8000/docs).

## Test

I test usano SQLite in-memory, quindi **non serve Docker** per eseguirli:

```bash
pytest -v
```
