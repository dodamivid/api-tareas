"""API de tareas: proyecto de práctica para demostrar CI/CD con GitHub Actions."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API de Tareas", version="1.0.0")

_db: dict[int, dict] = {}
_next_id = 1


class TareaIn(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    hecha: bool = False


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/tareas")
def listar() -> list[dict]:
    return list(_db.values())


@app.post("/tareas", status_code=201)
def crear(t: TareaIn) -> dict:
    global _next_id
    tarea = {"id": _next_id, **t.model_dump()}
    _db[_next_id] = tarea
    _next_id += 1
    return tarea


@app.get("/tareas/{tarea_id}")
def obtener(tarea_id: int) -> dict:
    if tarea_id not in _db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return _db[tarea_id]


@app.delete("/tareas/{tarea_id}", status_code=204)
def borrar(tarea_id: int) -> None:
    if tarea_id not in _db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    del _db[tarea_id]
