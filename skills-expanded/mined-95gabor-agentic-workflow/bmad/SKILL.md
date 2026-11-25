---
name: bmad
description: >-
  Applies BMAD-style agent workflow: break down goals, model requirements,
  analyze risks, and deliver in small verifiable steps. Use when planning
  features, writing specs, or structuring multi-phase implementation.
---

# BMAD Workflow

BMAD helps agents and humans align before coding: **Break down**, **Model**, **Analyze**, **Deliver**.

## When to use

- New features spanning UI + API + docs
- Changes to domain rules with high regression risk
- Multi-phase roadmap items

## Process

### 1. Break down

- State user outcome in one sentence.
- List in-scope vs out-of-scope per `docs/REQUIREMENTS.md`.
- Identify affected modules (paths from `project-context`).

### 2. Model

- Name entities and API operations; cross-check `docs/DATA_MODEL.md`.
- For content/schema changes, update the canonical docs first, then code/seed.

### 3. Analyze

- Risks: auth, PII, cost of third parties, scoring/domain drift, locale/copy.
- Dependencies: migrations, env vars, Docker/CI services.
- Test plan: one happy path + one edge/admin check.

### 4. Deliver

- Implement in thin vertical slices (API + UI + docs together when both layers change).
- Verify domain rules still match documented formulas/specs.
- Update README or AGENTS only when workflow changes.

## Artifacts

Prefer updating existing `docs/*.md` over new ad-hoc spec files unless the user asks for a dedicated design doc. Use `docs/handoffs/{slug}/` for Type B feature chains.
