---
name: observability-harness
description: Apply, update, validate, or bootstrap the Repo Harness Kit observability module in a target repository. Use when a repo needs the VictoriaMetrics baseline, observability inventories, signal catalog validation, or per-service smoke orchestration.
---

# Observability Harness

Use this skill when the repo needs the shared Victoria-based observability baseline.

Workflow
--------

1. For a new repo, scaffold project-owned configs and docs first:

```bash
uv run python scripts/harness/bootstrap.py --repo-root <repo> --module observability
```

2. Install or update the kit-managed observability assets:

```bash
uv run python scripts/harness/harness.py --repo-root <repo> --mode install --module observability
uv run python scripts/harness/harness.py --repo-root <repo> --mode update --module observability --kit-version <version>
```

3. Validate baseline assets and inventories:

```bash
uv run python scripts/harness/harness.py --repo-root <repo> --mode check --module observability
uv run python scripts/harness/observability/verify.py --repo-root <repo>
```

4. Plan or run smoke:

```bash
uv run python scripts/harness/observability/smoke.py --repo-root <repo> --dry-run
uv run python scripts/harness/observability/smoke.py --repo-root <repo>
```

Rules
-----

- Keep `harness/observability/baseline.yaml` as the source of truth for compose files, smoke label, timeout, and artifacts directory.
- Smoke is HTTP-only by default; non-HTTP service kinds can still participate in docs and signal catalog coverage.
- The skill stays script-first: use the shared smoke orchestration and generated inventories instead of ad hoc checks.
- Use the bundled `scripts/harness/**` runtime from this skill directory; do not assume the target repo contains harness code.
