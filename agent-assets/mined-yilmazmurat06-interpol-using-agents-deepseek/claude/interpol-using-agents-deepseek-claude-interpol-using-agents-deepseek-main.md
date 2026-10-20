# CLAUDE.md — Interpol Red Notice Scraper
> This file is the constitution of the system. All agents read this file at the start of every session.
> The Orchestrator makes decisions based on the rules defined here.
> Any modification to this file requires Orchestrator approval.

---

## Project

**Goal:**
Retrieve full wanted-person data published by Interpol using a two-phase scraping approach, push it into a queue, consume it into a database, and display it via a web server with rich filtering — all running in a Docker environment.

**Requirements:**
- **Container A:** Two-phase scraper on a configurable interval:
  - Phase 1: Fetch all notice IDs from the list API (`GET /notices/v1/red`, paginated).
  - Phase 2: For each ID, fetch full detail from the individual API (`GET /notices/v1/red/{id}`). This is the only way to get charges, date of birth, place of birth, physical description, and arrest warrant details.
  - Jitter delays between ALL requests (list pages AND individual calls). Anti-bot detection must be avoided.
- **Container B:** Python web server. Listens to RabbitMQ, persists full notice details to PostgreSQL, stores raw payloads in MinIO, and serves an HTML page with rich filtering and alarm markers. Page auto-updates via SSE.
- **Container C:** RabbitMQ message broker.
- **Supporting services:** PostgreSQL (notice storage), MinIO (payload/image storage).
- All config via environment variables — no hardcoded values.
- OOP throughout.
- Full Docker + docker-compose setup.
- Documentation: `requirements.txt`, README, `.env.example`, tests.

**Stack:**
- Language: Python (all services)
- Queue: RabbitMQ
- Backend: Flask
- Database: PostgreSQL
- Object storage: MinIO
- Frontend: HTML/CSS/JS (Jinja2 templates)
- Container: Docker + docker-compose
- Testing: pytest + Playwright

---

## Interpol API Domain Knowledge

> These constraints MUST be read and internalized before writing any code.
> They are derived from real runtime failures — not assumptions.

### Akamai TLS Fingerprinting (applies to API AND images)
- The entire `ws-public.interpol.int` host is fronted by Akamai. Akamai applies **TLS fingerprinting** at the SSL handshake level, before any HTTP header is parsed. This blocks Python's `requests`, `urllib3`, `httpx`, and any other library that does not mimic a real browser's TLS handshake.
- This affects **both the API endpoints AND the image CDN** — anything served from `ws-public.interpol.int`.
- HTTP headers (User-Agent, Accept, Referer) alone cannot bypass this.
- **Design rule:** Every server-side fetch against `ws-public.interpol.int` MUST use `curl_cffi` with `impersonate="chrome120"` (or newer). This applies to:
  - The list endpoint (`/notices/v1/red`)
  - The detail endpoint (`/notices/v1/red/{id}`)
  - The image CDN (`/notices/v1/red/{id}/images/...`)
- **Design rule:** When `curl_cffi` is used, the `requests`-style exception classes (`requests.HTTPError`, `requests.RequestException`) do NOT exist on the `curl_cffi.requests` module. Catch `Exception` and inspect `getattr(exc, "response", None)` to differentiate HTTP errors from network errors.
- **Design rule:** When `curl_cffi.requests` is imported as `from curl_cffi import requests`, omit any hardcoded `User-Agent` header — the impersonation sets one automatically that matches the spoofed TLS fingerprint. A mismatch between UA and TLS fingerprint is itself a bot signal.
- **Design rule:** Browser `<img src>` requests to the CDN can also be blocked (Referer / fingerprint checks). For reliability, the Flask app MUST proxy image fetches: a `GET /api/thumbnail/<path:notice_id>` route fetches the CDN URL server-side via `curl_cffi` and streams the bytes back to the browser. Do NOT 302-redirect to the CDN URL.

### Notice IDs Contain Slashes
- Interpol entity IDs have the format `YYYY/NNNNN` (e.g., `2026/10847`).
- **Design rule:** Flask routes that include a notice ID must use `<path:notice_id>`, not `<notice_id>` — the default string converter rejects slashes. PostgreSQL primary keys store slashes as-is (no escaping needed).

### Nullable API Fields
- Several Interpol API fields are `null` for valid records. `forename` is null for single-name individuals (common in South Asian names). `charges`, `date_of_birth`, `place_of_birth`, `height`, `weight`, `distinguishing_marks` are all frequently null.
- **Design rule:** Never add a `NOT NULL` constraint to any column that maps to an Interpol API field. All external API fields must be nullable in the schema.

### Two-Phase API Design: List vs. Detail Endpoint
- The list endpoint (`GET /notices/v1/red`) returns **minimal fields only**: entity_id, forename, name, nationalities, thumbnail URL. It does NOT return charges, date of birth, physical description, or arrest warrant details.
- Full data is only available from the **individual detail endpoint**: `GET /notices/v1/red/{entity_id}` (e.g. `GET /notices/v1/red/2026-10847` — note the dash, not slash, in the URL path).
- The detail endpoint returns: `date_of_birth`, `place_of_birth`, `sex_id`, `height`, `weight`, `languages_spoken_ids`, `eyes_colors_id`, `hairs_id`, `distinguishing_marks`, `arrest_warrants` (list of `{charge, issuing_country_id}`).
- **Design rule:** Always call the detail endpoint for each notice to get charges and physical description. The list endpoint alone is insufficient.
- **Design rule:** The entity_id stored in the DB uses slashes (`2026/10847`), but the API URL path uses dashes (`/notices/v1/red/2026-10847`). Convert when building the URL: `entity_id.replace("/", "-")`.

### Anti-Bot / Rate Limiting
- The list API (`/notices/v1/red`) is paginated (max 160/page) and applies rate limiting.
- The individual detail API also applies rate limiting — jitter delays are required between individual calls too, not just between list pages.
- Requests must include a randomised jitter delay (1–3.5 s) between ALL API calls.
- The image CDN applies independent bot detection (see above).
- **Sustained-rate threshold:** Akamai blocks egress IPs for 5–10 minutes when the aggregate request rate exceeds roughly 10 req/s. The relevant knob is `concurrency / avg_jitter` — keep that quotient under ~10.
- **Design rule:** The scraper MUST implement a circuit breaker: after N consecutive HTTP 403s across all workers (default N=5), pause every request globally for 5–10 minutes. Without this, retries during a penalty window count as fresh offenses and deepen the block.

### 160-Record Cap and the Nationality-Sweep Workaround
- For any single query against `/notices/v1/red`, the API returns **at most 160 records regardless of `resultPerPage` or `page`**. `page=2` either returns empty or silently repeats the same 160 records.
- This means an unfiltered query can only ever see the latest 160 of ~6,400+ notices.
- **Design rule:** To achieve full coverage, the scraper MUST sweep over a filter dimension (nationality = ISO-2 country code) and deduplicate by `entity_id`. Each per-country query returns ≤160; aggregated they cover the full dataset.
- **Design rule:** When a per-country query also returns >160 (e.g. RU=2,652), sub-slice that country by `sexId` × narrow `ageMin`/`ageMax` buckets. Age buckets must be narrow enough (~3–5 years each) for high-volume combos to fit under 160. Records still over cap after this two-level sub-slice are recorded as "unreachable" and logged.
- **Design rule:** Do NOT rely on HAL `_links.next` as the pagination stop condition for this API — it is unreliable in combination with the 160 cap. Drive pagination by total count and dedupe.

### MinIO URLs Must Be Routable from the Browser
- MinIO runs inside Docker as `minio:9000`. Presigned URLs generated server-side use this internal hostname, which the browser cannot resolve.
- **Design rule:** Never store `http://minio:9000/...` URLs in the database. If images are stored in MinIO, expose them via a Flask proxy route (e.g., `GET /api/thumbnail/<path:notice_id>`) so the browser only sees `localhost` URLs.

---

## Implementation Patterns (Non-Negotiable)

> These are project-wide patterns that have caused real failures. Every agent must apply them.

### PSC-1: psycopg2 transaction-error containment
- After ANY exception inside a psycopg2 cursor block, the connection is left in `TRANSACTION_STATUS_INERROR`. EVERY subsequent statement on that connection fails with `InFailedSqlTransaction` until a `rollback()` is issued.
- **Pattern:** Every write method that uses a shared connection MUST wrap its body in `try: … self._conn.commit(); except Exception: self._conn.rollback(); raise`. Read methods MUST end with `self._conn.rollback()` to release the implicit SELECT transaction.
- **Pattern:** The `_cursor()` (or equivalent) helper SHOULD pre-emptively rollback if `conn.get_transaction_status() == TRANSACTION_STATUS_INERROR` before handing out a cursor — defensive against poisoning from elsewhere.

### PSC-2: RabbitMQ heartbeat is negotiated, not declared
- Pika's `params.heartbeat = N` is a CLIENT REQUEST. The actual heartbeat used is `min(server_default, client_request)`. The RabbitMQ 3.x default is 60s.
- **Pattern:** To get a non-60s heartbeat, BOTH sides must agree. In `docker-compose.yml` set `RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS: "-rabbit heartbeat <N>"`; in every pika `URLParameters` set `params.heartbeat = <N>` matching. 600s is a good default for long-idle consumers.
- **Pattern:** Every consumer MUST implement an outer reconnect loop that catches `pika.exceptions.AMQPConnectionError`, `ConnectionClosedByBroker`, and `StreamLostError`, then reconnects.

### PSC-3: Streaming producer (per-record publish)
- A batch publish at the end of a long scrape cycle means downstream consumers (and the UI) see nothing until the entire cycle completes.
- **Pattern:** The scraper's main loop SHOULD accept an `on_record` callback that the producer wires to `publish_notice`. Records flow into RabbitMQ as soon as they are built. The end-of-cycle batch publish is anti-pattern for cycles longer than ~1 minute.
- **Pattern:** Pika's `BlockingConnection` is NOT thread-safe. When the scraper fans out detail fetches across worker threads, the per-record publish callback MUST be serialized with a `threading.Lock`.

### PSC-4: Server-side pagination from day one
- A list endpoint that returns up to 1,000 rows is a temporary hack — the moment the dataset exceeds the cap, the UI silently truncates and "older entities disappear on reload."
- **Pattern:** The JSON list endpoint MUST accept `page` and `page_size` parameters, return `{notices, total, page, page_size, pages}`, and back it with a paired `count_notices(filters)` query. The UI MUST render pagination controls (compact list with ellipses) and reset to page 1 on filter change.
- **Pattern:** SSE inserts MUST be conditional — only prepend a new card if the user is on page 1 with no active filters, otherwise the visible page silently drifts.

### PSC-5: Healthcheck commands must exist in the image
- Minimal/distroless images (especially MinIO on ARM64) often lack `curl`, `wget`, and even `sh`. A healthcheck written for one architecture can fail silently on another.
- **Pattern:** Every healthcheck command MUST be either (a) a binary bundled in the image's official documentation, or (b) the image's own tool. Concrete fallbacks:
  - PostgreSQL: `pg_isready`
  - RabbitMQ: `rabbitmq-diagnostics ping`
  - MinIO: `mc ready local` (with `MC_HOST_local` env var set; `mc` is bundled in all RELEASE images)
  - Custom Python apps: `python -c "import socket; socket.create_connection(('localhost', PORT), 2)"`

### PSC-6: Concurrency must respect upstream rate
- A thread pool that does `concurrency × (1/jitter)` requests per second WILL trigger Akamai. Document the formula in the Hard Rules and enforce it in defaults.
- **Pattern:** Default `SCRAPE_CONCURRENCY=4` with `JITTER_MIN_SECONDS=0.3`, `JITTER_MAX_SECONDS=0.8` → ~7 req/s sustained. Document the relationship so the user understands the trade-off.

### PSC-7: Playwright tests must use BASE_URL env var
- The orchestrator runs `pytest tests/` on the local machine with `BASE_URL=http://localhost:<port>` pointing at the live Docker stack. Tests that hardcode `http://localhost:8080` or any fixed URL break this contract.
- **Pattern:** Every Playwright test file MUST read the base URL from the environment:
  ```python
  BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")
  ```
- **Pattern:** `tests/requirements.txt` MUST include `playwright` and `pytest-playwright` so the live test runner can install dependencies before running.
- **Pattern:** `page.goto(BASE_URL)` — not `page.goto("http://localhost:8080")`. Any hardcoded URL is a PSC-7 violation and will be caught by `audit_hard_rules.sh`.
- **Pattern:** SSE endpoints (`text/event-stream`) are infinite streams. Playwright's `page.request.get()` waits for the response body to complete, which never happens → 30s timeout. Test SSE by navigating to the page first (`page.goto(BASE_URL)`), then using `page.evaluate()` with JavaScript `fetch("/api/stream")` + `AbortController` — the same-origin fetch from the loaded page avoids CORS blocks that occur from `about:blank`. Read the headers, then abort before the timeout fires.

---

## Architecture

```
Container A (Scraper)
  └── Phase 1: GET /notices/v1/red (list) → all entity IDs
  └── Phase 2: GET /notices/v1/red/{id} (detail) → full data per notice
  └── Anti-bot jitter between ALL calls → RabbitMQ producer

Container B (Web Server)
  └── RabbitMQ consumer → PostgreSQL (full model) + MinIO (payloads)
  └── Flask → HTML (rich filtering, SSE auto-update, alarm markers)

Container C (RabbitMQ)
  └── Message broker

Supporting
  └── PostgreSQL  ← full notice records (incl. arrest_warrants JSONB)
  └── MinIO       ← raw notice payloads
```

---

## Engineering Decisions

> Project-specific technical decisions. Agents derive their implementation from
> this section — they do NOT redecide these. Skills carry the generic best-practice
> "how"; this section carries the project-specific "what".

### Python Runtime
- **Python version: 3.11** (all services)
- Base image for every Python container: `python:3.11-slim`
- No `latest` tag anywhere.

### Docker / Compose
- **Service list** (exactly 5):
  1. `container-a` — scraper / RabbitMQ producer (no exposed ports)
  2. `container-b` — Flask web server + RabbitMQ consumer (exposes web port to host)
  3. `rabbitmq` — message broker (management UI port exposed for debugging)
  4. `postgres` — notice persistence (DB port exposed for debugging)
  5. `minio` — object storage (S3 API + console ports exposed)
- **Healthchecks required on:** `rabbitmq`, `postgres`, `minio`
- **Healthcheck commands (binary-verified, see PSC-5):**
  - postgres → `pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB`
  - rabbitmq → `rabbitmq-diagnostics ping`
  - minio → `mc ready local` (with `MC_HOST_local` env var set in service environment)
- **`depends_on` graph:**
  - `container-a` → `rabbitmq` (service_healthy)
  - `container-b` → `rabbitmq`, `postgres`, `minio` (all service_healthy)
- **Named volumes** for all stateful services (postgres, rabbitmq, minio).
- All container-to-container connections by Docker service name (e.g. `rabbitmq:5672`, `postgres:5432`, `minio:9000`).
- **RabbitMQ heartbeat configured on BOTH sides** (see PSC-2):
  - `rabbitmq` service: `RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS: "-rabbit heartbeat 600"`
  - Every pika `URLParameters`: `params.heartbeat = 600`

### Entrypoints
- `container-a` runs `producer.py` (which drives `scraper.py`).
- `container-b` runs `main.py` (which boots Flask app + background consumer thread).

### Database
- PostgreSQL 16+ (use the official `postgres:16` image, pinned).
- Primary key: `notice_id TEXT` (slashes allowed; no NOT NULL on external API fields except `notice_id`, `name`, `created_at`, `updated_at`, `is_alarm`).
- `arrest_warrants` stored as `JSONB`.
- Arrays (`nationalities`, `languages`) stored as `TEXT[]`.

### Queue
- RabbitMQ 3.13+ (`rabbitmq:3-management` image, pinned).
- Main queue + DLQ (`<queue>.dlq`) declared on startup.
- Producer reconnect on connection drop.

### Object Storage
- MinIO (latest stable tag pinned, NOT `latest`).
- Bucket auto-created on container-b startup if missing.

### Web
- Flask web server, single process is acceptable for this project.
- SSE endpoint for live UI updates (no WebSocket).
- All API routes that accept a notice_id use `<path:notice_id>` (see Interpol API Domain Knowledge).
- **Server-side pagination from day one** (see PSC-4): `/api/notices` accepts `page`/`page_size`, returns `{notices, total, page, page_size, pages}`. UI renders compact pagination and resets to page 1 on filter change.
- **Image proxy via curl_cffi** (NOT 302 redirect): `/api/thumbnail/<path:notice_id>` fetches the CDN URL server-side using `curl_cffi` and streams the bytes back to the browser.
- **Live DB-total counter**: `/api/filters` includes `total_notices` (unfiltered DB count) so the UI's top-left stat reflects the absolute DB row count, not the visible page count.

### Scraper Defaults (Akamai-safe)
- `SCRAPE_CONCURRENCY=4`, `JITTER_MIN_SECONDS=0.3`, `JITTER_MAX_SECONDS=0.8` → ~7 req/s sustained. Stay under ~10 req/s to avoid Akamai blocks (see PSC-6).
- Circuit breaker threshold: 5 consecutive 403s → 600s global pause.

### Configuration
- Every credential, port, hostname, and tuning param read from environment variables.
- `.env.example` is the canonical inventory — every variable documented with a one-line comment.
- **Bidirectional env-var check is mandatory** (see DevOps skill): every `${VAR}` in compose ⇄ every `VAR=` in `.env.example` ⇄ every `os.environ[...]` in Python. Name mismatches (`JITTER_MIN` vs `JITTER_MIN_SECONDS`) are silently ignored values — a high-impact bug class.

---

## File Layout (canonical paths)

> Agents write to these exact relative paths under `/mnt/session/outputs/`.
> No agent should hardcode these paths in its own system prompt — derive them from here.

### Developer-owned
```
container_a/scraper.py
container_a/producer.py
container_a/requirements.txt
container_b/app.py
container_b/consumer.py
container_b/models.py
container_b/db.py
container_b/storage.py
container_b/main.py
container_b/requirements.txt
container_b/templates/index.html
tests/__init__.py
tests/test_scraper.py
tests/test_consumer.py
tests/test_ui.py
```

### DevOps-owned
```
container_a/Dockerfile
container_b/Dockerfile
docker-compose.yml
.env.example
README.md
```

### Research-owned
```
research/<target-name>-constraints.md   (one per external system)
research/index.md
```

### QA-owned
```
tests/__init__.py
tests/test_scraper.py
tests/test_consumer.py
tests/test_ui.py
```

---

## Agents

### Agent 0 — Research
**Model:** claude-sonnet-4-6
**Role:** Probes every external system the project depends on BEFORE any code is written. Produces a constraints document per target that all downstream agents consume as authoritative ground truth.
**Tools:** read, write, edit, bash, web_fetch, web_search
**Owns:**
- `research/<target-name>-constraints.md` (one per external system)
- `research/index.md`

**Input:** `CLAUDE.md` (identifies in-scope external systems)
**Output:** Constraints documents written to `research/`
**Done signal:** Every external system named in CLAUDE.md has its own constraints document; every section of the SKILL's output format is filled or marked N/A.

**Why this exists:** This project does not maintain a `lessons-learned.md`. Every constraint a developer would otherwise discover by failing at runtime (pagination broken, auth missing, TLS fingerprinting, ID escaping, nullable fields) is discovered HERE, before the developer agent starts. Downstream agents read `research/` instead of accumulating bug history.

---

### Agent 1 — Developer
**Model:** claude-sonnet-4-6  
**Role:** Writes all Python application code following OOP principles.  
**Tools:** read, edit, write, bash, web_fetch, web_search (web access enabled for researching anti-bot strategies and library docs)  
**Owns:**
- `container_a/scraper.py`, `container_a/producer.py`
- `container_b/consumer.py`, `container_b/app.py`, `container_b/models.py`, `container_b/db.py`, `container_b/storage.py`
- `container_b/templates/`
- `requirements.txt` (per container)

**Input:** `handoff/qa-to-dev.md` (bug report from QA, if any)  
**Output:** Final assistant message captured as `handoff/dev-to-qa.md`  
**Done signal:** All assigned features in `feature-list.json` have `status: "dev-complete"`

**Session behaviour:** The developer receives **all pending developer features in a single batch prompt** and implements them together. This avoids redundant context loading and produces cohesive, cross-feature code.

**Pre-implementation checklist (mandatory before writing any code):**
- [ ] Read the "Interpol API Domain Knowledge" section above
- [ ] Read every file in `research/` — every constraint there is a hard rule for your implementation
- [ ] For any external asset (image, file): obey the "Hard Rules for Downstream Code" section of the relevant constraints document
- [ ] For any database column from an external API: make it nullable
- [ ] For any Flask route that accepts an external ID: check if the ID can contain slashes

---

### Agent 2 — DevOps
**Model:** claude-sonnet-4-6  
**Role:** Builds and manages the Docker infrastructure and documentation.  
**Tools:** read, edit, write, grep, glob  
**Owns:**
- `container_a/Dockerfile`
- `container_b/Dockerfile`
- `docker-compose.yml`
- `.env.example`
- `README.md`

**Input:** `handoff/qa-to-devops.md` (QA pass confirmation) or direct task for devops-owned features (F007, F008)  
**Output:** Final assistant message captured as `handoff/devops-to-qa.md`  
**Done signal:** Docker and docs assets are complete for the assigned feature

**Note:** DevOps-owned features (F007 Docker infrastructure, F008 documentation) go **directly to DevOps** without a prior QA step — there is no developer code to review for these.

---

### Agent 3 — QA
**Model:** claude-sonnet-4-6  
**Role:** Writes and validates tests. Reports failures as structured JSON. Does NOT run live Docker containers — scope is static analysis, unit/integration test authoring, and requirements.txt auditing.  
**Tools:** all (always_allow)  
**Owns:**
- `tests/test_scraper.py`
- `tests/test_consumer.py`
- `tests/test_ui.py` (Playwright)
- `handoff/qa-to-dev.md`
- `handoff/qa-to-devops.md`

**Input:** `handoff/dev-to-qa.md`  
**Output:** Final assistant message ending with exactly `Verdict: PASS` or `Verdict: FAIL`  
**Done signal:** All done criteria for the feature are validated; verdict written

**QA scope:** QA writes tests, runs unit/integration tests where possible, audits `requirements.txt`, and checks code structure against done criteria. It does **not** attempt to run `docker-compose up` or live E2E browser tests — those require a running cluster.

---

### Orchestrator
**Role:** State machine. Decides who runs and when. Reads and enforces CLAUDE.md.  
**Mode:** Hybrid — deterministic Python (`state_machine.py`) + LLM planning calls (`orchestrator.py`)  
**LLM calls:** Only at session start (planning), session end (summary), and when a feature is blocked (analysis)  
**Owns:**
- `orchestrator.py`
- `state_machine.py`
- `claude-progress.txt`
- `feature-list.json`
- `.claude/managed/agent_ids.json`

---

## Pipeline Flow

```
Session start
  └── Orchestrator LLM: session plan

  └── Research (ONE session, runs once per project — skipped if research/ already has constraints docs)
        └── Probes every external system → writes research/<target>-constraints.md

  └── Developer batch (ONE session for all pending developer features F001–F006)
        └── Reads research/ as ground truth
        └── Writes all Python code in a single pass

  └── Cross-functional review loop (max 3 rounds, stop on convergence)
        └── DevOps reviews developer code from infra perspective → findings
        └── QA reviews developer code from correctness perspective → findings
        └── If both reviewers report zero findings → exit loop (converged)
        └── Otherwise Developer fix pass on consolidated findings → next round

  └── QA verdict loop (max 3 iterations):
        └── QA (write tests, audit code, verify done criteria, issue Verdict: PASS/FAIL)
              ├── PASS → DevOps (integrate into Docker config)
              │           └── feature marked done
              └── FAIL → Developer fix (up to 3 iterations)
                          └── if still failing → feature marked blocked

  └── DevOps direct (F007, F008 — no QA step):
        └── Docker infrastructure + documentation → done

Session end
  └── Orchestrator LLM: session summary
```

**Status flow:** `pending` → `in-progress` → `dev-complete` → `qa-pass` → `done`  
**No agent may revert a status — only the Orchestrator can.**  
**Max iterations per feature: 3** — after 3 QA failures the feature is marked `blocked`.

---

## Handoff Format

Handoffs are **not written by agents**. The orchestrator captures each agent's final assistant message and writes the handoff file automatically.

```markdown
# Handoff: [Sender] → [Receiver]
**Feature:** F00X
**Date:** YYYY-MM-DD HH:MM
**Iteration:** N

## Completed
- ...

## Notes
- ...

## Open Issues / Bugs
- [ ] Bug 1: ...
```

---

## Global Done Criteria

A feature is not considered **done** until all of the following are satisfied:

- [ ] Code is working (pytest passes)
- [ ] All relevant environment variables are documented in `.env.example`
- [ ] Docker assets exist (`Dockerfile` per container, `docker-compose.yml`)
- [ ] Git commit made with feature ID in the commit message
- [ ] `feature-list.json` updated

> Note: Live `docker-compose up --build` and E2E Playwright browser tests are **not** run by agents — they require a running cluster. These are verified manually after the pipeline completes.

---

## Constraints (Non-Negotiable Rules)

1. **OOP is mandatory** — every service is class-based
2. **No credentials in code** — all config values come from `.env`
3. **Features are never deleted** — only their status changes
4. **Max iterations: 3** — if a feature fails 3 times it is marked `blocked` and the Orchestrator raises a flag
5. **Every session ends with a git commit** — incomplete work goes to a branch, never to main
6. **Agents never write to each other directly** — all communication goes through handoff files
7. **Orchestrator owns feature-list.json** — agents must not write to it; protected at download time

---

## Session Start Protocol

Every agent follows these steps at the start of every session:

```
1. Read CLAUDE.md
2. Read every file in research/ — authoritative ground truth for external system behavior
3. Read claude-progress.txt — what was done in the last session
4. Read feature-list.json — which features are pending or in-progress
5. Check own handoff folder — any pending messages?
6. Receive task from Orchestrator
7. Work
8. On completion: final assistant message becomes the handoff (orchestrator captures it)
```

> **No `lessons-learned.md`.** This project does not maintain a runtime-bug history. Every constraint that would otherwise become a lesson is discovered upfront by the Research agent and lives in `research/`. The pipeline targets one-shot production readiness — not iterative learning.

---

## Progress Log Format

`claude-progress.txt` is updated after every agent step:

```
[YYYY-MM-DD HH:MM] [AGENT_NAME] [FEATURE_ID] [STATUS]
Summary: ...
Next step: ...
---
```

---

## Observability

- **Live stdout:** `orchestrator.py` streams each agent's text output to the terminal in real time.
- **Progress log:** `tail -f claude-progress.txt` for structured per-step state.
- **Full traces:** Anthropic Console → Logs shows every session with prompt, tool calls, and response.

---

## Phase

**Current: Phase 1 — Deliver**  
Goal: Deliver the project in a working, tested, and dockerized state.  
Phase 2 (after delivery): Skill validator, optimizer, and Obsidian memory will be added.

---

## Workspace Structure

```
/
├── CLAUDE.md                  ← this file (constitution)
├── orchestrator.py            ← Managed Agents runtime + setup
├── state_machine.py           ← deterministic pipeline controller
├── claude-progress.txt        ← session log
├── feature-list.json          ← feature states (orchestrator-owned)
├── research/                  ← Research agent output (authoritative ground truth)
│   ├── index.md
│   └── <target-name>-constraints.md
├── handoff/
│   ├── dev-to-qa.md
│   ├── qa-to-dev.md
│   ├── qa-to-devops.md
│   └── devops-to-qa.md
├── container_a/
│   ├── Dockerfile
│   ├── scraper.py
│   ├── producer.py
│   └── requirements.txt
├── container_b/
│   ├── Dockerfile
│   ├── app.py
│   ├── consumer.py
│   ├── models.py
│   ├── db.py
│   ├── storage.py
│   ├── templates/
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
├── tests/
│   ├── test_scraper.py
│   ├── test_consumer.py
│   └── test_ui.py
├── .claude/
│   ├── agents/                ← .agent.md definitions
│   ├── skills/                ← skill reference docs
│   └── managed/
│       └── agent_ids.json     ← cached environment + agent IDs
└── README.md
```
