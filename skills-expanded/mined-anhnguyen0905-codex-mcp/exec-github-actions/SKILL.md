---
name: exec-github-actions
description: GitHub Actions execution idioms to embed into Codex prompts when a task edits .github/workflows — job and step structure, tag-gated release steps, OS matrices, secrets hygiene, timeouts, and smoke-step wiring for npm packages.
---

# GitHub Actions (embed into Codex prompts)

Serves: tasks that create or edit `.github/workflows/*.yml` (npm smoke wiring, OS matrix, tag-gated publish) — R9.2

Use when a task creates or edits a workflow under `.github/workflows/`. Embed the block below in the execution prompt; Codex cannot see this file.

## Core method

- Source: `.github/workflows/ci.yml` and `publish.yml` in this repository. Embed the block below verbatim in the Codex prompt for any task touching `.github/workflows/`:

```
GitHub Actions rules (mandatory):
- Pin every action by major tag (actions/checkout@v4, actions/setup-node@v4); never @main.
- Every job sets `timeout-minutes`; every network step (npm, npx, curl) has its own timeout or retry.
- Release-only steps are gated: `if: startsWith(github.ref, 'refs/tags/v')`; PR/main jobs never publish.
- Secrets: read only via `${{ secrets.NAME }}` into `env:`; never echo, never write to files that are uploaded or committed; `.npmrc` tokens come from env, never from the repo.
- Install with `npm ci` (lockfile), not `npm install`; cache with `actions/setup-node` `cache: npm`.
- Cross-platform jobs use `strategy.matrix.os: [ubuntu-latest, macos-latest, windows-latest]`; shell steps that must behave the same everywhere set `shell: bash` explicitly, or call `node` scripts instead of shell constructs.
- A smoke/verification step fails the job on non-zero exit; do not `|| true` a check.
- Derive the version from the tag with `${GITHUB_REF_NAME#v}` (bash) and pass it as an argument; never hard-code versions in YAML.
- Keep job names stable (they are branch-protection checks); add new checks as new jobs, do not rename existing ones.
- Prefer `node scripts/<name>.mjs` over inline shell for anything longer than one line, so the logic is unit-testable and platform-neutral.
```

## Why embedded

Workflow YAML fails late (only on push) and platform differences hide until the matrix runs. Encoding the rules in the prompt prevents the common regressions: unpinned actions, missing timeouts, release steps running on PRs, secrets echoed in logs, and bash-only substitutions breaking the Windows runner.

## Reviewer checklist

- Source: the Workflow block above (each line below restates one rule as a yes/no check).
- Every `uses:` is pinned to a major tag; no `@main`/`@master`.
- Every job has `timeout-minutes`; release steps carry a tag `if:` gate.
- No `echo` of a secret, no secret written into an uploaded artifact or committed file.
- `npm ci` used; matrix covers ubuntu/macos/windows when the task says cross-platform.
- Any smoke/verification step fails the job on non-zero exit (no `|| true`, no `continue-on-error` on checks).
- Version derived from the tag, not hard-coded.

## Failure modes

- Source: the Workflow block above. Unpinned action silently changes behaviour on a later push → pin by tag. Missing `timeout-minutes` hangs the runner for 6 h on a stuck `npx` → set timeouts. Release step without a tag gate publishes from a PR → gate with `if:`. Secret echoed in a log or written to an uploaded artifact → env-only, never print. Bash-only substitution on the Windows runner fails the matrix → call a node script instead.

## Provenance

- Source: `.codex-flow/SKILL-BRIEF-github-actions.md` (brief for gap R9.2, authored 2026-09-09 for codex-mcp 0.26.0).
- Source: `.github/workflows/ci.yml` and `.github/workflows/publish.yml` in this repository (existing pinning, matrix, tag-gate, and npm-view wait conventions).
- derived, unverified: GitHub Actions security-hardening guidance (pin actions, secrets via env only, per-job timeouts) as commonly documented; not re-checked against a primary source in this session.
