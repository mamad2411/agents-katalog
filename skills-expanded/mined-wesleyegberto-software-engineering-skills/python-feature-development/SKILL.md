---
name: python-feature-development
description: Orchestrate end-to-end Python backend feature development from idea or plan to reviewed, committed code. Use this skill proactively when the user wants to implement a feature, endpoint, service, module, or integration in a Python application — even if they just say "implement this", "add this endpoint", "build this service", "develop this plan", or "create this API". Works with any Python framework (FastAPI, Django, Flask) and sync or async code. Spawns parallel specialist subagents for codebase exploration, architecture planning, implementation, testing, and code review, then guides the user through approval, commit, and optional PR creation.
license: MIT
metadata:
  author: Wesley Egberto
  version: "1.0.0"
  domain: backend
  triggers: Python, FastAPI, Django, Flask, feature, implement, build, endpoint, API, service, module, backend
  role: orchestrator
  scope: implementation
  output-format: code + summary
  related-skills: python-expert, python-design-patterns, python-project-structure, python-type-safety, python-testing-patterns, terminal-monitor
---

# Python Backend Feature Development Orchestrator

## Objective

Orchestrate the complete development of a Python backend feature — from requirements through architecture planning, implementation, testing, review, and delivery. Uses specialized subagents running in parallel where possible to accelerate the workflow without sacrificing quality.

---

## Subagent Team

This skill **starts a team of specialist subagents** to parallelize and accelerate the implementation. Before proceeding, inform the user which agents will be used:

```
This skill will coordinate a team of specialist subagents to implement your feature:

  🔍 Code Explorer        — maps the existing codebase, patterns, and impact areas
  🏗️  Backend Architect    — designs the module structure, API, data model, and security
  🐍 Python Developer     — implements routes/views, services, repositories, and models
  🧪 Test Automator       — writes unit, integration, and API tests
  🔎 Code Reviewer        — reviews for correctness, security, performance, and consistency

Agents run in parallel where possible to save time.
Each agent will open in a dedicated terminal pane (tmux or iTerm2) so you can follow progress in real time.

Shall I start the team and begin the feature development workflow?
1. Yes — let's go
2. No — I'll implement manually
```

Use `AskUserQuestion` to present this message and wait for confirmation before continuing.
If the user selects option 2, stop and let them proceed on their own.

---

## Terminal Monitoring

Each agent step MUST open a dedicated terminal pane before launching so the user can follow progress in real time.

use skill `programming-skills:terminal-monitor` — handles detection (tmux / iTerm2 / none) and pane opening. Call it once per agent with the parameters below.

### Pane parameters per step

| Step | `mode` | `label` | `pane-name` | `output-file` |
|------|--------|---------|------------|---------------|
| 2 – Code Explorer | `subagent` | `🔍 Code Explorer` | `🔍 explorer` | `.python-dev/02-codebase-analysis.md` |
| 3 – Backend Architect | `subagent` | `🏗️ Backend Architect` | `🏗️ architect` | `.python-dev/03-architecture.md` |
| 4 – Python Developer | `subagent` | `🐍 Python Developer` | `🐍 python` | `.python-dev/04-implementation.md` |
| 5a – Test Automator | `subagent` | `🧪 Test Automator` | `🧪 tests` | `.python-dev/05-quality.md` |
| 5b – Code Reviewer | `subagent` | `🔎 Code Reviewer` | `🔎 reviewer` | `.python-dev/05-quality.md` |

---

## CRITICAL BEHAVIORAL RULES

Follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.python-dev/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval using `AskUserQuestion`. Do NOT continue automatically.
4. **Halt on failure.** If any agent errors or a step cannot be completed, STOP immediately and ask the user how to proceed.
5. **Architecture before code.** The `backend-architect` step MUST complete and be approved before implementation begins. Do NOT skip or merge it with implementation.
6. **Never enter plan mode autonomously.** Do NOT call `EnterPlanMode` — this skill IS the plan. Execute it.

---

## Pre-flight Checks

### 1. Check for existing session

Check if `.python-dev/state.json` exists:

- If `status` is `"in_progress"`: Read it and ask the user via `AskUserQuestion`:

  ```
  Found an in-progress Python feature session:
  Feature: [name from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session to .python-dev/archive/)
  ```

- If `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.python-dev/` directory and `state.json`:

```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

The feature description (`$FEATURE`) is the full content of `$ARGUMENTS`.

---

## Phase 1: Discovery (Step 1) — Interactive

### Step 1: Requirements Gathering

Gather requirements through interactive Q&A using `AskUserQuestion`. Ask ONE question at a time — do NOT dump all questions at once.

**Questions to ask (in order):**

1. **Feature description**: "Describe the feature to be built. What is its purpose, and which package or module does it belong to?"
2. **API contract**: "Describe the API surface needed: HTTP methods, endpoint paths, request/response payloads. If there's an existing API spec (OpenAPI, Swagger), share it. If this is not a web-facing feature, describe the function/CLI signature instead."
3. **Acceptance criteria**: "What are the key acceptance criteria? When is this feature 'done'?"
4. **Data and persistence**: "What data needs to be persisted? Describe the data model — new tables/collections, fields, relationships. Share existing ORM models or schema if available (SQLAlchemy, Django ORM, Pydantic, etc.)."
5. **Integrations**: "Does this feature call external services, message queues (Celery, RQ, Kafka), third-party APIs, or other microservices? If so, describe the integration contracts."
6. **Non-functional requirements**: "Any NFRs to consider? (e.g., latency SLA, rate limiting, authentication/authorization requirements, async vs. sync execution, background job processing)"
7. **Out of scope**: "What is explicitly OUT of scope for this feature?"

After gathering answers, write:

**Output file:** `.python-dev/01-requirements.md`

```markdown
# Requirements: $FEATURE

## Feature Description

[From Q1]

## API Contract

[From Q2 — endpoints, methods, request/response shapes, or CLI/function signature]

## Acceptance Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Data and Persistence

[From Q4 — models, relationships, schema changes]

## Integrations

[From Q5 — external services, queues, third-party APIs]

## Non-Functional Requirements

[From Q6 — latency, rate limiting, auth, async execution]

## Out of Scope

[From Q7]
```

Update `state.json`: set `current_step` to 2, add `"01-requirements.md"` to `files_created`.

---

## Phase 2: Codebase Analysis (Step 2)

### Step 2: Codebase Exploration

Read `.python-dev/01-requirements.md`.

use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🔍 Code Explorer`, `pane-name: 🔍 explorer`, `output-file: .python-dev/02-codebase-analysis.md`

Launch the codebase explorer:

```
Agent:
  subagent_type: "programming-skills:code-explorer"
  description: "Explore Python codebase for $FEATURE"
  prompt: |
    You are a codebase explorer. Analyze this Python project to map existing
    patterns and identify exactly what needs to change to implement this feature.

    ## Feature Requirements
    [Insert full contents of .python-dev/01-requirements.md]

    ## What to explore and document:

    1. **Project structure**: Package/module layout — how routers/views, services,
       repositories, models, schemas, and config are structured. Note whether it's
       organized by layer or by domain/feature (`src/` layout, Django apps, etc.).

    2. **Framework and runtime**: Which framework is in use (FastAPI, Django, Flask,
       or none), Python version, and package manager (uv, poetry, pip). Note the
       `pyproject.toml` or `requirements.txt` structure.

    3. **ORM / Database layer**: Which ORM or query tool is used (SQLAlchemy, Django
       ORM, Tortoise, raw SQL via psycopg/asyncpg), how models/schemas are defined,
       and where migrations live (Alembic, Django migrations).

    4. **Routing patterns**: How routes/views are defined and registered, how path
       params, query strings, and request bodies are validated (Pydantic, DRF
       serializers, marshmallow).

    5. **Middleware / dependency patterns**: Authentication (JWT, session, OAuth),
       dependency injection (FastAPI `Depends`, Django middleware), validation,
       error handling middleware, logging setup.

    6. **Service layer patterns**: How business logic is organized, sync vs. async
       usage, how dependencies are composed or injected.

    7. **Error handling**: Custom exception classes vs. standard exceptions, how
       they're caught (global exception handlers, try/except patterns), response
       error shapes.

    8. **Testing patterns**: Test setup (pytest, unittest), how integration/API
       tests are structured (httpx `TestClient`, Django `TestCase`, fixtures,
       factories), mocking patterns, test file naming and location conventions.

    9. **Impact map**: List the specific modules/files/directories that will likely
       be created or modified for this feature, with a brief reason for each.

    Write your findings as a structured markdown document with clear headings.
    Focus on what a developer needs to know to implement this feature consistently
    with the existing codebase.
```

Save the output to:

**Output file:** `.python-dev/02-codebase-analysis.md`

Update `state.json`: set `current_step` to 3, add step 2 to `completed_steps`.

---

## Phase 3: Architecture Planning (Step 3)

### Step 3: Backend Architecture Design

Read `.python-dev/01-requirements.md` and `.python-dev/02-codebase-analysis.md`.

use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🏗️ Backend Architect`, `pane-name: 🏗️ architect`, `output-file: .python-dev/03-architecture.md`

Launch the architecture agent:

```
Agent:
  subagent_type: "backend-architect"
  description: "Design Python backend architecture for $FEATURE"
  prompt: |
    You are a backend architect. Design the detailed technical architecture for this
    Python feature, grounded in the existing codebase patterns.

    ## Feature Requirements
    [Insert full contents of .python-dev/01-requirements.md]

    ## Existing Codebase Patterns
    [Insert full contents of .python-dev/02-codebase-analysis.md]

    ## Architecture Deliverables

    Provide ALL of the following:

    ### 1. Module / Component Design
    Map each component that needs to be created or modified:
    - **Router/View**: route paths, HTTP methods, request validation, response shapes
    - **Service(s)**: business logic responsibilities, sync/async boundaries, transaction handling
    - **Repository / Data access**: query patterns, ORM usage
    - **Model / Schema**: data structure, field types, validations, relationships (ORM model + Pydantic/serializer schema)
    - **Dependencies / Middleware**: any new dependency injections or middleware needed (auth guards, rate limiting, logging)

    ### 2. Data Model
    - New tables/collections with field definitions and types
    - Relationships (foreign keys, many-to-many, embedded documents)
    - Indexing strategy for query performance
    - Migration content (Alembic revision, Django migration)

    ### 3. API Design
    - Complete REST API specification: endpoint, HTTP method, request body schema,
      response schema, HTTP status codes, error responses
    - Pagination/filtering strategy if collections are returned
    - Input validation rules per field (Pydantic model / DRF serializer)

    ### 4. Security Design
    - Which endpoints require authentication/authorization
    - Role or permission requirements
    - Input sanitization strategy
    - Sensitive data handling (what NOT to return in responses)
    - Rate limiting if applicable

    ### 5. Integration Design
    - External service/queue contracts and how they will be called (sync HTTP client,
      Celery task, message broker)
    - Async vs. sync integration strategy
    - Resilience strategy (retries, circuit breakers, timeouts) if applicable

    ### 6. Risk Assessment
    - Technical risks and proposed mitigations
    - Known constraints or trade-offs

    Use the `Skill` tool with the following skills to guide your design decisions:
    - "software-architecture" — for architectural styles, patterns, and ADR guidance
    - "architecture-system-design" — for distributed systems and scalability decisions
    - "python:python-design-patterns" — for idiomatic Python structuring of the design

    Write your architecture as a single structured markdown document.
```

Save the output to:

**Output file:** `.python-dev/03-architecture.md`

Update `state.json`: set `current_step` to `"checkpoint-1"`, add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — Architecture Review

You MUST stop here. Present a concise summary and ask via `AskUserQuestion`:

```
Architecture design complete. Review .python-dev/03-architecture.md for full details.

Components: [list router/service/repository/model names from the design]
Data model: [summary of new models/tables and schema changes]
API: [list of new endpoints]
Security: [auth requirements summary]

1. Approve — proceed to implementation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 4 until the user selects option 1.
If they select option 2, revise `.python-dev/03-architecture.md` and re-checkpoint.
If option 3, update `state.json` status to `"paused"` and stop.

---

## Phase 4: Python Implementation (Step 4)

### Step 4: Implement the Feature

Read `.python-dev/01-requirements.md`, `.python-dev/02-codebase-analysis.md`, and `.python-dev/03-architecture.md`.

use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🐍 Python Developer`, `pane-name: 🐍 python`, `output-file: .python-dev/04-implementation.md`

Then launch the implementation agent:

```
Agent:
  subagent_type: "python:python-developer"
  description: "Implement Python feature: $FEATURE"
  prompt: |
    You are a senior Python backend engineer. Implement this feature based on the
    approved architecture and the existing codebase patterns.

    ## Feature Requirements
    [Insert full contents of .python-dev/01-requirements.md]

    ## Existing Codebase Patterns
    [Insert full contents of .python-dev/02-codebase-analysis.md]

    ## Approved Architecture
    [Insert full contents of .python-dev/03-architecture.md]

    ## Implementation Instructions

    1. Implement exactly what is specified in the architecture — router/view,
       service, repository, model, schema, dependencies.
    2. Match ALL existing code patterns from the codebase analysis: package layout,
       naming conventions, sync vs. async style, error handling approach, dependency
       injection style.
    3. Use type hints everywhere. Prefer async/await consistently if the project is
       async-first; do not mix sync blocking calls into async request handlers.
    4. Apply input validation on all incoming request data using the project's
       existing validation library (Pydantic, DRF serializers, marshmallow).
    5. Implement proper error propagation — raise typed/custom exceptions and let the
       global exception handler catch them, unless the project uses a different convention.
    6. Add database migrations as specified in the architecture, following the
       existing migration tooling and naming conventions (Alembic, Django).
    7. Add docstrings/comments only where business logic is non-obvious.
    8. Do NOT introduce new dependencies unless clearly necessary and explicitly
       approved in the architecture or already present in `pyproject.toml`.

    Use the `Skill` tool with the following skills as needed:
    - "python:python-design-patterns" — for idiomatic structuring and design patterns
    - "python:python-type-safety" — for type hints and static typing decisions
    - "python:python-async-patterns" — for async/await, concurrency, and background task patterns
    - "python:python-error-handling" — for exception hierarchies and error responses
    - "python:python-project-structure" — for package/module layout conventions
    - "python:django-expert" — if the project uses Django

    Write all code files directly to the project directory.
    After implementation, report a complete summary as a markdown document listing:
    - Every file created or modified (with path and brief description of changes)
    - Key implementation decisions and patterns used
    - Any deviations from the architecture and why
    - Database migration files created
```

Save the agent's summary to:

**Output file:** `.python-dev/04-implementation.md`

```markdown
# Implementation Summary: $FEATURE

## Files Created

- `app/features/feature/router.py`: Route definitions and request validation.
- `app/features/feature/service.py`: Business logic.
- `app/features/feature/repository.py`: Data access layer.
- `app/features/feature/schemas.py`: Pydantic request/response schemas.
- `alembic/versions/xxxx_add_feature_table.py`: Database migration.

## Files Modified

- `app/main.py`: Registered new feature router.
- `app/models/__init__.py`: Exposed new model.

## Key Decisions

- [Decision 1 and rationale]
- [Decision 2 and rationale]

## Deviations from Architecture

- [Any deviations and why — or "None"]
```

Update `state.json`: set `current_step` to `"checkpoint-2"`, add step 4 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — Implementation Review

You MUST stop here. Ask via `AskUserQuestion`:

```
Implementation complete. Review .python-dev/04-implementation.md for full details.

Files created: [count] | Files modified: [count]
Key changes: [2-3 bullet points of most important changes]
Migrations/schema updates: [list of files, or "None"]

1. Approve — proceed to testing and code review
2. Request changes — tell me what to fix
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 5 until the user selects option 1.

---

## Phase 5: Quality — Testing & Review (Step 5)

### Step 5: Parallel Testing and Code Review

Read `.python-dev/01-requirements.md`, `.python-dev/03-architecture.md`, and `.python-dev/04-implementation.md`.

use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🧪 Test Automator`, `pane-name: 🧪 tests`, `output-file: .python-dev/05-quality.md`
use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🔎 Code Reviewer`, `pane-name: 🔎 reviewer`, `output-file: .python-dev/05-quality.md`

Launch TWO agents in parallel in a single response:

**5a. Test Automator:**

```
Agent:
  subagent_type: "programming-skills:test-automator"
  description: "Create test suite for $FEATURE"
  prompt: |
    You are a Python test engineer. Create a comprehensive test suite for this
    Python backend feature.

    ## Requirements
    [Insert full contents of .python-dev/01-requirements.md]

    ## Architecture
    [Insert full contents of .python-dev/03-architecture.md]

    ## Implementation Summary
    [Insert full contents of .python-dev/04-implementation.md]

    ## Testing Instructions

    1. Write unit tests for all new service functions/methods using pytest.
       Mock all dependencies (repository, external services).
       Cover: happy path, business rule violations, edge cases
       (None inputs, empty collections, boundary values).

    2. Write unit tests for all new repository/data-access functions using an
       in-memory or test database (SQLite, test containers) if used in the project.
       Test query correctness, pagination, and filtering.

    3. Write integration/API tests for all new endpoints using the project's test
       client (FastAPI `TestClient`/`httpx.AsyncClient`, Django `TestCase`/`APIClient`).
       Cover: valid requests (201/200), validation errors (400/422),
       unauthorized access (401/403), not-found cases (404), server errors (500).

    4. Write at least one end-to-end integration test for the primary happy path
       using a real test database connection.

    5. Follow the existing test patterns, fixture usage, and directory structure
       from the codebase analysis.

    6. Target 80%+ coverage for new code.

    Use the `Skill` tool with:
    - "python:python-testing-patterns" — for pytest patterns, fixtures, mocking
    - "python:temporal-python-testing" — if the feature involves Temporal workflows

    Write all test files directly to the project directory.
    Report a summary of: test files created, what each covers, and any coverage gaps.
```

**5b. Code Reviewer:**

```
Agent:
  subagent_type: "programming-skills:code-reviewer"
  description: "Code review for $FEATURE"
  prompt: |
    You are a senior Python code reviewer. Perform a thorough review of this
    backend feature implementation.

    ## Requirements
    [Insert full contents of .python-dev/01-requirements.md]

    ## Approved Architecture (for conformance check)
    [Insert full contents of .python-dev/03-architecture.md]

    ## Codebase Patterns (for consistency check)
    [Insert full contents of .python-dev/02-codebase-analysis.md]

    ## Implementation Summary
    [Insert full contents of .python-dev/04-implementation.md]

    ## Review Dimensions

    Review ALL of the following dimensions. For each finding include severity
    (Critical, High, Medium, Low), the affected file:line if known, and a
    specific fix recommendation.

    1. **Correctness**: Logic errors, incorrect HTTP status codes, missing None
       checks, improper exception handling, blocking calls inside async functions.

    2. **Architecture conformance**: Does the implementation match the approved
       architecture? Check for layering violations (e.g., DB query in a view/router),
       missing components, or unapproved deviations.

    3. **Python patterns**: Missing type hints, mutable default arguments, improper
       use of `async`/`await`, unclosed resources (files, connections, sessions),
       overly broad `except` clauses.

    4. **Code consistency**: Does the code match the patterns documented in the
       codebase analysis? (naming, package layout, error handling, dependency style)

    5. **Security**: Missing input validation, SQL injection risks (raw queries),
       sensitive data exposed in responses, improper auth checks, missing rate
       limiting where required, insecure deserialization.

    6. **Performance**: N+1 query patterns (ORM lazy loading), missing pagination,
       synchronous blocking I/O in async paths, unnecessary data fetched from DB,
       missing indexes implied by query patterns.

    7. **Maintainability**: Overly complex functions, magic values that should be
       constants or settings, unclear variable names, duplicated logic.

    Format findings as a structured markdown list:
    ```
    - **Severity**: High
      **File**: `app/features/feature/service.py:54`
      **Finding**: Blocking DB call inside an async endpoint handler — no `await`,
        will block the event loop.
      **Fix**: Use the async session/engine and `await` the query, or run in a
        thread pool executor if the driver is sync-only.
    ```

    Use the `Skill` tool with:
    - "python:python-anti-patterns" — for common Python pitfalls and anti-patterns
    - "python:python-error-handling" — for exception design review
    - "python:python-performance-optimization" — for profiling and optimization checks

    Provide an overall assessment: Approved / Approved with minor fixes / Requires changes.
```

After both complete, consolidate into:

**Output file:** `.python-dev/05-quality.md`

```markdown
# Quality Report: $FEATURE

## Test Suite

[Summary from test automator — test files created, coverage areas, gaps]

## Code Review Findings

[Consolidated findings list from code reviewer]

### Overall Assessment

[Approved / Approved with minor fixes / Requires changes]

## Action Items (Critical & High severity)

[List of Critical and High findings that MUST be addressed before delivery]
```

**If Critical or High severity findings exist**, address them now:
1. Apply fixes directly or spawn a focused `python:python-developer` agent to fix them.
2. Update `.python-dev/04-implementation.md` with any additional files changed.
3. Re-run the code reviewer on the changed files only.

Update `state.json`: set `current_step` to `"checkpoint-3"`, add step 5 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — Quality Review

You MUST stop here. Ask via `AskUserQuestion`:

```
Testing and code review complete. Review .python-dev/05-quality.md for full details.

Tests: [number of test files created] test files
Code review: [count Critical] Critical | [count High] High | [count Medium] Medium findings
Overall assessment: [Approved / Approved with minor fixes / Requires changes]
Critical/High items addressed: [Yes / None found]

1. Approve — proceed to final delivery
2. Request changes — tell me what to fix
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 6 until the user selects option 1.

---

## Phase 6: Delivery (Step 6)

### Step 6: Summary, Review, and Commit

#### 6a. Generate Final Summary

Read all `.python-dev/*.md` files and write:

**Output file:** `.python-dev/06-summary.md`

```markdown
# Feature Delivery Summary: $FEATURE

## What Was Built

[2-4 sentence description of the feature and its business purpose]

## Files Created

[Complete list from 04-implementation.md + 05-quality.md test files]

## Files Modified

[Complete list of modified files]

## Database / Schema Changes

[List of migration files and what they do — or "None"]

## API Surface

[List of new endpoints: METHOD /path — brief description]

## Quality Assurance

- Tests: [list of test files and what they cover]
- Code review assessment: [overall assessment]
- Issues resolved: [list of Critical/High findings addressed, or "None found"]

## Points of Attention

[List any Medium/Low review findings NOT fixed — explain why deferred and recommended follow-up]
[Any known limitations, TODO comments, or tech debt introduced]
[Any deviations from requirements and why]

## Impact Map

[Which modules and parts of the application were touched and how they interact]

## How to Test Manually

1. [Step 1 — e.g., "Install dependencies: uv sync"]
2. [Step 2 — e.g., "Run migrations: alembic upgrade head"]
3. [Step 3 — e.g., "Start server: uvicorn app.main:app --reload"]
4. [Step 4 — e.g., "Call the endpoint: curl -X POST /api/features ..."]
5. [Step 5 — edge cases to verify manually]
```

Present the summary to the user and ask via `AskUserQuestion`:

```
Feature implementation is complete. Here's what was built:

[Paste "What Was Built", "API Surface", and "Points of Attention" sections inline]

Please:
1. Review the code in the files listed above
2. Run the test suite: [insert the project's test command, e.g., `pytest`]
3. Perform manual verification using the steps in .python-dev/06-summary.md

When you're ready:
1. Approve — commit the changes
2. Request changes — tell me what to fix
3. Abort — discard all changes
```

Wait for user response. If they request changes, implement them and return to this checkpoint.

#### 6b. Commit

Once the user approves:

1. Run `git status` to confirm the changed files match the implementation summary.
2. Stage all implementation and test files explicitly (do NOT use `git add .`).
3. Check recent `git log` to match the project's commit message convention. Then commit:

```
feat(<module>): [brief description of the feature]

- [Key change 1]
- [Key change 2]
- [Key change 3]
- Add migration: [migration file name if applicable]

Co-Authored-By: Claude Code
```

4. Confirm the commit succeeded with `git status`.

Then ask via `AskUserQuestion`:

```
Changes committed successfully.

Branch: [current branch name]
Commit: [commit hash and message]

Would you like to open a Pull Request?

1. Yes — create a PR now
2. No — I'll open the PR manually later
```

#### 6c. Pull Request (if requested)

If the user says yes, create the PR using `gh pr create`:

- **Title**: `feat(<module>): [feature name]` (short, under 70 characters)
- **Body**: Include What Was Built, API Surface, files changed, how to test manually, and Points of Attention from `.python-dev/06-summary.md`

Return the PR URL to the user.

---

## Completion

Update `state.json`:

```json
{
  "status": "complete",
  "last_updated": "ISO_TIMESTAMP"
}
```

#### Move artifacts to feature docs folder

Derive the feature folder name from `$FEATURE`: lowercase, spaces replaced by hyphens, special characters removed (e.g., `"User Authentication"` → `user-authentication`). Call this `$FEATURE_SLUG`. Also capture today's date as `$DATE` (format `YYYY-MM-DD`).

Create the destination directory and move all generated files:

```bash
DATE=$(date +%Y-%m-%d)
mkdir -p .specs/features/$DATE-$FEATURE_SLUG/artifacts/python
mv .python-dev/01-requirements.md      .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/
mv .python-dev/02-codebase-analysis.md .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/
mv .python-dev/03-architecture.md      .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/
mv .python-dev/04-implementation.md    .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/
mv .python-dev/05-quality.md           .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/
mv .python-dev/06-summary.md           .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/
mv .python-dev/state.json              .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/
```

After moving, remove the now-empty `.python-dev/` directory:

```bash
rmdir .python-dev
```

Present the final message:

```
Python backend feature development complete: $FEATURE

Artifacts saved to .specs/features/$DATE-$FEATURE_SLUG/artifacts/python/:
- 01-requirements.md      — Requirements
- 02-codebase-analysis.md — Codebase exploration
- 03-architecture.md      — Backend architecture design
- 04-implementation.md    — Implementation summary
- 05-quality.md           — Tests & code review
- 06-summary.md           — Final delivery summary

Next steps (if any):
[List any deferred items from points of attention]
```
