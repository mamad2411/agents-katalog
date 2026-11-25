---
name: python-background-workers
description: "When to activate: ARQ, RQ, background workers, Redis-based queues, async task workers"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python Background Worker Patterns

## ARQ (Async Redis Queue)
```python
# tasks.py
from arq import cron
from arq.connections import RedisSettings
import logging

logger = logging.getLogger(__name__)

async def send_email(ctx: dict, to: str, subject: str, body: str) -> dict:
    """ARQ task: enqueue with await redis.enqueue_job('send_email', ...)"""
    try:
        await email_service.send(to=to, subject=subject, body=body)
        return {"status": "sent"}
    except Exception as exc:
        logger.exception("Email send failed: %s", exc)
        raise  # ARQ will retry based on worker settings

async def generate_report(ctx: dict, report_id: str, params: dict) -> dict:
    db = ctx["db"]  # injected via on_startup
    report = await report_service.generate(db, report_id, params)
    return {"report_id": report_id, "url": report.download_url}

# Worker settings
class WorkerSettings:
    redis_settings = RedisSettings(host="redis", port=6379)
    functions = [send_email, generate_report]
    max_jobs = 10
    job_timeout = 300
    keep_result = 3600
    retry_jobs = True
    
    # Periodic jobs
    cron_jobs = [
        cron(cleanup_expired_sessions, hour={0}, minute={0}),  # daily at midnight
    ]
    
    async def on_startup(ctx: dict) -> None:
        ctx["db"] = await create_db_session()
    
    async def on_shutdown(ctx: dict) -> None:
        await ctx["db"].close()

# Enqueue from FastAPI
@router.post("/reports")
async def trigger_report(params: ReportParams, redis=Depends(get_redis)):
    report_id = str(uuid4())
    await redis.enqueue_job("generate_report", report_id=report_id, params=params.dict())
    return {"report_id": report_id}
```

## RQ (Redis Queue, sync)
```python
from rq import Queue
from redis import Redis
from rq.job import Job

redis_conn = Redis(host="redis", port=6379)
default_queue = Queue("default", connection=redis_conn)
high_queue = Queue("high", connection=redis_conn)

# Enqueue
job = high_queue.enqueue(
    send_welcome_email,
    args=(user.email, user.name),
    job_timeout=60,
    retry=Retry(max=3, interval=[10, 30, 60]),
)

# Check job status
job = Job.fetch(job_id, connection=redis_conn)
print(job.get_status())  # queued | started | finished | failed
print(job.result)        # return value if finished

# Worker: run with `rq worker high default`
```
