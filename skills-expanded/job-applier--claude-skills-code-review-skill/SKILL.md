---
name: code-review
description: Perform a full code review of the currently checked out branch against main. Analyzes best practices, unit tests, DRY code, architecture, error handling, correctness & caller-impact, documentation, DB migration safety, and SvelteKit conventions across the diff for this Python (FastAPI/SQLModel) + SvelteKit project. Use when the user asks to review the branch, review a PR, or do a code review.
---

# code-review

Perform a comprehensive code review of all changes on the currently checked out branch compared to `main`. Scope is limited to the branch diff — for a whole-codebase audit, use `/codebase-audit` instead.

This is a mixed-stack repo: a Python 3.12 backend (FastAPI, SQLModel over SQLite, a `typer` CLI exposed as `job-applier`) under `src/job_applier/`, and a SvelteKit frontend (Svelte 5 runes, TypeScript) under `web/src/`. Reviews must cover whichever side(s) the diff touches.

## When to Use
- User asks to review the current branch or an open PR
- User asks for a code review before merging
- User invokes `/code-review`

## Instructions

### Step 1: Identify Changes

Determine the diff between the current branch and `main`:

```bash
git diff main...HEAD --name-only
git diff main...HEAD --stat
```

If there are no changes vs main, inform the user and stop.

Collect the full diff for context:

```bash
git diff main...HEAD
```

### Step 2: Spawn Parallel Review Agents

Launch **nine** agents in parallel using the Agent tool (subagent_type: `general-purpose`). Each agent receives the list of changed files and the full diff, and is responsible for one review category.

**Critical preamble — include in every agent prompt:**

> You are performing an exhaustive code review of a Python (FastAPI / SQLModel / typer) + SvelteKit (TypeScript, Svelte 5 runes) project. You must check EVERY item in the checklist below — do not skip items or stop early. For each item, read the relevant code and report either a finding or "PASS". When an item asks you to grep or search, you MUST actually run the search and report the results — do not assume. Your review must be deterministic: given the same code, you should always find the same issues.

**Each agent returns a structured report with:**
- Severity: `critical`, `warning`, or `suggestion`
- File path and line number (or range)
- Clear description of the issue
- Suggested fix or code snippet when appropriate

---

#### Agent 1: Test Quality & Coverage

1. **Read [CLAUDE.md](../../../CLAUDE.md)** — backend tests are `pytest` in `tests/test_<name>.py`, use fixtures from `tests/conftest.py` (e.g. the `make_raw` `RawJob` factory) and `@pytest.mark.parametrize` for table-driven cases; frontend tests are `vitest` in `web/src/lib/*.test.ts` or `web/src/lib/__tests__/*.test.ts` using `@testing-library/svelte`. Test command: `make test` (`make test-api` = pytest, `make test-web` = vitest).

2. **List all changed source files** under `src/job_applier/` (`.py`) and `web/src/` (`.ts`, `.svelte`, excluding `*.test.ts`). For EACH:
   a. Search for a corresponding test (`tests/test_<module>.py` for backend; colocated `*.test.ts` for frontend helpers). Report whether one exists.
   b. If a test exists, read it. Verify every new/changed public function, API endpoint, filter rule, source adapter, or exported helper has at least one test.
   c. If NO test file exists, flag per user preference ("always write tests"): new modules / new filter rules / new API routes / new source adapters = `critical`; new public functions on existing modules = `warning`; cosmetic-only = `suggestion`.

3. **Read every changed test file.** For each test:
   a. Assertions must test **outcomes** (returned `FilterResult.status`, persisted rows, response bodies, store state), not implementation details.
   b. Flag tests that only assert "is not None" / "does not raise" without checking behavior.
   c. Prefer fixture reuse: flag backend tests that hand-roll a `RawJob` instead of using the `make_raw` factory when the factory would do.
   d. For filter-rule changes, flag missing parametrized cases — the existing suite pins both pass and drop directions per rule; new rules should follow suit.
   e. Frontend: flag component/store tests that don't exercise the runes-driven state transition they claim to cover.

4. **For every new `if` / `match` / early-return branch added in the diff:** check that at least one test exercises it. Untested filter outcomes (`passed` / `manual` / `dropped`) or error branches → `warning`.

5. **For every new API endpoint, CLI command, or source adapter:** check that a test covers the success path AND at least one failure/validation/empty-result path.

---

#### Agent 2: DRY Code

1. **Read every changed source file (not tests)** under `src/job_applier/` and `web/src/`. For each:
   a. Any code block (3+ lines) repeated more than once in the same file → `warning`.
   b. Any block nearly identical to code in another changed file → `warning`.

2. **For each pattern found:** grep the full repo (`src/job_applier/`, `web/src/`) for ALL occurrences. Only flag if it appears 3+ times OR extracting it meaningfully reduces maintenance burden.

3. **Repeated string/integer literals** used as source names, filter reasons, status strings, API paths, or DB column names across changed files — flag magic values appearing 3+ times (they belong in a constant, enum, or the shared types in `web/src/lib/api.ts`).

4. **Source-adapter duplication:** the per-company adapters (`greenhouse`, `lever`, `ashby`, `workday`, `workable`, `smartrecruiters`) share shape via the `SourceAdapter` protocol in `src/job_applier/sources/base.py`. If the diff adds a new adapter or copies fetch/parse boilerplate that base helpers already provide, suggest consolidation.

5. **Do NOT flag:** test verbosity, trivial property/getter repetition, or two-site patterns in clearly different contexts.

---

#### Agent 3: Architecture

User is a senior engineer who values cohesive boundaries and dislikes god objects and shared-state desync. Weight findings accordingly.

1. **Read [CLAUDE.md](../../../CLAUDE.md)** — layering: FastAPI app + Pydantic schemas in `src/job_applier/api/`; the frontend talks to it only through `web/src/lib/api.ts`; source adapters implement the `SourceAdapter` protocol and register in `src/job_applier/sources/__init__.py`; the hard filter lives in `src/job_applier/filters/rules.py`; schema + migrations in `src/job_applier/models/db.py`.

2. **For every changed module:**
   a. **God object check:** lines of code, number of public functions, number of distinct responsibilities. Flag any module growing past ~400 lines or mixing clearly distinct concerns (e.g. HTTP fetching + parsing + persistence in one function).
   b. **Shared-state desync:** does the change introduce a new source of truth that duplicates state the DB already owns (scores, dedupe hashes, application status)? Flag as `critical` if two places now own the same data. Score writes must go through the active `MatchScore` + `MatchScoreHistory` snapshot path — flag direct mutations that skip history.
   c. **Layer coupling:** does new frontend code reach the backend by raw `fetch` instead of the typed `api` client in `web/src/lib/api.ts`? Flag as `warning`. (`api.ts` browser-safety is covered by Agent 9.)
   d. **LLM boundary:** the LLM is NEVER called server-side — scoring/drafting happen via slash commands in `.claude/commands/`. Grep the diff for `anthropic`, `ANTHROPIC_API_KEY`, or any server-side model call. Flag as `critical`.

3. **For new source adapters:** confirm they implement the `SourceAdapter` protocol and are registered in `sources/__init__.py`; per-company sources must read slugs from the `SourceSlug` table at runtime, not hardcode them (`companies.py` is seed-only). Flag deviations.

4. **Right shape for data:** backend — `SQLModel` table vs Pydantic schema vs plain dataclass (`RawJob`). Frontend — Svelte 5 rune store (`*.svelte.ts`) vs `+page.server.ts` loader data vs component-local state. Flag mismatches (e.g. cross-route state stuffed into a component instead of a rune store like `draftCart.svelte.ts`).

5. **Feature cohesion:** does the change place new files in the correct package (`api/`, `sources/`, `filters/`, `models/`) or route folder? Flag files that cut across boundaries without justification.

---

#### Agent 4: Python / TypeScript Best Practices

1. **Read [CLAUDE.md](../../../CLAUDE.md)** for project conventions. Lint is `make lint` (`ruff check src/`); frontend typecheck is `cd web && npm run check`.

2. **For every changed `.py` file:**
   a. **Type hints:** public functions have typed parameters and return types; modules start with `from __future__ import annotations` (established style across `src/job_applier/` and `tests/`). Flag missing as `warning`.
   b. **No bare `except:`** and no `except Exception` that silently swallows. (Error semantics in depth are Agent 5's job; here just flag the syntactic violation.)
   c. **No stray `print()`** in library code. Grep for `print(` in `src/job_applier/`; in CLI code use `typer.echo`, elsewhere use logging. `warning`.
   d. **f-strings** over `%`-formatting or `.format()` in new code. `suggestion`.
   e. **Ruff cleanliness:** flag unused imports, unsorted imports, unused variables that `make lint` would catch.

3. **For every changed `.ts` / `.svelte` file:**
   a. **Explicit types** on exported functions; no `any` leaking into the typed `api` surface. Flag `any` as `warning`.
   b. **`import type`** for type-only imports.
   c. **No `console.log`** left in committed code. Grep `web/src/` for `console.log(`. `warning`.
   d. Code should pass `npm run check` (svelte-check). Flag obvious type errors.

4. **Repo-specific hard rules (carry verbatim — these catch more than "follow conventions"):**
   a. **No `anthropic` SDK / API-key handling server-side** — grep new `.py` files for `import anthropic`, `from anthropic`, `ANTHROPIC_API_KEY`. Flag as `critical`. (See also Agent 3.)
   b. **No LinkedIn / Indeed scraping** — grep new source code (especially under `src/job_applier/sources/`) for `linkedin.com` / `indeed.com` endpoints or scraping logic. ToS violation and explicit project rule. `critical`.
   c. **Generated-draft purity** — if the diff touches `.claude/commands/draft.md` or draft-rendering code, confirm no em dashes (`—`), en dashes (`–`), or smart quotes (`"` `"` `'` `'`) are introduced into generated resume/cover-letter output rules. Grep these literal characters. `warning`.
   d. **No direct commits to main** — check the current branch is not `main`. If it is, flag as `critical` and stop review.

---

#### Agent 5: Error Handling

A focused pass on swallowed errors, unhandled failure paths, and incomplete returns. This is a baseline concern — never fold it into another agent.

1. **Read [CLAUDE.md](../../../CLAUDE.md)** for any error-handling / logging conventions.

2. **Fallible sinks across every changed file** — for each call below, confirm the result is checked or the exception is allowed to surface:
   - **Python:** `httpx` calls (`.get` / `.post` / `Response.raise_for_status`), `pypdf.PdfReader(...)`, `pdf.render_to_pdf(...)` (headless Chromium/Electron), `json.loads(...)`, `Path(...).read_text(...)`, `sqlmodel.Session.exec(...).one()` (raises on miss), and any subprocess call. Flag unguarded use where a failure would corrupt state or 500 a request. `warning` (or `critical` for ingest/dedupe data paths).
   - **TypeScript / SvelteKit:** `await request.json()` / `request.formData()` in actions without a try/catch or guard, `fetch(...)` without checking `response.ok`, loaders/actions with implicit `undefined` returns. Flag as `warning`.

3. **Swallowed errors:**
   - Python: grep changed `.py` for `except:` (bare), `except Exception: pass`, `except Exception: ...` that logs and falls through into invalid state, fire-and-forget cleanup.
   - TypeScript: grep `web/src/` diff for bare `catch {}` and `catch (e) { console.log(e) }` with no re-throw or recovery.
   A caught error must either recover, return a typed failure (e.g. `fail(...)` in form actions), or re-raise — never log-and-continue into an inconsistent state.

4. **Async/await failure paths:**
   - Python: `async def` endpoints that `await` without try/catch when downstream raises should map to a deliberate HTTP status, not a 500 + silent log.
   - TypeScript: form actions returning `fail(...)` on bad input (see the `VALID_STATUS` guard in `web/src/routes/jobs/[id]/+page.server.ts`); flag new actions that throw on user input instead of returning `fail()`.

5. **Incomplete return paths:** functions with a declared return type whose branches can fall through to implicit `None`/`undefined`. Flag inconsistent return paths as `warning`.

---

#### Agent 6: Correctness & Caller-Impact

Generic runtime-bug hunting plus the highest-value real-bug finder: checking every caller of every changed function. This is a baseline concern — never drop it, never merge it into a domain agent.

1. **Generic correctness bugs across the diff** — read each changed file and check:
   a. **Nullable / sentinel lookups used unguarded:**
      - Python: `dict.get(key)` → `None`, `re.search(...)` → `None`, `next(iter, default)` patterns, SQLModel `Session.get(Model, id)` → `None`. Flag dereference without a `None` guard → `warning` (or `critical` on a crash/data-corruption path).
      - TypeScript: `Array.prototype.find()` → `undefined`, `.indexOf()` → `-1`, optional-chaining gaps where a `null`/`undefined` would slip through.
   b. **Off-by-one:** loop bounds, `len(x) - 1`, range/slice endpoints, SQL `LIMIT` / `OFFSET`, inclusive-vs-exclusive mistakes (date ranges, score thresholds).
   c. **Inverted / incorrect boolean logic:** wrong negation, `and`/`or` precedence, comparison against the wrong constant or enum value (e.g. `FilterStatus.dropped` vs `FilterStatus.manual`, `ApplicationStatus` mismatches between Python and TS).
   d. **Type confusion masked by a cast:** a typed assignment that assumes a shape the data may not have — e.g. casting a `dict.get(...)` to a non-Optional type, TS `as` casts hiding `undefined`.

2. **Caller-impact analysis (do this thoroughly — it is the strongest bug finder here).** For EVERY function/method whose signature, return type, return-value semantics, error behavior, persisted-row shape, or response shape changed in the diff:
   a. Grep the ENTIRE repo (`src/job_applier/`, `web/src/`, `tests/`) for call sites. Report the count.
   b. For each caller, verify it still passes correct args, handles the new return type/shape, and accounts for any newly introduced error path, early return, or `None`/`undefined` result.
   c. **Cross-language drift is in scope:** if a backend API endpoint's request/response shape changed, the typed `api` client in `web/src/lib/api.ts` and every `+page.server.ts` loader/action that calls it must be updated too. Flag mismatches as `critical`.
   d. Flag callers that will now break or silently misbehave as `critical`.

3. **Dangling references:** for any function, signal, constant, DB column, or enum value renamed or removed in the diff, grep for now-dangling references to the old name → `critical`.

4. **Partial-state transitions:** new branches that leave a row with some fields updated and others stale (e.g. updating `MatchScore` without snapshotting `MatchScoreHistory`, updating `Application.status` without `last_contact_at`) → `warning`.

---

#### Agent 7: Documentation

Both halves of this stack have a doc-comment convention (Python docstrings; JSDoc/TSDoc). Goal: catch **stale / wrong** docs, not just missing ones. Presence-only checks are cheap and miss real bugs — the high-value finds are tag-vs-behavior drift.

1. **Read [CLAUDE.md](../../../CLAUDE.md)** for any documentation rules. There is no `pydocstyle` / `eslint-plugin-jsdoc` enforcement in this repo, so do NOT demand docstrings everywhere. Use the lint config (or its absence) as a false-positive guard: don't flag missing docs the project deliberately doesn't require.

2. **Tag-vs-behavior cross-checks (highest value — apply to every changed function with a doc comment):**
   a. **Python `Raises:` / "Raises" lines** must match the actual `raise` statements in the body. Flag drift: `Raises: ValueError` on a function that actually raises `HTTPException`. `warning` (or `critical` if a caller relies on the doc).
   b. **Python `Returns:` / `:return:` text** must match the actual return type/shape. Flag a docstring saying "Returns the active MatchScore" when the function now returns `None` on miss.
   c. **Python `Args:` / `:param:` names and types** must match the signature. Flag renamed/added/removed parameters that the docstring still describes the old way.
   d. **TSDoc / JSDoc `@param` / `@returns` / `@throws`** in `web/src/` — same drift checks. `@throws {Error}` when the code throws a specific subclass (or doesn't throw at all) is a `warning`.

3. **Top-of-module / top-of-file rationale** in `src/job_applier/` and `web/src/`: a number of modules carry a short "what this is for" docstring (e.g. `web/src/lib/api.ts`'s "must stay browser-safe" comment). If the diff changes the module's actual responsibility, the lead-in docstring/comment must move with it — flag drift.

4. **Public-surface presence (soft check, no lint backing):** for new exported names in `src/job_applier/api/`, `web/src/lib/api.ts`, and any module declared as the public seam, a one-line docstring/JSDoc is recommended but not required. Flag missing as `suggestion`, never `warning` or above — there is no project rule mandating docs.

5. **`.claude/commands/*.md` slash commands** are the primary user-facing documentation for the LLM workflow. If the diff changes scoring rubric, drafting rules, or status transitions, confirm `match-pending.md` / `score-draft.md` / `draft.md` / `suggest-roles.md` are updated in step. Out-of-sync rubric files between `match-pending.md` and `score-draft.md` are a CLAUDE.md-flagged rule — flag as `warning`.

6. **README / CLAUDE.md drift:** if the diff adds a new make target, source adapter, or status state, confirm `README.md` and/or `CLAUDE.md` reflect it. `suggestion`.

---

#### Agent 8: DB Migration & Schema Safety

The project deliberately uses no alembic. Schema changes are hand-rolled idempotent `_ensure_*_columns()` helpers in `src/job_applier/models/db.py`, run on EVERY startup from `init_db()` (the block calling `SQLModel.metadata.create_all(engine())` then each `_ensure_*` helper). `make prune` lightens old rows but must preserve dedupe hashes. Get this wrong and a fresh `uv run job-applier init` or a returning user's DB silently diverges.

1. **Read the migration block in [src/job_applier/models/db.py](../../../src/job_applier/models/db.py)** — the `init_db()` function and every `_ensure_*_columns()` helper. Confirm the established pattern: read existing columns via `PRAGMA table_info(<table>)`, then `ALTER TABLE ... ADD COLUMN` only for missing ones.

2. **For every new or changed `SQLModel` table field in the diff:** there MUST be a matching `_ensure_*` helper that adds the column to an existing DB. A new field with no helper means returning users get a broken schema. Flag as `critical`.

3. **Idempotency:** every helper must guard with the `PRAGMA table_info` membership check before `ALTER TABLE`. Flag any unconditional `ALTER TABLE` (it will throw on the second startup) as `critical`.

4. **Wiring:** every new `_ensure_*` helper must actually be called from `init_db()`. Grep to confirm. An orphaned helper is a `critical` no-op.

5. **SQLite limits:** SQLite `ALTER TABLE` only reliably supports `ADD COLUMN`. Flag any attempt to drop, rename, or retype a column via raw SQL, or any added `NOT NULL` column without a default (existing rows will violate it) as `critical`.

6. **No alembic / ORM auto-migrate creep:** flag any introduction of alembic, `create_all` side effects that assume an empty DB, or migration logic outside `db.py`.

7. **Prune/dedupe safety:** if the diff touches `prune` or JD-dedupe logic, confirm dedupe hash columns (`cross_source_hash`, `jd_fingerprint`) and `duplicate_of` links are preserved, not cleared. Flag data loss as `critical`.

---

#### Agent 9: SvelteKit Frontend Conventions

Only run the substantive checks if the diff touches `web/`. If it doesn't, return "PASS — no frontend changes." The user is learning SvelteKit here and wants idiomatic patterns; convention drift is worth flagging even when it "works."

1. **Read [CLAUDE.md](../../../CLAUDE.md)** frontend section and skim [web/src/lib/api.ts](../../../web/src/lib/api.ts) for the established client shape.

2. **Mutations via form actions:** status changes and other writes must go through SvelteKit form `actions` in `+page.server.ts` (see `jobs/[id]/+page.server.ts`), NOT client-side `fetch`. Grep changed `.svelte` files for `fetch(` that performs a mutation. Flag as `warning`.

3. **Loaders, not onMount fetching:** page data should come from a `load` function in `+page.server.ts`, not `onMount`-driven client fetches. Flag client-side initial-data fetching as `warning`.

4. **`api.ts` must stay browser-safe** (this is the single highest-impact rule and gets its own check here, not in Architecture): grep `web/src/lib/api.ts` and anything it imports for `$env/dynamic/private`, `$env/static/private`, `node:`, `fs`, `path`, or any server-only import. Flag as `critical`.

5. **Typed client:** new backend calls from the frontend should go through a typed method on the `api` object in `api.ts` with a matching TypeScript type, not ad-hoc inline `fetch` + `any`. Flag untyped responses as `warning`.

6. **Svelte 5 runes:** cross-route shared state belongs in a rune store (`*.svelte.ts`, like `draftCart.svelte.ts`); reactive state should use `$state` / `$derived`, not legacy Svelte 4 stores (`writable`/`readable`) unless there's a reason. Flag legacy patterns in new code as `suggestion`.

7. **Form-action contract:** actions should validate input and return `fail(<status>, { error })` on bad input rather than throwing (see the `VALID_STATUS` guard in `web/src/routes/jobs/[id]/+page.server.ts`). Flag missing validation on new actions as `warning`.

---

### Step 3: Compile & Present Results

After all agents return:

**Deduplication:** multiple agents may flag the same issue. Keep the highest severity and most actionable description. Do NOT list the same issue twice.

**Pre-existing vs new:** clearly distinguish issues introduced by this branch from pre-existing issues in touched files. Downgrade pre-existing issues one severity level (critical → warning, warning → suggestion) unless they are data-corruption or schema-safety risks.

**Contradiction check:** scan all findings for contradictions (e.g., "remove X" vs "X is missing"). Resolve by picking the correct recommendation based on the full context.

**Prioritization:** within each severity, sort by category in this order: architecture > correctness > migrations > error-handling > tests > sveltekit > docs > DRY > best-practices.

```
## Code Review: [branch-name]

### Critical Issues
(Must fix before merging)
- [category] file:line — description

### Warnings
(Should fix — could cause problems)
- [category] file:line — description

### Suggestions
(Nice to have — improve code quality)
- [category] file:line — description

### Summary
- X critical, Y warnings, Z suggestions
- Overall: PASS / NEEDS WORK / BLOCK
```

**Verdict logic:**
- Any `critical` finding → **BLOCK**
- More than 3 `warning` findings → **NEEDS WORK**
- Otherwise → **PASS**

### Step 4: Auto-Fix on BLOCK / NEEDS WORK

If the verdict is **PASS**, stop here — present the report and you're done.

If the verdict is **BLOCK** or **NEEDS WORK**, do NOT ask permission. Immediately address every high-level item that drove the verdict:

- **BLOCK** → fix every `critical` finding.
- **NEEDS WORK** → fix every `warning` finding (criticals too, if somehow present).

**What counts as "high level":**
- All `critical` and `warning` items in the categories the review reported on (tests, DRY, architecture, best practices, error handling, correctness & caller-impact, documentation, migrations, SvelteKit).
- Do NOT auto-apply `suggestion` items — those wait for explicit user direction.

**Fix-vs-defer rubric.** Default to fixing. A finding is fixable when the correct change is determinable from the code and the review's own description — apply it. **"I'm not sure" is not a valid reason to defer:** if you're unsure how to fix a real finding, investigate (read the surrounding code, the callers, the tests) until you are sure, then fix it. Defer only for the specific reasons listed below — never out of uncertainty.

**How to address them:**
1. Group findings by file to minimize churn.
2. For each finding, make the smallest correct change that resolves the issue. Don't bundle unrelated cleanup.
3. Add or update tests when the finding is test-related (missing test file, untested branch, untested endpoint).
4. **Re-run the project's full verification, not just unit tests.** Run `make test` (both `test-api` pytest and `test-web` vitest). If frontend code changed, also run `cd web && npm run check` for svelte-check. If backend code changed, also run `make lint`. If anything fails, fix the failures before reporting done — do not stop at red.
5. Do NOT commit or push. Leave changes in the working tree so the user can review the diff.

**When to defer an item instead of fixing it:**
- The fix requires a product/design decision the user hasn't made.
- The fix would expand scope well beyond the current branch (e.g., refactoring a module that pre-dates this branch).
- The finding is on pre-existing code the branch only touched incidentally.
- The fix conflicts with an explicit choice the user defended earlier in the conversation.

Defer means: leave the code as-is and call it out in the final report. Do NOT silently skip. The defer reason must be one of the four above — never "unsure".

### Step 5: Final Report

After fixes land, report:

```
## Auto-Fix Report

### Fixed
- file:line — what changed and why (one line each)

### Deferred
- file:line — finding, and the specific reason it was deferred (must be one of the four defer reasons — never "unsure")
  - Suggested next step: how the user should approach it

### Verification
- make test: PASS / FAIL (with failing test names if FAIL)
- make lint (if backend changed): PASS / FAIL
- npm run check (if frontend changed): PASS / FAIL

### Remaining Verdict
- Re-state the verdict after fixes: PASS / NEEDS WORK / BLOCK, and what (if anything) still drives a non-PASS.
```

Keep the report tight. The user will read the diff for the details — the report is the index.
