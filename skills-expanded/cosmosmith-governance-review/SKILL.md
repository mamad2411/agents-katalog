---
name: cosmosmith-governance-review
description: Review Cosmosmith artifacts, task ledgers, generated project rules, and skill outputs for coherence, layer separation, missing evidence, and rule drift. Use before marking Cosmosmith planning or implementation tasks done, after spec generation, or when project rules and generated rules may have diverged.
---

# Cosmosmith Governance Review

## Purpose

Protect the project from drift: rules, skills, templates, and tasks must stay coherent.

## Workflow

1. Read project `AGENTS.md`, `task.md`, and relevant Cosmosmith artifacts.
2. Check layer separation:
   - Project instructions belong in `AGENTS.md`.
   - Claude-specific adaptation belongs in `CLAUDE.md`.
   - Reusable workflows belong in Cosmosmith skills.
   - Long standards belong in references or docs.
   - Deterministic checks belong in scripts.
3. Check every reviewed task for owner role, status, context, expected output, acceptance checks, harness, loop, evidence, and dependencies.
4. Check that philosophy affects an operational artifact, harness, or loop.
5. Report findings by severity and update `task.md` with follow-up tasks when needed.

## Findings Format

Use this structure:

- Severity:
- Location:
- Problem:
- Why it matters:
- Required fix:

## Completion

Stop when each reviewed artifact is either accepted with evidence or has a concrete follow-up task in `task.md`.

