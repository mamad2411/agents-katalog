---
name: traceability-harness
description: Apply, update, validate, or bootstrap the Repo Harness Kit traceability module in a target repository. Use when a repo needs requirement catalogs, OpenAPI x-requirements enforcement, generated HTTP inventories, or PR-level contract sync checks.
---

# Traceability Harness

Use this skill when the repo must mechanically align requirements, contracts, and tests.

Workflow
--------

1. Ensure the repo already has docs baseline and `harness/manifest.yaml`.
2. For a new repo, scaffold starter project-owned files first:

```bash
uv run python scripts/harness/bootstrap.py --repo-root <repo> --module traceability
```

3. Install or update the module:

```bash
uv run python scripts/harness/harness.py --repo-root <repo> --mode install --module traceability
uv run python scripts/harness/harness.py --repo-root <repo> --mode update --module traceability --kit-version <version>
```

4. Verify the result:

```bash
uv run python scripts/harness/harness.py --repo-root <repo> --mode check --module traceability
uv run python scripts/harness/traceability/verify.py --repo-root <repo>
```

Rules
-----

- `fastapi` services require OpenAPI and requirement coverage by default.
- `worker`, `service`, `typescript`, `javascript`, `go`, and `rust` stay docs-first unless the repo explicitly opts into stronger contract checks.
- Surface-registry failures mean code changed without aligned contract artifacts; fix the alignment instead of disabling the check.
- Use the bundled `scripts/harness/**` runtime from this skill directory; do not assume the target repo contains harness code.
