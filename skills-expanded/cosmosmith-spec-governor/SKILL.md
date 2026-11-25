---
name: cosmosmith-spec-governor
description: Convert Cosmosmith idea and research briefs into proposal, design, and task ledger artifacts. Use after product discovery, when a rough idea needs an OpenSpec-like proposal, buildable design, and claimable tasks with acceptance checks and verification evidence.
---

# Cosmosmith Spec Governor

## Purpose

Turn clarified intent into executable project structure: `proposal.md`, `design.md`, and `task.md`.

## Workflow

1. Read project `AGENTS.md`, `docs/cosmosmith/idea-brief.md`, optional `docs/cosmosmith/research-brief.md`, and existing specs.
2. Draft `proposal.md` from the plugin proposal template.
3. Draft `design.md` from the plugin design template.
4. Create or update `task.md` from the plugin task ledger template.
5. Publish the smallest claimable tasks that can produce reviewable evidence.
6. Assign owner roles, dependencies, acceptance checks, and harness notes.
7. Add a governance review task for `cosmosmith-governance-review`.

## Task Publishing Rules

- Derive tasks from proposal and design artifacts.
- Keep each task small enough to verify.
- Use role owners, not named people, unless the user explicitly named someone.
- Leave tasks `queued` until an agent claims them.
- Never mark tasks `done` without evidence.

## Completion

Stop when proposal, design, and task ledger exist and each claimable task has output, acceptance checks, harness, loop, and dependencies.

