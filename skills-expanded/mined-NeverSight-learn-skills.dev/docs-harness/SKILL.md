---
name: docs-harness
description: Apply, update, validate, or bootstrap the Repo Harness Kit docs module in a target repository. Use when a repo needs the index-driven docs structure, C4 docs, generated inventories, or docs bootstrap for new services and monorepos.
---

# Docs Harness

Use this skill when the target repo needs the documentation baseline from the Repo Harness Kit.

Workflow
--------

1. Read `references/contract.md` if the repo shape or ownership boundary is unclear.
2. For a new repo, scaffold project-owned files first:

```bash
uv run python scripts/harness/bootstrap.py --repo-root <repo> --module docs
```

3. For an existing repo, install or update the module:

```bash
uv run python scripts/harness/harness.py --repo-root <repo> --mode install --module docs
uv run python scripts/harness/harness.py --repo-root <repo> --mode update --module docs --kit-version <version>
```

4. Verify the result:

```bash
uv run python scripts/harness/harness.py --repo-root <repo> --mode check --module docs
uv run python scripts/harness/docs/verify.py --repo-root <repo>
```

Rules
-----

- Do not overwrite project-owned docs by default.
- Treat `docs/index.md` as the only entrypoint.
- If the repo mixes Python and non-Python services, keep non-Python kinds on the docs-only path unless a stronger adapter is explicitly required.
- Use the bundled `scripts/harness/**` runtime from this skill directory; do not assume the target repo contains harness code.
