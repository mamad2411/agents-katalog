# Django Celery Tasks

## Summary

**One-sentence:** Integrate Celery into Django with explicit task names, idempotency, retry policy, time limits, and DLQ for every async task.

**One-paragraph:** Every Celery task declares an explicit name, an idempotency guard, retry policy (max_retries, retry_backoff, retry_jitter), and time limits (soft_time_limit, time_limit). Tasks land on a named queue with a known worker pool. Failures route to a dead-letter queue with alert + retry policy. Output is task module code + queue config + monitoring spec.

**Ефективно для:**

- Building reliable async pipelines (emails, webhooks, ETL, report generation).
- Replacing synchronous request handlers with background processing.
- Designing predictable retry + failure semantics across many task types.
- Onboarding engineers to a Celery codebase with consistent conventions.

## Applies If (ALL must hold)

- Django project with Celery 5+ as the async runner.
- Broker is Redis or RabbitMQ; result backend chosen.
- Tasks have user-visible failure modes (retry, alert, DLQ).
- Operations team needs visibility into task health (Flower, Prometheus exporters).

## Skip If (ANY kills it)

- Sync request handling is fast enough — Celery adds complexity without payoff.
- Use case is a single cron job (django-extensions runscript or crontab is simpler).
- Project uses a different runner (RQ, Dramatiq, Huey) — methodology specifics differ.
- Long-running pipelines belong in Airflow / Prefect, not Celery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task inventory: name, trigger, payload shape, frequency | table | tech-lead |
| Broker + result backend chosen + version pinned | config | platform |
| Queue topology decision: per-priority or per-domain queues | ADR | tech-lead |
| Alerting integration (PagerDuty, Slack) for DLQ events | endpoint | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[django-services]] | Tasks call into service-layer functions. |
| [[logging-patterns]] | Structured logs around task lifecycle. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (explicit name, idempotency, retry policy, time limits, named queues, DLQ) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for Celery task module spec + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory → name + idempotency → policies → queues → monitoring | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `task_authoring` | sonnet | Mechanical task module emission with policies. |
| `queue_topology_design` | opus | Cross-cutting decision about isolation + priority. |
| `dlq_alerting_wire_up` | sonnet | Plumbing exporters + alert routes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/task-idempotent.py` | Celery task template with idempotency, retry, time limits |
| `templates/celery-worker.service` | systemd unit for worker |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-celery.py` | Validate the task module spec metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[django-services]]
- [[message-queues]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps async need, runner choice, and reliability requirements to a rule from `01-core-rules.xml`, telling the agent whether to apply the Celery conventions or skip in favour of a different runner or sync handling. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/task-idempotent.py`

```python
# task-idempotent.py — Canonical idempotent Celery task pattern
# Input:  user_id (int, primitive)
# Output: bool — True if action was performed, False if already done

import requests
from celery import shared_task


@shared_task(
    name="emails.send_welcome",
    bind=True,
    max_retries=5,
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    soft_time_limit=300,   # fires SoftTimeLimitExceeded
    time_limit=360,        # hard SIGKILL
    acks_late=True,
    task_reject_on_worker_lost=True,
)
def send_welcome(self, user_id: int) -> bool:
    """
    Send welcome email to user.

    Idempotent: checks welcome_email_sent before acting.
    Uses DB-level atomic UPDATE WHERE not_done to prevent race conditions.
    """
    from apps.users.models import User

    user = User.objects.only("id", "email", "welcome_email_sent").get(pk=user_id)

    if user.welcome_email_sent:
        return False  # already sent, safe to return

    # Perform the side effect
    _send_welcome_email(user.email)

    # Atomic guard: only mark done if it was False (handles concurrent retries)
    updated = User.objects.filter(pk=user_id, welcome_email_sent=False).update(
        welcome_email_sent=True
    )
    return bool(updated)


def _send_welcome_email(email: str) -> None:
    """Send the actual email. Raises requests.RequestException on failure."""
    response = requests.post(
        "https://api.email-provider.com/send",
        json={"to": email, "template": "welcome"},
        timeout=30,
    )
    response.raise_for_status()
```

### `templates/celery-worker.service`

```ini
# /etc/systemd/system/celery-emails.service
# Systemd unit for a single-queue Celery worker.
# Adjust: User, WorkingDirectory, ExecStart queue name, concurrency.

[Unit]
Description=Celery worker (emails queue)
After=network.target redis.service

[Service]
Type=simple
User=app
Group=app
EnvironmentFile=/etc/app/celery.env
WorkingDirectory=/srv/app
ExecStart=/srv/app/.venv/bin/celery -A config worker \
  -Q emails \
  -n emails@%%h \
  --concurrency=4 \
  --max-tasks-per-child=200 \
  --soft-time-limit=300 \
  --time-limit=360 \
  --without-gossip \
  --without-mingle
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
