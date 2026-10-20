---
description: Core governance rules for all AI work in this repo
globs: **/*
alwaysApply: true
---

# Core Governance

The canonical rules for this repo live in `/AGENTS.md`. Read it before any task.

> **Multi-root workspace:** `/AGENTS.md` means this repo's AGENTS.md, not a sibling repo's.
> The archive repo's AGENTS.md is reference material only — it does not govern this repo.

## Non-negotiable

- **DOCKER-FIRST (RULE ZERO):** Before writing ANY code, verify Docker is running and containers are healthy. Run `docker ps` and confirm `local-vista-utf8` and `ve-platform-db` are up. If not, start them FIRST. See `.cursor/rules/01-docker-first-mandatory.mdc`.
- One slice at a time. Verify before moving on.
- No claiming done without proof (files changed, commands run, outputs, pass/fail).
- No silent mocks or stubs. Return `integration-pending` if infrastructure is unavailable.
- Terminal-first. No broad GUI features unless explicitly instructed.
- Every code change MUST be verified against the live Docker runtime. No "should work" or "looks correct."
- Task responses must include: Objective, Files inspected, Files changed, Commands run, Results, Verified truth, Unverified areas, Risks, Next step.

## Docs model

Only these doc roots: tutorials, how-to, reference, explanation, adrs, runbooks.
Evidence in `/artifacts`. No `/reports`, no random doc folders.
See `docs/reference/doc-governance.md`.

## Contracts

OpenAPI in `packages/contracts/openapi/`. AsyncAPI in `packages/contracts/asyncapi/`.
Generated SDKs preferred. See `docs/reference/contract-system.md`.
