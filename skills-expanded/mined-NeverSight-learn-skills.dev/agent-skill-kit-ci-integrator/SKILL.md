---
name: agent-skill-kit-ci-integrator
description: Wire the agent-skills toolkit into CI — install the GitHub Actions workflow that runs validate/lint/audit/deps on every PR, and install the pre-commit hooks for local-loop parity. Use when the user asks to set up CI for skills, install pre-commit hooks, configure GitHub Actions for SKILL.md validation, or wire the toolkit into a new repo.
tier: org
license: Apache-2.0
compatibility: requires `pre-commit` (Python pkg) for local hooks; GitHub Actions for CI; node>=20 + python>=3.11 for the underlying skills-ref CLI
---

# Agent Skill CI Integrator

Documents the two CI integration points the toolkit ships and explains how to install, inspect, and extend them.

## When to use

- "Set up CI for our skills"
- "Install pre-commit for SKILL.md"
- "How do I wire skills-ref into GitHub Actions?"
- "Add a PR gate for skills changes"
- "Audit the agent-skills CI configuration"

## GitHub Actions workflow

The canonical workflow lives at `.github/workflows/agent-skills-ci.yml`. It declares three jobs in a strict dependency order:

1. **`mjs-ci`** — runs `make ci` in `.agents/skills/agent-skill-kit-commons/packages/mjs/`. Emits `artifacts/validate.json` from the Node runtime as a stage artifact.
2. **`py-ci`** — runs `make ci` in `.agents/skills/agent-skill-kit-commons/packages/py/`. Verifies polyglot parity by re-running the same gates from the Python runtime.
3. **`gate`** (depends on both) — runs `lint, audit, deps` from the Node runtime, downloads `mjs-ci`'s validate artifact, and posts a single rolled-up comment on the PR. The comment is keyed by an HTML marker (`<!-- agent-skills-ci-marker -->`) so subsequent pushes update the existing comment in place rather than stacking new ones.

Triggers: `pull_request` filtered on `paths: [".agents/skills/**", ".github/workflows/agent-skills-ci.yml"]` (the `.agents/skills/**` glob covers the moved `agent-skill-kit-commons/packages/**` subtree, so no separate filter entry is needed). Permissions: `contents: read, pull-requests: write` — the minimum needed to comment.

Action pins are all majors (`@v4`, `@v5`, `@v7`); never `@main`. The security auditor flags `@main` refs as `A030_HOST_PATH_LEAK`-adjacent, so the convention is enforced by the toolkit itself.

## Pre-commit hooks

The manifest at `.pre-commit-hooks.yaml` exposes four hooks, one per CLI verb (`validate`, `lint`, `audit`, `deps`). All hooks use `language: system` and shell out to the mjs CLI — staying single-runtime in the inner loop avoids paying the parity overhead on every commit.

The local config at `.pre-commit-config.yaml` consumes the manifest so the suite runs its own hooks against itself. Local install:

```bash
pip install pre-commit
pre-commit install
```

After install, any `git commit` touching `.agents/skills/**` runs `validate, lint, audit, deps` against the entire skill set. `pass_filenames: false` is critical — the CLI walks the tree itself; without it, pre-commit would replace the args with the changed file paths and break the recursive scan.

## Inspect / extend

To add a new gate (e.g., a custom organisation-specific rule):

1. Copy a hook entry in `.pre-commit-hooks.yaml`, point `entry:` at your new tool, keep `pass_filenames: false`.
2. Add the matching step to the `gate` job in the workflow YAML.
3. Run `bash .agents/skills/agent-skill-kit-commons/scripts/test-workflow.sh` locally — it parses the YAML, audits for security findings, and confirms all action refs stay pinned to majors.

## Self-test driver

`.agents/skills/agent-skill-kit-commons/scripts/test-workflow.sh` runs offline sanity checks (YAML parse, audit clean, action-ref pinning) and optionally invokes `act` to run the workflow locally inside a Docker runner. If `act` is not installed, the script prints a manual verification checklist.

## Reference

Full specification: see the canonical spec at [../../../agentskills.io.md](../../../agentskills.io.md).
