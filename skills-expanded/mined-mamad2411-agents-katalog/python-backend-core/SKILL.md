---
name: python-backend-core
description: "Shared reference for the python-backend cluster: the thin-adapter model (web/API layer over a typed, tested core), the Django-vs-FastAPI decision, boundary validation, the test/verify gate, and the shared tooling matrix. USE WHEN choosing a Python web framework, wiring persistence or validation, or planning a release — the conventions every spoke in this cluster shares."
cluster: python-backend
version: 1.0.0
---

# Python Backend Core

Shared model for the `python-backend` cluster. The framework, testing, security, and ML spokes
all depend on these conventions — keep them consistent here so no spoke contradicts another.

## 1. The decision this cluster turns on: a thin adapter over a typed core

Every spoke assumes the same layering. The HTTP/task layer is **thin**; it parses, validates,
delegates, and serializes. Business logic lives in plain, typed, testable Python that knows
nothing about the request:

```
Request ──> Boundary (validate + parse) ──> Service / domain (typed, framework-free) ──> Persistence
                  ▲                                   │
              serialize ◄────────── typed result ◄────┘
```

- **Boundary** — DRF serializers (Django) or Pydantic models (FastAPI) validate *every* input and shape *every* output. Raw ORM objects, secrets, and framework globals never cross into a response schema. → `django-patterns`, `fastapi-patterns`
- **Service / domain** — pure Python, fully type-hinted; this is what the tests target directly. → `python-patterns`, `python-testing`
- **Persistence** — ORM (Django) or explicit DB dependencies (FastAPI); kept behind the service, never called from a view.

**Rule:** if logic can live in a framework-free function, it does. Views/routers stay skimmable.

## 2. The framework choice (Django vs FastAPI)

The cluster's first fork. Pick the lane, then stay in it.

| Pick **Django** when… | Pick **FastAPI** when… |
|---|---|
| You want batteries included: ORM, migrations, admin, auth, forms | You want an async-first, minimal service |
| Server-rendered pages **or** DRF REST API | Pure JSON API, OpenAPI/schema-driven |
| A relational data model is central | You compose your own DB/validation stack |
| Background jobs via Celery (`django-celery`) | High-concurrency I/O-bound endpoints (`async def`) |

Both follow §1. Django spokes are the deep lane here (patterns/TDD/security/celery/verification);
FastAPI is one consolidated spoke. Need ranking/feed logic behind either → `recsys-pipeline-architect`.

## 3. Testing & the verify gate (nothing is "done" untested)

- **TDD is the default** — red → green → refactor. Plain Python → `python-testing`; Django → `django-tdd` (pytest-django, factory_boy, DRF test client).
- **Target the service layer**, not the framework. Test transforms, branching, and contracts directly; use fixtures/mocks at the edges.
- **The gate before any PR or deploy**: environment → lint/format → type-check → tests + coverage → security scan → readiness. Django ships this as `django-verification`; for FastAPI/ML, run the same phases with the tools in §5.

## 4. Security & secrets (non-negotiable in production)

- `DEBUG` off; secrets from the environment, never committed. → `django-security`
- Validate at the boundary (§1) — defense against SQLi/XSS/mass-assignment starts there.
- Auth/authz explicit per endpoint; CSRF for cookie-session apps; HTTPS-only cookies + HSTS in prod.
- For ML, treat artifacts/datasets/prompts/logs as a security surface (secrets, PII, unsafe deserialization). → `mle-workflow`

## 5. Version / tooling matrix

| Concern | Default tool | Spoke |
|---|---|---|
| Language | Python 3.11+, full type hints | `python-patterns` |
| Tests | pytest (+ pytest-django for Django) | `python-testing`, `django-tdd` |
| Test data | factory_boy | `django-tdd` |
| Lint / format | ruff + black | `python-patterns`, `django-verification` |
| Type check | mypy | `python-patterns`, `django-verification` |
| Web (batteries) | Django + DRF | `django-patterns` |
| Web (async) | FastAPI + Pydantic v2 | `fastapi-patterns` |
| Async tasks | Celery + Redis/RabbitMQ | `django-celery` |
| ML training | PyTorch (device-agnostic, seeded) | `pytorch-patterns` |
| ML system | data contracts, eval gates, rollback | `mle-workflow` |
| Ranking/feed | six-stage pipeline | `recsys-pipeline-architect` |

## 6. Shared guardrails

- **Thin adapter**: no business logic in views/routers; logic is framework-free and typed.
- **Validate at the boundary**: DRF serializers / Pydantic models on every input *and* output; the client is untrusted.
- **No raw ORM / secrets in responses**; explicit `response_model` / serializer fields only.
- **Untested = unfinished**: TDD by default; the verify gate (§3) must pass before PR/deploy.
- **Prod hygiene**: `DEBUG=False`, env-sourced secrets, secure cookies/HSTS, explicit auth.
- **State scope changes**: a new external call, a loosened auth check, a skipped migration check, or an un-gated model promotion is a change worth saying out loud.
- **Django vs FastAPI**: choose once per service by §2; don't blend ORM-centric Django logic into an async FastAPI router or vice versa.
