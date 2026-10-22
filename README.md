# API de Tareas · CI con GitHub Actions

![CI](https://github.com/dodamivid/api-tareas/actions/workflows/ci.yml/badge.svg)

Pipeline: **lint (ruff)** + **pruebas (pytest) en Python 3.11 / 3.12 / 3.13** con cobertura mínima de 90 %.

```bash
pip install -r requirements-dev.txt && ruff check . && pytest
```
