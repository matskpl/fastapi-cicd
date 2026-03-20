from fastapi import FastAPI

app = FastAPI(title="FastAPI CI/CD Demo")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from FastAPI CI/CD"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}