# CLAUDE.md — Confidence-Routed Document Extraction

## What This Project Does

An AI-assisted document extraction pipeline with a self-improving reliability model.

The core loop:
1. AI drafts field extraction from a document
2. Human reviews and approves (editing any wrong fields)
3. System records, per field, whether the human changed it ("touched" = 1, untouched = 0)
4. Change rates aggregate into a **per-field reliability model**
5. High-change-rate fields get flagged for mandatory human review on future documents; low-change-rate fields pass with lighter review

The training signal is free: the human's normal review edits are the ground-truth labels. No separate annotation step, no model self-confidence, no semantic diffing.

---

## Tech Stack

| Layer | Choice |
|---|---|
| API | FastAPI (async) |
| Data models | Pydantic v2 |
| Database | SQLite via raw `sqlite3` — deliberate POC choice, local testing only, no production target |
| Migrations | None — `create_all()` on startup; schema changes are manual for this POC |
| Task queue | ARQ (async Redis queue) — planned for Epic 2, not active yet |
| AI extraction | Anthropic Claude API (claude-sonnet-4-6 default) |
| Testing | pytest + pytest-asyncio |
| Linting | ruff |
| Type checking | pyright (strict) |

---

## Repository Structure

```
confidence-routed-extraction/
├── CLAUDE.md
├── pyproject.toml
├── src/
│   └── extraction/
│       ├── api/            # FastAPI routers
│       ├── core/           # Business logic (no framework deps)
│       │   ├── pipeline.py     # Draft → review → approval flow
│       │   ├── diff.py         # Touch detection
│       │   ├── observations.py # Per-field touch observations (Feature 2a)
│       │   ├── reliability.py  # Per-field-group scores + routing (Feature 2b)
│       │   └── config.py       # Effective persona + reference-doc composition (Feature 1a)
│       ├── schemas/        # Pydantic request/response schemas
│       ├── tasks/          # ARQ background tasks (Epic 2)
│       ├── backfill.py     # Derive observations for pre-2a approvals (Feature 2a)
│       └── db.py           # All sqlite3 (drafts, approvals, field_observations, config, reference_documents)
└── tests/
    ├── unit/
    └── integration/
```

**Rule:** Business logic lives in `core/` with no FastAPI imports. Routers are thin — they validate input, call core, return output.

**Rule:** All `sqlite3` calls live in `db.py`. No cursor or connection usage anywhere else in the codebase.

---

## Development Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # fill in ANTHROPIC_API_KEY
git config core.hooksPath .githooks   # enable the secret-scanning pre-commit hook (once per clone)
PYTHONPATH=src uvicorn extraction.api.main:app --reload
```

`.env` is loaded automatically at app startup via `python-dotenv` (`load_dotenv` in `api/main.py`); real environment variables take precedence over `.env`.

**Secret guard:** `.githooks/pre-commit` blocks commits that stage a real-looking secret (`sk-ant-`, `ghp_`, `github_pat_`, `AKIA…`, PEM private keys); obvious placeholders (e.g. `sk-ant-...`) are allowed. It activates only after the `git config core.hooksPath .githooks` step above — that config is local and does not travel with a clone. Bypass a false positive with `git commit --no-verify`.

The SQLite database (`drafts.db`) is created automatically on first startup — no migration step needed.

Run tests (`pythonpath = ["src"]` is set in pyproject.toml so no env var needed for pytest):
```bash
pytest                        # all tests
pytest tests/unit/            # unit only (no DB or API key required)
```

Type check and lint:
```bash
pyright src/
ruff check src/ tests/
```

---

## Development Lifecycle

This project follows a **define → plan → implement → verify → review → ship** cycle. Each stage has a specific gate before moving forward.

### Define
- All new features start with a written description of the field schema change, endpoint contract, or reliability model behavior being added.
- Open architectural questions (see below) must be explicitly resolved — or explicitly deferred — before implementation begins.
- CLAUDE.md is updated if a decision closes one of the open questions.

### Plan
- Use `/feature-dev` to explore the codebase and draft an implementation plan before writing code.
- Architectural decisions belong in the plan, not in comments or PR descriptions.
- DB schema changes are made directly in `db.py` (`CREATE TABLE` statements); no migration tooling exists for this POC.

### Implement
- New endpoints: router → schema → core logic — in that order.
- No business logic in routers. No `sqlite3` calls outside `db.py`.
- Pydantic models are the contract boundary: use them for all API input/output and for field schemas passed to the AI extraction step.
- Keep `core/` pure: no FastAPI, no `sqlite3` inside `core/pipeline.py`, `core/diff.py`, or `core/reliability.py`.

### Verify
- Every PR must pass: `pyright`, `ruff`, `pytest tests/unit/`
- Unit tests mock the Claude API and do not require a running DB or API key.
- Run `/security-guidance` before committing. (Configure as a hook once the repo is active.)

### Review
- Use `/code-review` for automated PR review before requesting human review.
- Reviewer checklist: core/router separation respected, Pydantic schemas complete, all `sqlite3` calls confined to `db.py`, touch-detection edge cases covered.

### Ship
- Use `/commit-commands` for commit, push, and PR creation.
- Squash-merge only. PR title = commit message.
- Tag releases that change the reliability model schema — downstream consumers depend on field routing behavior.

---

## Coding Conventions

**Async for HTTP and Claude API calls.** FastAPI route handlers and `anthropic` SDK calls are `async`. `sqlite3` is synchronous — calls go through `db.py` directly without asyncio wrappers (acceptable for this local POC).

**Pydantic v2 style.** Use `model_validator` and `field_validator`, not `validator`. Annotate with `Annotated[...]` for constraints.

**No bare `except`.** Catch specific exceptions. FastAPI exception handlers live in `api/exceptions.py`.

**Type everything.** pyright strict is the bar. No `Any` without a comment explaining why.

**Tests mirror src.** `tests/unit/core/test_diff.py` tests `src/extraction/core/diff.py`. Same path structure.

**No magic strings for field names.** Document field schemas are defined as Pydantic models or enums — never as free-form dict keys in business logic.

---

## Key Architectural Decisions (Locked)

These were evaluated and rejected — do not re-open without a strong reason:

- **Model self-reported confidence** — rejected. Models report high confidence on wrong answers. Not a reliable signal.
- **Logprobs / multi-sample agreement** — rejected. Proxies for uncertainty. We want measured correction history, not estimated uncertainty.
- **Semantic field diffing** — rejected. Too brittle ("B.S." vs "Bachelor of Science" is cosmetic, not an error). We don't need to know *how* a field changed — only *that* it did.
- **Touch definition:** deletions count as touched. Fields left blank by the AI that the human fills in count as touched. The question is "was this field ship-ready as drafted?" — a binary.

---

## Resolved Design Decisions (Epic 2 — locked 2026-06-25, closes #9)

**Unifying principle:** configurable defaults, with **"unproven → mandatory review"** as the
safe fallback everywhere. This single rule is the overfitting defense, the cold-start behavior,
and the graceful-degradation-on-new-inputs guarantee — the Vision Brief's biggest stated risk,
resolved in design. Any code computing or storing reliability scores must honor it.

**1. Reliability model granularity**
The grouping key is **configurable** (a list, e.g. `["field", "document_type"]`) — never a
hardcoded assumption. POC default: `field × document_type`. `field` alone is too coarse (a field
behaves differently by doc type — GPA on a transcript vs. a diploma); adding `× country`/`× language`
is too fine for POC data volume (buckets explode, none populate). Add levels to the key later when
data supports it. **Unseen buckets → mandatory review** until they clear the sample threshold (see
#3); a new country/type never inherits another bucket's score.

**2. Cosmetic edits**
Count **all non-whitespace touches** as signal (whitespace is already normalized out in Feature 1c).
Exposed as a documented flag `count_cosmetic_edits`, default `true`. Rationale: the question is "was
this field ship-ready as drafted?" — a reworded field wasn't, by the reviewer's standard, even if
technically correct. Distinguishing real error from cosmetic reword needs semantic judgment
(LLM-as-judge), reintroducing the complexity the binary approach exists to avoid. Semantic filtering
of cosmetic edits is **deferred** to a possible future iteration.

**3. Minimum sample threshold before routing decisions**
**Configurable** threshold; below it a bucket defaults to **mandatory review**. POC default:
**5 samples** — explicitly a *demonstrability* value (lets buckets cross the threshold on limited
POC data so routing behavior is observable), **not** a statistically sound one. Production would
need ~30+ for real confidence. Documented as such.

---

## Scope Boundary

**In scope:**
- Generic, domain-agnostic pipeline
- Any document type with discrete extractable fields (invoices, lab reports, intake forms)
- The draft → review → approval → touch-capture → reliability loop
- A routing decision per field based on reliability score + configurable threshold

**Out of scope:**
- Credential evaluation rules or academic equivalency logic
- CRM integrations (Salesforce, HubSpot, etc.)
- Any proprietary document formats or client-specific field definitions
- UI — this is an API; the review interface is assumed to exist externally
