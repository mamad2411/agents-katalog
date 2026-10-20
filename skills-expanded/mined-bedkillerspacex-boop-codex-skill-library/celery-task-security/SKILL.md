---
name: celery-task-security
description: >
  Secure Celery task queues for owned apps: broker auth/TLS, serialization (JSON not
  pickle), task authz, rate limits, result backend hygiene, routing, and worker OS
  privileges. Use when Celery pickle RCE risk, Redis/RabbitMQ broker hardening, task
  name injection, or untrusted task payloads — not for attacking third-party queues.
---

# Celery Task Security

## Scope And Authorization

- **In scope:** Celery deployments, brokers, and result backends you operate.
- **Out of scope:** Unauthorized access to others’ Redis/RabbitMQ/Celery.
- Pickle deserialization of untrusted messages is **RCE** — treat as critical.
- Pair with `redis-security-misconfig`, secrets hygiene, `code-quality-standards`.

## When To Use

- Hardening Celery in Django/FastAPI/Flask apps.
- Findings: `pickle` serializer, open broker, tasks that run shell on input.
- Multi-tenant task queues needing isolation.
- Configuring acks, time limits, and least-privilege workers.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Redis bind/AUTH general | `redis-security-misconfig` |
| Generic async patterns | backend reliability skills |
| Supply chain Python | Python packaging skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Surface | Risk |
| --- | --- |
| Serializer | Pickle/YAML → RCE |
| Broker | Open Redis/AMQP → task inject |
| Result backend | Sensitive result leakage |
| Task code | Command injection, SSRF via tasks |
| Workers | Overprivileged OS user / network |
| Autodiscover | Untrusted packages registering tasks |

## Workflow

### 1. Confirm scope and success criteria

1. Celery version, broker (Redis/RabbitMQ/SQS), result backend, internet exposure.
2. Success: JSON (or equivalent safe) serializer only; broker authenticated + TLS/private net; workers non-root; no arbitrary task execution from untrusted users.
3. Inventory all task modules.

### 2. Inventory configuration

```bash
# Search config
rg -n "CELERY_|broker_url|task_serializer|accept_content|pickle|result_backend" -g '*.{py,env,yml,toml}'
celery -A proj inspect conf 2>/dev/null | head
```

1. Note `task_always_eager` in prod (should be false).
2. List queues and routes.
3. Who can publish to broker?

### 3. Safe serialization (critical)

```python
# Celery config — preferred
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    event_serializer="json",
)
# NEVER accept pickle in production with untrusted producers
```

1. If legacy pickle required temporarily: isolate private broker, no Internet, signed network, migration plan with expiry.
2. Reject unknown content types.

### 4. Broker and backend hardening

| Control | Guidance |
| --- | --- |
| Network | Private subnets; no public 6379/5672 |
| Auth | Redis AUTH/ACL; RabbitMQ users per app |
| TLS | Where supported end-to-end |
| ACL | Producers ≠ consumers credentials when possible |
| Persistence | Result TTLs; do not store secrets in results |
| SQS | IAM least privilege; no world-writable queues |

```python
# broker_url from env/secret manager — not committed
# rediss://:password@host:6379/0  # TLS variant when configured
```

### 5. Task design authz and safety

```python
@app.task(bind=True, time_limit=60, soft_time_limit=50)
def export_user_data(self, requester_id: int, user_id: int):
    if requester_id != user_id and not is_admin(requester_id):
        raise PermissionError("forbidden")
    # no shell=True; no pickle loads; validate paths
    ...
```

1. **Never** trust client-supplied task name/args without authz — expose only via your API that enqueues after session checks.
2. Avoid `celery.task.control` exposure to web tier.
3. `autoregister` / import only trusted modules.
4. Rate limit hot tasks (`rate_limit=` or broker throttles).
5. Time limits prevent stuck CPU bombs.
6. Idempotent tasks for at-least-once delivery.

### 6. Worker process hardening

1. Run workers as non-root; read-only FS where possible.
2. Separate queues: `cpu`, `io`, `highrisk` with different pools.
3. No cloud admin credentials on workers that execute user-driven tasks — scope IAM.
4. Disable dangerous `celery events` exposure publicly.
5. Keep dependencies patched (`pip audit` / etc.).

### 7. Verify and hand off

```bash
# Confirm serializers
celery -A proj inspect conf | rg -i serializer
# Broker not public
# Attempt from unauthorized network should fail
# Unit: task rejects cross-user export
pytest tests/test_celery_security.py -q
```

1. Pen-test style: can web user enqueue arbitrary task by talking to Redis? Must be no.
2. Log redaction: task args may contain PII — configure careful logging.
3. Apply `code-quality-standards`; document runbooks for poison queue messages.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Serializer | JSON only | `pickle` + `accept_content=['pickle']` |
| Broker | Private + AUTH | Redis `0.0.0.0` no password |
| Enqueue | After app authz | Client publishes raw Celery messages |
| Tasks | Validated args | `subprocess` on user string |
| Results | Short TTL, no secrets | Password reset tokens in results forever |
| Workers | Least IAM | Admin AWS keys on all workers |

## Output Checklist

- [ ] Serializer locked to JSON (or safe)
- [ ] Broker/backend auth + network hardened
- [ ] Secrets not in git or results long-term
- [ ] Task authz on sensitive operations
- [ ] Time/rate limits set
- [ ] Workers non-root least privilege
- [ ] Verification: no arbitrary publish path
- [ ] Logging redaction reviewed
- [ ] `code-quality-standards` applied

## Rules

- Pickle + untrusted messages = RCE; eliminate in shared systems.
- Application authz must gate enqueue; broker is not your IdP.
- Isolate brokers from the public Internet.
- Authorized environments only.
- Redis-specific bind/ACL depth → `redis-security-misconfig`.
