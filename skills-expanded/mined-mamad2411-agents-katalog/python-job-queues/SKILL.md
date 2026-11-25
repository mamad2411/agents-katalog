---
name: python-job-queues
description: Use when picking a Python async job queue — Procrastinate (Postgres LISTEN/NOTIFY), Celery, Arq, Dramatiq, APScheduler.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [python]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [python-django, python-essentials, postgres, observability-essentials]
---

# Python Job Queues

**Iron Law: every job is idempotent — same input MUST produce the same outcome whether it ran 0, 1, or N times. Retries are not a hypothetical; they will happen. Pass an `idempotency_key`, dedupe at the side-effect boundary (DB row, external API call), never trust "the queue will only deliver once."**

## Decision table — which queue?

| Queue                    | Broker                               | Pick when                                                                                                                                          |
| ------------------------ | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Procrastinate**        | Postgres (LISTEN/NOTIFY)             | You already have Postgres, jobs/sec ≤ a few hundred, you want one less moving part. **Default for typical Django apps.**                           |
| **Celery**               | RabbitMQ / Redis / SQS               | You need RabbitMQ routing (exchanges, topic), priority queues, broad ecosystem (Flower, beat), or you're already on it. Heaviest of the bunch.     |
| **Arq**                  | Redis                                | You want async-native, lightweight, FastAPI-style. Stays simple; small ecosystem.                                                                  |
| **Dramatiq**             | RabbitMQ / Redis                     | You want "Celery done right" — simpler API, better defaults, but smaller community.                                                                |
| **APScheduler**          | In-process (or Postgres/Redis store) | Periodic jobs only, in-process, single instance. **Loses jobs on crash unless backed by a persistent store** — fragile for production work queues. |
| **Raw PG LISTEN/NOTIFY** | Postgres                             | One small notification stream, you don't need retries/scheduling. Roll-your-own; don't reach for it before Procrastinate.                          |

### Rule of thumb

- Already running Postgres? Start with **Procrastinate**. PG is the only persistent dependency. LISTEN/NOTIFY gives you sub-second latency without a separate Redis/RabbitMQ to operate.
- Reach for Celery only when you need RabbitMQ-specific routing (topic exchanges, dead-letter queues with broker-side semantics) or SQS for cross-account decoupling.
- `APScheduler` is fine for "run this cron-style every hour" inside ONE process — **lost on crash** unless you configure the SQLAlchemy/MongoDB job store, at which point you've reinvented half a queue.

## Procrastinate — Django integration

```python
# settings.py
INSTALLED_APPS += ["procrastinate.contrib.django"]
PROCRASTINATE_APP = "myproject.tasks.app"

# tasks.py
from procrastinate.contrib.django import app

@app.task(queue="default", retry={"max_attempts": 5, "wait": 30, "exponential": True})
def render_report(report_id: int) -> None:
    Report.objects.get(pk=report_id).render()       # idempotent — re-render is safe

# enqueue from a Django view / signal:
render_report.defer(report_id=42)                   # async write to PG, worker picks up
```

Run a worker: `manage.py procrastinate worker --queues default`. Periodic schedules go in `app.periodic_task(cron="0 * * * *")` decorators — Procrastinate enforces single-fire across workers using PG advisory locks.

| Need                   | Procrastinate primitive                                 |
| ---------------------- | ------------------------------------------------------- |
| At-least-once delivery | Default — retries until `max_attempts`                  |
| Job result             | `await job.result()` — stored in PG                     |
| Periodic               | `@app.periodic_task(cron="...")`                        |
| Job-level lock         | `queueing_lock="report-42"` — only one queued at a time |
| Worker-level lock      | `lock="report-42"` — only one running at a time         |
| Schema migrations      | `manage.py procrastinate schema --apply`                |

Migrations are versioned and **must be applied before code that uses new features** ships.

## Celery — when you actually need it

```python
# celery.py
from celery import Celery
app = Celery("project", broker="amqp://rabbit/", backend="redis://redis/")

@app.task(bind=True, autoretry_for=(SomeError,), retry_backoff=True, max_retries=5,
          acks_late=True, reject_on_worker_lost=True)
def send_email(self, user_id: int) -> None:
    user = User.objects.get(pk=user_id)
    mail.send(user.email)
```

**Defaults you must set explicitly** (Celery's out-of-box settings will lose jobs):

| Setting                                   | Value    | Why                                                          |
| ----------------------------------------- | -------- | ------------------------------------------------------------ |
| `acks_late=True`                          | per-task | Ack AFTER success, not on receive — worker crash re-delivers |
| `task_reject_on_worker_lost=True`         | global   | Lost workers re-queue, don't silently drop                   |
| `worker_prefetch_multiplier=1`            | global   | Stop hoarding tasks; let other workers pick up               |
| `task_acks_on_failure_or_timeout=False`   | global   | Failures requeue, don't ack                                  |
| `broker_connection_retry_on_startup=True` | global   | Survive transient RabbitMQ flap                              |

Out of the box, Celery + Redis broker has data-loss footguns. Use RabbitMQ for anything you can't afford to lose; Redis broker only for fire-and-forget telemetry.

## Arq — async-native, Redis-backed

```python
from arq import create_pool
from arq.connections import RedisSettings

async def render_report(ctx, report_id: int) -> None:
    await Report.objects.aget(pk=report_id).arender()

class WorkerSettings:
    functions = [render_report]
    redis_settings = RedisSettings(host="redis")
    max_jobs = 10                                     # concurrent per worker
    job_timeout = 300                                 # seconds
```

Best fit when your stack is already async (FastAPI + async ORM). Smaller surface, no broker debate. Limited periodic-job sophistication compared to Procrastinate/Celery.

## Dramatiq — "Celery without the footguns"

```python
import dramatiq
from dramatiq.brokers.redis import RedisBroker
dramatiq.set_broker(RedisBroker(host="redis"))

@dramatiq.actor(max_retries=5, min_backoff=1000, max_backoff=60_000, time_limit=60_000)
def render_report(report_id: int) -> None:
    Report.objects.get(pk=report_id).render()
```

Sane defaults out of the box (acks-late, retries, time limits). Smaller ecosystem; no `beat`-style scheduler built in (use `apscheduler` or cron).

## APScheduler — for in-process scheduling

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

scheduler = BackgroundScheduler(
    jobstores={"default": SQLAlchemyJobStore(url=os.environ["DATABASE_URL"])},
)
scheduler.add_job(refresh_cache, "interval", minutes=5, id="refresh_cache", replace_existing=True)
scheduler.start()
```

**Without a persistent jobstore, APScheduler loses every pending job on process exit.** Configure the SQLAlchemy/Redis/Mongo jobstore, or accept that you're using it for "best-effort in-memory cron" only. Across multiple Django processes (Gunicorn workers), every instance will try to fire the job — use `replace_existing=True` AND a coordination lock (advisory lock, Redis SETNX) or use a real queue.

## Retry semantics — what you need to think about

| Concern                 | Implementation                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Idempotency**         | Dedupe at the side effect. DB write: `INSERT ... ON CONFLICT DO NOTHING`. External API: pass `Idempotency-Key` header (Stripe-style). |
| **Backoff**             | Exponential with jitter — synchronized retries thunder-herd downstream                                                                |
| **Poison messages**     | `max_retries` then dead-letter (manual table, separate queue, or alert)                                                               |
| **Visibility timeout**  | Job that exceeds the timeout is re-delivered while still running — set it longer than your P99                                        |
| **Long jobs**           | Checkpoint progress; on retry, resume from last checkpoint, not from scratch                                                          |
| **Time-sensitive jobs** | Include `enqueued_at` in the payload; skip if too stale                                                                               |

## Periodic jobs

| Queue         | Mechanism                                                                       |
| ------------- | ------------------------------------------------------------------------------- |
| Procrastinate | `@app.periodic_task(cron="...")` — built-in, single-fire across workers         |
| Celery        | `celery beat` — separate process; **must run exactly one** or jobs fire N times |
| Arq           | `cron_jobs = [cron(refresh, hour=3)]` in worker settings                        |
| Dramatiq      | Use external scheduler (apscheduler, cron, k8s CronJob)                         |
| APScheduler   | First-class — but see the persistence caveat above                              |

## Observability hooks

- **Job lifecycle events**: emit `started`, `succeeded`, `failed`, `retried` to Sentry / Prometheus
- **Queue depth**: scrape per-queue depth into Prometheus — set alerts at depth growth rate, not absolute
- **Job duration histogram**: per task type — find drift early
- **Failure rate**: per task type — Sentry release-tagged
- **Worker liveness**: heartbeat to PG/Redis; alert if no worker for 60s
- Procrastinate exposes `procrastinate_jobs` table — query for depth, oldest pending, retry counts directly

## Anti-patterns

- Non-idempotent jobs ("send_email" that doesn't dedupe by recipient+template) — retry causes double-send
- Passing big objects in the payload (PDF bytes, ML models) — payload bloat slows the queue; pass IDs, load inside the worker
- Job that calls `time.sleep(60)` to "throttle" — blocks the worker; use the queue's rate-limit or split into N smaller jobs
- Catching exceptions in the job and returning normally — masks failures from the queue's retry logic
- Long-running jobs (>1h) on a queue with short visibility timeout — re-delivered while still running; use a separate "long" queue with longer timeout
- `APScheduler` in production without a persistent jobstore — jobs lost on every deploy
- Celery defaults without `acks_late` — worker crash = silent loss
- One queue for all task types — slow OCR jobs starve fast notification jobs; use named queues
- Calling Django ORM in `async def` Arq jobs without `sync_to_async` — silent blocking on event loop
- Database writes inside transactions that span the job enqueue — if the queue is your DB (Procrastinate), this is fine; if external (Celery/Redis), the enqueue might commit before the row is visible, and the worker sees stale data

## Hand-off

For Django integration patterns (signals, `transaction.on_commit`): `Skill(devkit:python-django)`. For idempotency at the DB layer (advisory locks, ON CONFLICT, unique constraints): `Skill(devkit:postgres)`. For monitoring queue depth and failure rates: `Skill(devkit:observability-essentials)`. For broader Python rules: `Skill(devkit:python-essentials)`.
