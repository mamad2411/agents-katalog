---
name: repo-architecture
description: GBrain-inspired filing rules for this Codex package. Use when deciding where new skills, docs, registries, scripts, or tests should live in the repo.
---

# Repo Architecture

Use this skill when deciding where future GBrain port artifacts belong in this repo.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Decision Rules

- new skill ports go in `skills/<slug>/`
- source registries go in `data/`
- strategy, compatibility, and resolver docs go in `docs/`
- deterministic helpers go in `scripts/` or `src/`
- regression coverage goes in `tests/`

## Workflow

1. Identify the primary purpose of the new artifact.
2. Put it where contributors would naturally look first.
3. Avoid duplicate representations of the same source of truth.
4. Update docs or registries when the new artifact changes repo structure.

## Guardrails

- Do not create parallel structures that split one concern across multiple folders without a good reason.
- Prefer extending existing docs or registries before inventing a new one.
- Keep the GStack and GBrain source layers explicit when a file belongs to one of them.
