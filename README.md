# FastAPI CI/CD + GHCR +  VPS

Najprostszy serwis FastAPI z automatyzacją:
- testów i budowy w GitHub Actions,
- publikacji obrazu Docker do GHCR,
- wdrożenia na VPS przez SSH i `docker compose`.

## Endpointy

- `GET /` -> wiadomość testowa
- `GET /health` -> status zdrowia

## Uruchomienie lokalne (bez Dockera)

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Testy

```bash
pytest
```

## Build obrazu lokalnie

```bash
docker build -t fastapi-cicd:local .
docker run --rm -p 8000:8000 fastapi-cicd:local
```

## GitHub Actions

Workflow: `.github/workflows/ci-cd.yml`

Działa tak:
1. `pull_request` do `main`: uruchamia testy.
2. `push` do `main`: testy -> build obrazu -> push do GHCR -> deploy na VPS.

## Wymagane sekrety repozytorium

Ustaw w GitHub (`Settings -> Secrets and variables -> Actions -> Repository secrets`):

- `VPS_SSH_KEY` - prywatny klucz SSH (format PEM) dla użytkownika `debian`
- `GHCR_PAT` - GitHub PAT z zakresem co najmniej `read:packages`

Workflow używa automatycznie właściciela repo jako loginu do GHCR.

Parametry VPS są ustawione bezpośrednio w workflow:

- host: `146.59.12.114`
- user: `debian`
- SSH port: `22`
- port aplikacji: `8049` (na podstawie numeru indeksu `049`)

## Wymagania na VPS

Na serwerze muszą być dostępne:
- Docker
- Docker Compose v2 (`docker compose`)

Przykład instalacji (Ubuntu):

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
```

## Co robi deploy

Podczas `push` na `main` workflow:
1. kopiuje `docker-compose.yml` do `/home/debian/fastapi-cicd`,
2. tworzy tam plik `.env` z obrazem i tagiem,
3. loguje się do GHCR,
4. wykonuje `docker compose pull` i `docker compose up -d`.

Po wdrożeniu aplikacja będzie dostępna pod adresem:

`http://146.59.12.114:8049`
