---
name: extract-conventions-emerging
description: Round-two extraction of EMERGENT conventions — patterns that recur 5+ times across the codebase but aren't documented anywhere (error shape, pagination shape, validation pattern, transaction boundaries, async-work naming, time/money/ID handling). Used by /setup-project Phase 2.10 in REFINE mode to upgrade round-one explicit-conventions detection (file naming, suffix matrix, base classes) with the implicit "this is how we always do X" rules that the team follows by habit.
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-conventions-emerging

## Purpose

Round-one Phase 2 detects *explicit* conventions: file-naming pattern, base classes, suffix matrix, test colocation. Those are the conventions a linter could check.

Round-two finds *emergent* conventions: patterns that aren't enforced by any tool but are followed by repetition, consistently enough that breaking them would feel wrong. Examples:

- "Every controller catches `ValidationError` and rethrows as `app.errors.BadRequest`."
- "Every list endpoint accepts `?cursor=<base64>` (never `?page=`)."
- "All money is `Decimal` (never `float`); all timestamps are UTC ISO 8601."
- "Background tasks live in `app/tasks/<feature>_tasks.py` (never `app/jobs/` or `app/workers/`)."

These are the conventions a senior engineer learns by code review, not by reading a CONTRIBUTING.md. REFINE makes them explicit.

## Premise

- Real source is the truth. Sample the actual files for each category — controllers for error-shape, list endpoints for pagination, route handlers for validation, log call sites for logging shape, transaction-opening points for boundaries.
- Every recorded pattern cites ≥3 representative `<file:line>` occurrences from the count claimed.
- The `min_occurrences` threshold is enforced from real reads, not estimates; auto-generated code (migrations, OpenAPI clients, `__generated__/`) is excluded.
- Empty extraction is honest — the negative finding per Category I is itself useful (tells round-two NOT to invent uniformity).
- Fabrication — naming a pattern from one beautiful example, or asserting uniformity across a genuinely heterogeneous codebase — locks the wrong rule into every downstream artifact.

## Mechanical halt

- Hand-wave in convention output — `etc.`, `...`, `most controllers`, `appears to use cursor pagination`, `roughly always`, a pattern entry without `citations:` populated to ≥3 `<file:line>`, a count without supporting samples — REFUSE to advance.
- Re-grep, re-count, regenerate the entry with explicit citations OR move it to `negative_findings`.
- If a category has fewer than `min_occurrences` real hits, record `<NOT-DETECTED: <category>: <N> occurrences below threshold>` — never round up an under-threshold pattern into `emergent_conventions`.
- Contested conventions (60/40 splits across the codebase) go in `contested_conventions` with both options + counts — not silently averaged into one rule.

## When to use

- `/setup-project --refine` Phase 2.10 — once per project.
- Manually when authoring `ai/conventions.md` for a project that has substantial code but the round-one auto-populated `conventions.md` reads as generic.

## Inputs

- `min_occurrences` (default: 5) — a pattern must appear ≥ N times to count as "emergent."
- `output_section` — section path (default: `## Conventions (emergent)`).

## Procedure

### Step 1 — Sweep for candidate categories

For each category, run a structured search:

#### Category A: Error-shape convention

- Sample 10 controller / endpoint files.
- For each: collect every `try/except` body (Python), `try/catch` body (TS/Java), `if err != nil` block (Go), `rescue` block (Ruby), `?`-propagated error (Rust).
- Group by raised exception type.
- A pattern emerges if ≥ 5 instances catch `<X>` and re-raise as `<Y>` (or return `<Z>` shape).

Record:
```
- "Catch `ValidationError` → raise `app.errors.BadRequest({code, message, fields})`" (5 occurrences in app/controllers/)
- "All API errors flow through `app.exceptions.handlers.handle_api_error` (12 occurrences via decorator @api_error_handler)"
```

#### Category B: Pagination convention

- Sample list endpoints (heuristic: GET handlers returning collections; resolver names matching `list*`, `find*`, `paginate*`).
- For each, identify the pagination scheme:
  - Offset-based: `?page=`, `?offset=`, `?limit=`.
  - Cursor-based: `?cursor=`, `?after=`, `?next=`.
  - Keyset-based: `?after_id=`, `?since=`.
  - None: returns full list.
- A pattern emerges if ≥ 5 endpoints use the same scheme.

Record:
```
- "All list endpoints use cursor-based pagination (?cursor=<opaque-base64>) — 8 occurrences. Cursor encoded by app/pagination.py:encode_cursor:23."
```

#### Category C: Validation library + decorator/serializer pattern

- Detect validation lib(s): `pydantic`, `class-validator`, `joi`, `zod`, `yup`, `marshmallow`, `cerberus`, `drf serializers`, `dry-validation`.
- For each handler/route, identify how validation is plugged in:
  - Body validation: decorator? framework-native (e.g. `@app.post(...)` with Pydantic type)? manual?
  - Query validation: decorator? type hint? manual?
  - Response validation: enabled? skipped?
- A pattern emerges if ≥ 5 endpoints use the same validation pattern.

Record:
```
- "Request validation: every controller method takes `body: <ModelName>Request` Pydantic type as first param after `request` (15 occurrences). FastAPI auto-validates."
- "Response validation: NOT enforced (response_model= is set on only 3 of 22 endpoints). Round-two finding for security artifact."
```

#### Category D: Logging shape

- Find logger imports + calls. Languages:
  - Python: `logging.getLogger(__name__)`, `loguru.logger`, `structlog.get_logger()`.
  - Node: `pino`, `winston`, `bunyan`, custom `logger.ts`.
  - Go: `slog`, `zap`, `logrus`.
- For each call, identify the structured fields passed: `logger.info('msg', user_id=..., request_id=..., event=...)`.
- A pattern emerges if ≥ 5 log calls use the same structured-field shape.

Record:
```
- "Structured logging: every logger call passes `{event: <verb-noun>, user_id, request_id, tenant_id?}` (32 occurrences). Use this shape for any new log call."
```

#### Category E: Transaction-boundary convention

- Find `with transaction.atomic()`, `await prisma.$transaction(...)`, `db.Transaction(func() ...)`, etc.
- Note WHERE the transaction is opened: in the controller? the service layer? the repository?
- A pattern emerges if ≥ 5 transactions are opened at the same layer.

Record:
```
- "Transactions opened in service layer (5 of 5 occurrences in app/services/*.py). Repository methods do not open transactions; controllers do not."
```

#### Category F: Async-work naming + location

- Find async / background-task definitions: `@celery.task`, `@bull.queue`, `Queue.add(...)`, `BackgroundTasks.add_task`, `Sidekiq::Worker`, `goroutine`-spawning helpers.
- Note their file location + naming convention.
- A pattern emerges if ≥ 5 tasks live in a consistent location with consistent naming.

Record:
```
- "Background tasks: live in app/tasks/<feature>_tasks.py (8 occurrences); naming: `<feature>_<verb>_task` (e.g. `billing_send_receipt_task`). Never in app/jobs/ or app/workers/ — those don't exist."
```

#### Category G: Time / money / ID handling

- Search for type imports:
  - `Decimal` (Python) / `BigDecimal` (Java) / `decimal.js` (Node) → money.
  - `uuid` / `ulid` / `nanoid` / sequential int → ID strategy.
  - `datetime.utcnow` / `dayjs.utc` / `time.Now().UTC()` / `Date.now()` (epoch) → timestamp strategy.
- A pattern emerges if ≥ 5 fields/columns use the same approach.

Record:
```
- "Money: always `Decimal(amount)` (NEVER `float`) — 14 occurrences in models. DB column type: `numeric(12,2)`. Currency is a separate `currency` ISO-4217 string column."
- "IDs: ULID (NOT UUIDv4) — 9 occurrences. Generated by app/ids.py:new_id:12. Stored as `varchar(26)` not `binary(16)`."
- "Timestamps: ISO 8601 UTC, stored as `timestamptz`, deserialized via `pydantic.AwareDatetime`. Naive datetimes are rejected at the boundary (12 occurrences of explicit `if not dt.tzinfo: raise ...`)."
```

#### Category H: Naming conventions emerging beyond the suffix matrix

- File-name patterns the round-one extraction missed (e.g. `*_repo.py` is documented; `*_query_builder.py` for shared query construction is emergent — found by grep but never described).
- Class-name patterns (e.g. every "translation handler" is named `Translate<Entity>Handler` — emergent if not enforced).

Record under `## Naming (emergent additions)`.

#### Category I: Negative findings

If a category genuinely has no emergent convention (codebase is heterogeneous on that axis), record it explicitly:

```
- "Pagination: NO consistent convention — 3 endpoints use ?page=, 2 use ?cursor=, 1 returns full list. Round-two recommendation: standardize. Until then, REFINE will not enforce a pagination shape in generated artifacts."
```

The negative finding is itself useful — it tells round-two NOT to invent uniformity.

### Step 2 — Output

Write to `.claude/_refine-extract.md` under `## Conventions (emergent)`:

```yaml
extraction_date: <YYYY-MM-DD>
strong_signals: ["error-shape", "pagination", "validation", "logging",
                 "transaction-boundary", "async-naming", "time-money-id"]
min_occurrences_threshold: 5

emergent_conventions:
  - category: error-shape
    pattern: <1-sentence rule>
    occurrences: <N>
    citations: [<file:line> x 3]
    confidence: <high|medium>   # high = ≥10 occurrences; medium = 5-9
  # repeat per pattern

negative_findings:
  - category: <which one>
    pattern: NONE
    note: <why — heterogeneous; mixed schemes; etc.>

# When > 1 pattern competes (e.g. 60% of code uses one error shape, 40% uses another):
contested_conventions:
  - category: <which>
    options:
      - { pattern: <A>, occurrences: <N>, sample: <file:line> }
      - { pattern: <B>, occurrences: <M>, sample: <file:line> }
    note: <recommendation — usually "the older subsystem uses A; new code uses B; consider migration">
```

## Quality gate

- **STRONG**: ≥ 4 emergent conventions found OR ≥ 3 emergent + ≥ 1 explicit negative finding.
- **WEAK**: < 3 emergent — flag `[REFINE-WEAK: emergent-conventions]`. Phase 4.7-DEEP enriches `ai/conventions.md` with explicit conventions from round-one only.

## Anti-patterns

- **Pattern from a single file** — even if the pattern is beautiful, 1 occurrence is not emergent. The threshold protects against extracting one engineer's preference as project canon.
- **Pattern from auto-generated code** — exclude `migrations/`, `__generated__/`, OpenAPI-generated clients, etc. They're consistent but not authored.
- **Pattern from imported third-party code** — only count this codebase's own files.
- **Forcing a pattern when there isn't one** — record negative findings explicitly. They're as informative as positive ones.
- **Citing only one occurrence per pattern** — the value is in showing the user "this is followed in 12 places, here are 3 representative ones." Single citation = appears like an example, not a convention.
