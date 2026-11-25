# Authoring a new skill

This document walks through the pattern used to ship `spring-boot-api-scaffold`,
so you can follow the same shape for the next skill. The fastest valuable
follow-up is `fastapi-scaffold` — symmetric to spring-boot, but exercises the
SQLAlchemy/Alembic branch — and the steps below are written with that target
in mind.

## The two pieces of a real skill

A real skill (one with file-generation authority, as opposed to a stub) has
exactly two artifacts:

1. **`skills/<skill-name>/SKILL.md`** — the human-readable procedure. Lives
   in the skill library, PR-reviewed by domain CODEOWNERS. Documents the
   contract: what it reads from the Project Spec, what it produces, what
   external effects it has (usually none for scaffolds), what gates apply.

2. **`src/devenv_agent/skill_impls/<skill_name>.py`** — the executor. Reads
   the params dict, writes files under `workspace/`, returns a
   `ScaffoldResult`. No external I/O beyond the filesystem.

The Scaffolder sub-agent calls the executor when the planner emits a step
naming the skill and `dry_run=False`. Everything else (planning, missing-skill
detection, gating) just works because the skill name appears in
`skills/`'s frontmatter and in `skill_impls.REGISTRY`.

## Step-by-step (using fastapi-scaffold as the example)

### 1. Write `skills/fastapi-scaffold/SKILL.md`

The frontmatter is the lint-enforced contract. Stick to this shape:

```yaml
---
name: fastapi-scaffold
version: 0.1.0
owner: backend-platform
description: Scaffolds a FastAPI (Python 3.12) service wired for OAuth2 resource-server,
             SQLAlchemy 2.x, Alembic, Authlib for JWT validation, structlog for JSON
             logging, and prometheus-fastapi-instrumentator. Multi-stage Dockerfile
             and a compose fragment for docker-compose-dev.
inputs:
  - backend                  # one entry from Project Spec backends[]
  - projectName
  - idp.issuerUrl            # from IdPOps output
  - sla
outputs:
  - services/<backend.name>/
  - compose.fragment.yml
effects:
  - none-external            # files only; no MCP calls
---
```

Then the body is a numbered procedure. Look at
`skills/spring-boot-api-scaffold/SKILL.md` for the level of detail expected —
each section corresponds to a step the executor will perform, with the
files/templates it emits called out explicitly.

The body is what a future contributor reads to understand the skill. It's
also what a future Claude sub-agent (when sub-agents are real, not mocks)
will read to know what to produce. Treat it as the authoritative
specification; the Python code below should match it line-for-line.

### 2. Write `src/devenv_agent/skill_impls/fastapi_scaffold.py`

The contract is small. Look at `spring_boot_api_scaffold.py` for the
reference; the new module must expose:

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ScaffoldResult:
    files_created: list[str]
    service_dir: str
    package: str         # or any module-identifier the spec needs to know about

def run(params: dict, *, workspace: Path | None = None) -> ScaffoldResult:
    backend       = params["backend"]
    project_name  = params["projectName"]
    issuer_url    = params.get("idp.issuerUrl") or "${OAUTH2_ISSUER_URI}"
    workspace     = workspace or Path.cwd()

    service_dir = workspace / "services" / backend["name"]
    if service_dir.exists() and any(service_dir.iterdir()):
        raise FileExistsError(...)                # idempotency check

    created = []
    def write(rel, content):
        p = service_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        created.append(str(p.relative_to(workspace)))

    write("pyproject.toml",         _pyproject(...))
    write("Dockerfile",             _dockerfile())
    write("src/<pkg>/main.py",      _main_py(...))
    # ... etc.

    return ScaffoldResult(files_created=created, service_dir=str(service_dir), package=pkg)
```

Templates as inline Python string literals (f-strings or `.format()`). Don't
reach for Jinja yet — at one or two skills the dependency cost outweighs the
leverage. Lift to `templates/` directories once you have three backend
scaffolds sharing patterns.

### 3. Register it in `src/devenv_agent/skill_impls/__init__.py`

```python
from . import fastapi_scaffold, spring_boot_api_scaffold

REGISTRY = {
    "spring-boot-api-scaffold": spring_boot_api_scaffold.run,
    "fastapi-scaffold":         fastapi_scaffold.run,
}
```

That's it. The Scaffolder picks it up automatically. The planner already
emits the right step name via `planner._scaffold_skill_for["fastapi"]`.

### 4. Add a regression test

Pattern from `tests/test_planner.py::test_real_spring_boot_scaffold_generates_files`:

```python
def test_real_fastapi_scaffold_generates_files(tmp_path):
    from devenv_agent.skill_impls.fastapi_scaffold import run as scaffold_run

    spec = Spec.load(EXAMPLE)
    backend = next(b for b in spec.backends if b["framework"] == "fastapi")
    result = scaffold_run({
        "projectName":   spec.project_name,
        "backend":       backend,
        "idp.issuerUrl": f"https://keycloak.corp/realms/{spec.realm_name}",
    }, workspace=tmp_path)

    assert len(result.files_created) >= 8
    sd = tmp_path / "services" / backend["name"]
    assert (sd / "pyproject.toml").exists()
    assert (sd / "Dockerfile").exists()
    # One sanity check on the content:
    assert "fastapi" in (sd / "pyproject.toml").read_text().lower()
```

The test ensures the file count matches the SKILL.md's promise and that the
generated content references the right framework.

### 5. Verify end-to-end

```bash
make test                       # new test passes alongside existing 15
make plan                       # fastapi-scaffold now shows ✓ (known) instead of ✗ MISSING
python -m devenv_agent.cli run examples/orders-platform.json --apply --workspace /tmp/out
ls /tmp/out/services/inventory-api/   # should contain the new scaffold
```

## Common gotchas

- **Don't write outside `workspace/services/<backend.name>/`.** The shared
  layout (root compose, top-level Makefile) is owned by `docker-compose-dev`
  and `dev-tasks-makefile`, not the per-service scaffold. Emit a
  `compose.fragment.yml` that the compose-dev skill merges in.

- **Don't hardcode the OAuth2 issuer URL.** Read it from
  `params["idp.issuerUrl"]` (will be the production URL) and let the
  `application-local.yml` / equivalent override to the compose-internal URL
  via env var.

- **Don't embed live secrets in any scaffold output.** Use placeholder env
  vars and let `secrets-vault-integration` populate Vault paths. The
  scaffold should emit `${ORDERS_API_DB_PASSWORD:-dev}` or similar, never
  a real value.

- **Keep the executor < 400 lines.** If you're growing past that, the
  templates probably belong in separate files. Readability suffers fast
  once a single executor mixes orchestration with more than a few template
  bodies.

- **The frontmatter description must not contain unquoted colons.** YAML
  treats `decision:` as a mapping separator. Quote the string if in doubt.

## Why this pattern, not template-engine-driven scaffolds

Inline templates as Python string literals look low-tech but they pay off:

- Templates can use Python's full power for conditionals (the
  `spring-boot-api-scaffold` emits a scope-gated route only if
  `backend.scopes` is non-empty). With Jinja you'd need a separate filter
  registry; in Python it's two lines.
- Type errors in templates surface as Python `KeyError` or `AttributeError`
  at run time with clear stack traces.
- Code review of a new scaffold is straightforward: it's one Python file
  with one function per generated file. No template loader configuration,
  no environment construction, no escaping rules to learn.

When skill N (probably N≈4) shares enough structure that we'd be repeating
ourselves, that's the right moment to extract a shared template layer. Not
before.
