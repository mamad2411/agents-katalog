---
name: python-backend-orchestrator
description: "Route a Python backend task to the right specialist — idiomatic Python, pytest/TDD, the Django stack (patterns, TDD, security, Celery, verification), FastAPI services, and the ML lane (PyTorch, recsys pipelines, MLE workflow). USE WHEN building, testing, securing, or shipping a Python web/ML backend but the specific framework or concern hasn't been named yet."
cluster: python-backend
version: 1.0.0
---

# Python Backend Orchestrator

The single entry skill for Python server-side and ML-engineering work. It locates the task on
the **framework × lifecycle** map and delegates to one of 11 specialist spokes. The
cross-cutting model every Python backend shares — *the web/API layer is a thin adapter over a
typed, tested core; validate at the boundary; gate every change through the test/verify loop* —
lives in `python-backend-core`; read it before choosing a framework or wiring persistence.

## Cluster map (spoke → role)

**Language foundation (framework-agnostic)**
- `python-patterns` — idiomatic Python, PEP 8, type hints, packaging, error handling.
- `python-testing` — pytest, TDD red/green/refactor, fixtures, mocking, parametrization, coverage.

**Django lane (batteries-included web)**
- `django-patterns` — project layout, DRF API design, ORM, caching, signals, middleware.
- `django-tdd` — pytest-django, factory_boy, testing models/views/serializers and DRF endpoints.
- `django-security` — auth/authz, CSRF, SQLi/XSS prevention, secure production settings.
- `django-celery` — background jobs, Beat scheduling, retries, canvas workflows, task testing.
- `django-verification` — the pre-PR/pre-deploy gate: migrations → lint → tests → security → readiness.

**FastAPI lane (async-first services)**
- `fastapi-patterns` — async endpoints, dependency injection, Pydantic request/response models, OpenAPI, security.

**ML / data lane**
- `pytorch-patterns` — device-agnostic, reproducible training loops, model architectures, data loading.
- `recsys-pipeline-architect` — the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect ranking/feed pattern.
- `mle-workflow` — production ML: data contracts, reproducible training, eval gates, deployment, monitoring, rollback.

**Python application surface (folded spokes)**
- `textual` — TUI (Text User Interface) apps with the Textual framework: App/Screen/Widget architecture, TCSS styling, reactive programming, workers, and `run_test`/pilot testing.

## Folded spokes

These spokes were folded into this cluster from the wider skill library. They share the cluster's
core contract (typed, tested core; validate at the boundary; gate every change through the
test/verify loop) and are routed exactly like the spokes above — loaded on demand by name.

- `textual` — building Python terminal UIs with Textual (widgets, screens, TCSS, reactivity, async workers, pilot-based tests).

## Picked-up spokes

Vetted standalone spokes picked up from the antigravity-awesome-skills library (MIT). They cover
backend-adjacent surfaces — CLI design, chat-bot/CRM integration backends, and a framework-upgrade
analyzer — and are loaded on demand by name exactly like every other spoke.

- `ai-native-cli` — the 98-rule design spec for CLI tools AI agents can safely invoke: JSON-first output, input contracts validated like a public API, fail-closed guardrails, exit codes, agent self-description (extends the cluster's "validate at the boundary" contract to the command-line surface).
- `discord-bot-architect` — production Discord bots in Discord.js (JS) and Pycord (Python): gateway intents, slash commands, interactive components, rate-limit backoff, and sharding.
- `slack-bot-builder` — Slack apps on the Bolt framework (Python/JS/Java): Block Kit UIs, interactive components, slash commands, event handling, and OAuth install flows.
- `hubspot-integration` — HubSpot CRM integration backends (Node.js + Python SDKs): OAuth, CRM objects, associations, batch operations, webhooks, and custom objects.
- `skill-rails-upgrade` — analyzes a Ruby on Rails app and produces an upgrade assessment: version detection, gem-compatibility checks, and selective config-file merging (cross-framework reference for backend upgrade planning).

## Routing rules by intent

- **"Write/refactor/review plain Python"** → `python-patterns` (+ `python-testing` for the tests).
- **"Set up tests / follow TDD"** → `python-testing` (Django app → `django-tdd` instead, for pytest-django + factory_boy + DRF).
- **"Build a web app / REST API"** → pick the lane: batteries-included, ORM, admin, server-rendered or DRF → `django-patterns`; async-first, OpenAPI-driven, Pydantic I/O, microservice → `fastapi-patterns`. (Tie-breaker in `python-backend-core`.)
- **"Background jobs / scheduled / async processing"** → `django-celery`.
- **"Lock it down / auth / production hardening"** → `django-security` (FastAPI security lives inside `fastapi-patterns`).
- **"Is it ready to ship?" / pre-PR / pre-deploy** → `django-verification` (the verify loop; non-Django → run the equivalent gate from `python-testing` + `mle-workflow`).
- **"Train a model / training loop / GPU"** → `pytorch-patterns`.
- **"Rank/recommend/feed — top-K for a (user, context)"** → `recsys-pipeline-architect`.
- **"Turn notebook code into a production ML system"** → `mle-workflow` (orchestrates `python-patterns`, `python-testing`, `pytorch-patterns` for the pieces).
- **"Build a terminal UI / TUI / interactive CLI app"** → `textual` (Textual widgets, screens, TCSS, reactive state, async workers; tests via `run_test`/pilot, built on the `python-patterns` + `python-testing` foundation).
- **"Make a CLI safe for AI agents to call / agent-friendly CLI spec"** → `ai-native-cli` (JSON-first output, validated input contracts, fail-closed guardrails, exit codes).
- **"Build a Discord bot"** → `discord-bot-architect` (Discord.js / Pycord, intents, slash commands, components, sharding).
- **"Build a Slack app / bot"** → `slack-bot-builder` (Bolt framework, Block Kit, slash commands, events, OAuth install).
- **"Integrate with HubSpot CRM"** → `hubspot-integration` (OAuth, CRM objects, associations, batch, webhooks, custom objects).
- **"Assess / plan a Rails upgrade"** → `skill-rails-upgrade` (version detection, gem compatibility, selective config merge).

## Standard flow

1. **Classify** the task: which lane (foundation / Django / FastAPI / ML) and which lifecycle stage (design → implement → test → secure → ship).
2. **Anchor on the core**: if it touches framework choice, boundary validation, persistence, or the test gate, pull the shared model from `python-backend-core` first.
3. **Delegate** to the spoke(s). Multi-step asks fan out in lifecycle order — e.g. "build and ship a Django API" → `django-patterns` → `django-tdd` → `django-security` → `django-celery` (if async) → `django-verification`.
4. **Return**: the chosen spoke(s), the framework lane, the test/security implications, and the next action.

## Guardrails

See `python-backend-core`. In short: **keep business logic out of views/routers** — they are thin adapters over a typed core; **validate every input at the boundary** (DRF serializers / Pydantic models), never trust the client; **tests before "done"** — no feature is complete until `python-testing`/`django-tdd` covers it and `django-verification` (or the lane's equivalent gate) passes; **secrets and DEBUG never ship** — `django-security` settings are non-negotiable in production; for ML, **reproducibility and a rollback path** gate promotion (`mle-workflow`). Don't silently widen scope: a new external call, a loosened auth check, or a skipped migration check is a change worth stating.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
