---
name: celery-async-task
description: "Use when: creating a Celery async task in Overfitted.io backend, setting up worker.py, dispatching a task from a FastAPI endpoint, or polling task status. Covers Redis queue, Celery app init, and the full async task lifecycle."
---

# Celery Async Task — Overfitted.io

## 1. Créer / vérifier `backend/app/worker.py`

Si le fichier n'existe pas, le créer :

```python
from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "overfitted",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)
```

## 2. Définir une tâche

Toujours décorer avec `@celery_app.task(bind=True)` pour accéder à `self.update_state` :

```python
# backend/app/worker.py
from app.worker import celery_app

@celery_app.task(bind=True)
def process_image_task(self, file_bytes: bytes) -> dict:
    self.update_state(state="PROCESSING")
    # ... traitement image ici ...
    return {"status": "done", "output_path": "/tmp/result.svg"}
```

## 3. Dispatcher depuis un endpoint FastAPI

```python
from fastapi import APIRouter, UploadFile
from app.worker import process_image_task

router = APIRouter()

@router.post("/process")
async def process(file: UploadFile) -> dict:
    data = await file.read()
    task = process_image_task.delay(data)
    return {"task_id": task.id, "status": "pending"}
```

## 4. Endpoint de polling du statut

```python
from celery.result import AsyncResult

@router.get("/status/{task_id}")
async def task_status(task_id: str) -> dict:
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
```

## 5. Lancer le worker en local

```bash
cd backend
celery -A app.worker.celery_app worker --loglevel=info
```

## 6. Gotchas
- **Redis doit tourner** avant de lancer le worker — vérifier `REDIS_URL` dans `.env`
- **Ne jamais passer des objets non-sérialisables** (PIL Image, fichiers ouverts) dans `.delay()` — sérialiser en `bytes` ou `str` (path)
- **`bind=True`** requis pour `self.update_state` — sans ça, pas de statut intermédiaire
- **Tests** : mocker `celery_app.send_task` ou utiliser `CELERY_TASK_ALWAYS_EAGER=True` dans les fixtures pytest
