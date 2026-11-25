---
name: python-code-quality-enforcement
description: >
  Python code quality and conventions for forge consumers. Tooling,
  layouts, coding standards, and security checks for all
  Python code.
  Triggers when writing or modifying Python code in a consumer codebase (MCA during coding); NOT for non-Python code or design-level decisions.
status: active
relevant_for: ["main-code-agent"]
invocation:
  primary: sub-skill
  secondary: [workflow-step]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: python-code-quality-enforcement

## Purpose

Enforce Python code quality and conventions for forge consumers.
Defines tooling, layouts, coding standards, and security checks for
all Python code in a consumer project.

Inspired by Trail of Bits' `modern-python` skill. Stack-specific
patterns (broker / DB / multi-tenancy conventions) belong in the
consumer repo's own override files, not in this skill.

## Who runs it

Every agent that writes or reviews Python code. Buddy enforces
on delegation (checklist section 8). Primary consumer:
`agents/main-code-agent.md`.

## Triggers

| Trigger | Action |
|---------|--------|
| New Python code is written | The agent follows these conventions |
| Code review / PR | The reviewer checks against these conventions |
| New package / dependency added | `pyproject.toml`, no requirements.txt |

---

## 1. Project layout

```
<project>/
  pyproject.toml          # the only build/dependency definition
  src/<project>/          # source root (src layout)
    __init__.py
    ...                   # consumer-defined package structure
  tests/                  # tests (mirror of src/<project>/)
    unit/
    integration/
    fixtures/
  .venv/                  # local virtual environment
```

**Rules:**
- The `src/` layout is required. No flat layout.
- One `pyproject.toml` — no `setup.py`, no `setup.cfg`, no
  `requirements.txt`.
- `__init__.py` in every package — even when empty.

### First-time setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## 2. Dependency management

### pyproject.toml (SoT)

```toml
[project]
requires-python = ">=3.12"
dependencies = [...]          # runtime deps

[project.optional-dependencies]
dev = [...]                   # dev/test deps
```

### Rules

- **Every dependency in pyproject.toml.** No
  `requirements.txt`, no `Pipfile`.
- **Version constraints:** `>=x.y` for libraries, no `==`
  pinning (a lock file owns exact pinning when introduced).
- **Add a new dependency:** under `[project.dependencies]` or
  `[project.optional-dependencies.dev]`. Then run
  `pip install -e ".[dev]"` in the venv.
- **No global `pip install`.** Everything in the venv.

### Later (when uv is introduced)

uv as a drop-in for pip / venv. Commands:

```bash
uv venv .venv              # instead of python -m venv
uv pip install -e ".[dev]" # instead of pip install
uv pip compile             # generate the lock file
```

Currently: standard pip + venv is the baseline. uv when needed
(large dependency trees, lock files).

---

## 3. Code quality: ruff

ruff is linter + formatter in one. Replaces flake8, black,
isort.

### Current config (pyproject.toml)

```toml
[tool.ruff]
target-version = "py312"
line-length = 120
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

### Rule sets

| Code | What | Why |
|------|------|-----|
| E | pycodestyle errors | base style |
| F | pyflakes | dead imports, undefined names |
| I | isort | import sorting |
| N | pep8-naming | naming conventions |
| W | pycodestyle warnings | style warnings |
| UP | pyupgrade | use Python 3.12+ syntax |

### Extended rules (recommended for service / library code)

```toml
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "RUF", "ASYNC", "S"]
```

| Code | What | Why |
|------|------|-----|
| B | flake8-bugbear | common bugs (mutable defaults, etc.) |
| SIM | flake8-simplify | constructs that simplify |
| RUF | ruff-specific | ruff's own rules |
| ASYNC | flake8-async | async / await mistakes (relevant for async frameworks) |
| S | bandit (security) | security patterns (eval, exec, hardcoded passwords) |

**Caution on activation:** existing code can fall foul of stricter
rules (bare `except Exception:` S110, `subprocess.run()` in tests
S603/S607). Before activation:
1. Run `ruff check --select B,SIM,RUF,ASYNC,S src/ tests/`
   (dry run).
2. Fix auto-fixable issues:
   `ruff check --fix --select B,SIM,RUF,ASYNC,S src/`.
3. Review non-auto-fixable issues one by one; if needed,
   `# noqa: S110` with rationale.

### Execution

```bash
# Lint
.venv/bin/ruff check src/ tests/

# Format
.venv/bin/ruff format src/ tests/

# Fix (auto-fixable issues)
.venv/bin/ruff check --fix src/ tests/
```

ruff runs in the venv (installed via the `dev` deps). No
global install needed.

---

## 4. Testing: pytest

### Config (pyproject.toml — SoT)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-n auto --dist loadgroup"   # parallel default: skills/testing/lean-suite.md
markers = [
    "integration: L3 integration tests (need infra services)",
    "e2e: L4 end-to-end tests (need running services)",
    "contract: L3 contract tests (need OpenAPI schema)",
    "property: L5 property-based tests (hypothesis)",
    "smoke: L4 smoke tests (against production endpoints)",
    "eval: eval tests (verify hypotheses with code)",
]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "session"
asyncio_default_test_loop_scope = "session"
```

**Note:** `pyproject.toml` is the SoT. When this config and
the real `pyproject.toml` diverge: adjust pyproject.toml (not
the other way round).

### Conventions

- **Test files:** `test_<module>.py` — mirror of the src
  structure.
- **Test functions:** `test_<what_is_tested>()`.
- **Fixtures:** in `conftest.py` at the right level (tests/,
  tests/unit/, tests/integration/).
- **Async tests:** `async def test_...()` — pytest-asyncio in
  auto mode.
- **Integration tests:** marker `@pytest.mark.integration`.
  Need infra services (DB, broker, etc.). Testcontainers in
  dev deps when applicable.

### Execution

```bash
# All unit tests
.venv/bin/pytest tests/unit/

# Integration tests (need Docker)
.venv/bin/pytest tests/integration/ -m integration

# With coverage (src layout: point the path at the package)
.venv/bin/pytest --cov=src/<project> --cov-report=term-missing tests/

# Single test
.venv/bin/pytest tests/unit/test_models.py::test_specific -v
```

### Test-pyramid mapping

See `skills/testing/SKILL.md` for the 6-level pyramid. This
skill defines only the pytest mechanics, not the test
strategy.

---

## 5. Security tooling

### detect-secrets

Prevents API keys, passwords, tokens from landing in the
code.

```bash
# Create the baseline
detect-secrets scan > .secrets.baseline

# Audit against the baseline
detect-secrets audit .secrets.baseline
```

```bash
.venv/bin/pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

### pip-audit

Audits dependencies for known vulnerabilities (CVEs).

```bash
.venv/bin/pip-audit
```

```bash
.venv/bin/pip install pip-audit
```

---

## 6. Stack conventions

Generic Python service patterns. Consumer repos add stack-specific
patterns (broker, ORM, multi-tenancy, framework idioms) in their
own override files.

### Pydantic models

- Shared models in a dedicated package (e.g. `<project>/models/`).
- `model_config = ConfigDict(...)` instead of `class Config`.
- Validators via `@field_validator` (Pydantic v2 syntax).
- No `from_orm` — Pydantic v2 uses `model_validate`.

### FastAPI (when used)

- Routers in separate files (one per resource).
- Dependency injection via `Depends()`.
- Response models explicit: `response_model=...`.
- No `*` imports.

### Async / await

- No `asyncio.run()` in library code (only in entrypoints).
- `asyncio.to_thread()` for blocking I/O (e.g. LLM completion,
  subprocess).
- No mixing of sync / async in the same module without a
  clear reason.

### Imports

- Absolute imports.
- No relative imports (`from .models import ...`) except in
  `__init__.py`.
- Import order (enforced by ruff `I`):
  1. stdlib.
  2. third-party.
  3. local (`<project>.*`).

### Logging

- `structlog` (not stdlib `logging`).
- Logger per module:
  `logger = structlog.get_logger(__name__)`.
- Structured: `logger.info("event_name", key=value)` — no
  f-string in log messages.
- **Migration:** on touching files that still use
  `import logging`, switch to `structlog`. No
  big-bang refactor.

---

## 7. What NOT

- **No mypy / ty (by default).** Pydantic + ruff UP + runtime
  validation are enough for many service codebases. Evaluate
  type checkers when the codebase grows. Write type
  annotations anyway — they serve as documentation and
  Pydantic uses them at runtime.
- **No pre-commit framework.** CC hooks are the mechanism
  for pre-commit checks. A separate pre-commit framework
  would conflict with that.
- **CI / CD optional.** Local-first is fine. CI comes when
  the project needs it.
- **No uv (yet).** Standard pip + venv is enough at the
  baseline. uv when needed (large dependency trees, lock
  files).

---

## 8. Checklist on code delegation

Buddy verifies on every code delegation to main-code-agent:

- [ ] New code under `src/<project>/` (src layout)?
- [ ] Tests under `tests/` (with the right marker)?
- [ ] Dependencies in `pyproject.toml` (not
  requirements.txt)?
- [ ] `ruff check` + `ruff format` clean?
- [ ] No secrets in the code (API keys, passwords)?
- [ ] Async patterns correct (no `asyncio.run` in libraries)?
- [ ] Structured logging (structlog, not print / logging)?

---

## Common rationalizations

The scan-layer for this discipline skill: the excuses that talk an
implementer out of the conventions above. Reject each on sight.

- *"It's just a script / one-off — typing and Ruff are overkill."*
  One-offs become imports. Type + lint from line one; the cost is
  zero, the later retrofit is not.
- *"Mypy noise — I'll add `# type: ignore` to move on."* An ignore
  without a code and a reason is silent debt. Narrow it
  (`# type: ignore[code]`) or fix the type; never blanket-ignore.
- *"`print` is faster to debug than structlog."* `print` ships to
  prod and loses context. Structured logging is non-negotiable in
  library/service code.
- *"Tests later, the feature first."* "Later" is the drift the
  whole framework exists to prevent. Red test before the fix
  (per `adversary_test_plan` / `testing`).
- *"`asyncio.run` inside the library is fine for now."* It breaks
  the moment a caller already has a loop. Libraries expose
  coroutines; only the entrypoint runs the loop.
- *"Secret in a constant just for local dev."* Local secrets leak
  via git history and `--cached` diffs. Env / secret store only —
  detect-secrets is a backstop, not a license.
