---
type: skill
id: adr-writing
title: ADR Writing Skill
version: 1
group: tech
applies_to:
  - decision-agent
  - architecture-agent
  - implementation-agent
---
# ADR Writing Skill

## Purpose

Standardize how Architecture Decision Records are written so every decision is captured the same
way and stays auditable.

## When to use

When a real, consequential technical decision is being made or recognized — and only then.

## Inputs

The context pack, the relevant Work Item or architecture note, and the decision being made.

## Output

A single ADR containing: context, the decision, alternatives considered, consequences, the code
paths it governs (`code:` globs when known) and the decision status (proposed / accepted /
superseded).

## Rules

- One ADR = one decision. Never mix unrelated decisions.
- Never invent decisions; never write an ADR without a clear reason.
- Record alternatives honestly, including the one chosen and why.
- Prefer narrow governed `code:` globs over broad ones.

## Quality checklist

- Context explains why the decision was needed.
- The decision and its alternatives are explicit.
- Consequences (positive and negative) are stated.
- Status and governed paths are present.

## Example output

```md
# ADR-0007 — Use SQLite for local persistence
Status: accepted
## Context
...
## Decision
...
## Alternatives considered
...
## Consequences
...
```
