---
name: django-async-views-pitfalls
description: >
  Avoid Django async view and ASGI pitfalls: ORM sync-in-async, get_sync_to_async misuse,
  connection handling, middleware compatibility, cache/DB/httpx, and when to stay sync.
  Use when Django async def views, ASGI, async ORM, SynchronousOnlyOperation, async
  middleware, or owned Django performance under async — not general asyncio tutorials alone.
---

# Django Async Views Pitfalls

## Scope And Authorization

- **In scope:** Django apps you own; load tests on non-prod first.
- **Out of scope:** Blind production flips to ASGI without testing ORM paths.
- Prefer measuring benefit (IO wait) before converting entire codebase to async.
- Redact credentials in settings dumps used for debugging.
- Pair with `django-orm-nplusone`, `django-security-settings`, and `code-quality-standards`.

## When To Use

- Adopting `async def` views or async middleware on Django 4.1+.
- Seeing `SynchronousOnlyOperation` in logs.
- Mixing Django ORM with async views incorrectly.
- Choosing uvicorn/daphne/hypercorn vs gunicorn sync workers.
- Reviewing third-party packages for async safety.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| N+1 query fixes | `django-orm-nplusone` |
| CSRF/security settings | `django-csrf-middleware-tuning` / `django-security-settings` |
| General Python asyncio | language asyncio guides |
| Redis locks | `distributed-lock-redis-safety` |
| Code quality baseline | `code-quality-standards` |

## Core rules of thumb

| Rule | Detail |
| --- | --- |
| ORM is sync-first | Calling ORM directly from async context raises or blocks |
| `sync_to_async` | Wrap ORM/blocking calls; use `thread_sensitive=True` default carefully |
| One request, one thread affinity | Django DB connections are thread-bound historically |
| Async helps IO | Concurrent awaits to HTTP/cache; not a free CPU speedup |
| Middleware | Not all middleware is async-capable; order matters |
| Prefer explicit | Full async stack or sync stack; minimize mixed footguns |

## Workflow

### 1. Confirm scope and success criteria

1. Django version, deployment (ASGI vs WSGI), endpoints candidates for async.
2. Success: no `SynchronousOnlyOperation`; no connection leaks; latency improves under concurrent IO; tests cover async paths.
3. Document endpoints that remain intentionally sync.

### 2. Inventory async surface

```bash
rg -n "async def |sync_to_async|async_to_sync|AsyncMiddleware|ASGI" --type py
rg -n "uvicorn|daphne|hypercorn|gunicorn" Dockerfile* docker-compose* Procfile* .github 2>/dev/null
```

1. List third-party apps: admin, debug toolbar, auth backends—async compatible?
2. Note template rendering and session backends.

### 3. Avoid ORM-in-async pitfalls

```python
# BAD — ORM in async view without wrapping (Django raises SynchronousOnlyOperation)
async def bad_view(request):
    user = User.objects.get(id=request.user.id)  # wrong
    return JsonResponse({"u": user.username})

# BETTER — wrap ORM
from asgiref.sync import sync_to_async

async def ok_view(request):
    user = await sync_to_async(User.objects.get)(id=request.user.id)
    return JsonResponse({"u": user.username})

# OFTEN BEST — keep view sync if it is ORM-heavy
def fine_sync_view(request):
    user = User.objects.select_related("profile").get(id=request.user.id)
    return JsonResponse({"u": user.username})
```

1. Django continues improving async ORM (`aget`, `afilter` in newer versions)—use version-correct APIs when available; still avoid naive patterns.
2. Do not call `sync_to_async` for every tiny attribute access in a loop—batch in one sync function.

```python
@sync_to_async
def load_user_bundle(user_id: int):
    return (
        User.objects.select_related("profile")
        .prefetch_related("groups")
        .get(id=user_id)
    )
```

### 4. Connections, transactions, and threads

1. DB connections in async contexts: understand `close_old_connections` behavior; avoid sharing connections across tasks incorrectly.
2. `atomic()` blocks are sync—run transactional units inside a single `sync_to_async` function.
3. `thread_sensitive=True` (default for `sync_to_async`) keeps Django ORM on a consistent thread—required for many Django APIs; do not casually set False for ORM.
4. Background `asyncio.create_task` that touches ORM is a footgun—prefer Celery/RQ for background work.

### 5. External IO: the actual win

```python
import httpx
from django.http import JsonResponse

async def proxy_view(request):
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get("https://api.example.com/data")
    return JsonResponse(r.json())
```

1. Use async HTTP/Redis clients when the view is async.
2. Do not call `requests.get` inside async views without `sync_to_async` (blocks event loop).
3. Measure: concurrent outbound IO benefits most.

### 6. Middleware, auth, CSRF

1. Ensure security middleware still applies under ASGI.
2. Session/auth: test login/logout and CSRF on async views (`django-csrf-middleware-tuning`).
3. Streaming/`StreamingHttpResponse` async iterators: verify client disconnect handling.
4. File uploads and body reads: know sync vs async request body APIs for your Django version.

### 7. Test, deploy, hand off

```bash
# Owned project
pytest --ds=config.settings -q
# Run ASGI locally
uvicorn config.asgi:application --reload
# Load test concurrent IO endpoints (staging)
```

1. Explicit tests that async views do not call ORM bare.
2. Production: worker count and event loop config; do not assume 1:1 with gunicorn sync formula.
3. Document: “async only for endpoints X,Y.”
4. Apply `code-quality-standards` and typing for async functions.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| ORM-heavy page | Sync view + optimized ORM | Async view wrapping 50 queries |
| Fan-out HTTP | `httpx` async | `requests` on event loop |
| `sync_to_async` | One batch function | Decorator spam per field |
| Background | Task queue | Fire-and-forget asyncio + ORM |
| Deploy | Tested ASGI | Flip ASGI switch Friday night |
| Middleware | Verified async-safe | Assume all packages work |

## Output Checklist

- [ ] Async candidates justified by IO concurrency
- [ ] ORM access uses async-safe APIs or batched `sync_to_async`
- [ ] No bare ORM in `async def` (tests/CI grep)
- [ ] External clients are async-capable
- [ ] Middleware/auth/CSRF verified under ASGI
- [ ] Connection/transaction patterns reviewed
- [ ] Load test evidence on staging
- [ ] Remaining sync endpoints documented
- [ ] Deployment (uvicorn/daphne) documented
- [ ] `code-quality-standards` applied

## Rules

- Async is not a magic performance switch for ORM-bound apps.
- Never block the event loop with sync IO.
- Prefer clarity: sync views for sync stacks.
- Match Django version docs for async ORM features.
- Owned apps only; evidence with tests and load metrics.
