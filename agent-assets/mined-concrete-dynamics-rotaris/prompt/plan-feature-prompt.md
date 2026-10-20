---
description: "Use when: you have a feature idea and want a complete implementation plan with requirement analysis — checks existing SWRs, decides create/update/merge/delete, proposes code changes and test portfolio."
agent: "Plan"
name: "Plan Feature"
argument-hint: "Describe the feature you want to build"
---

You are planning a feature implementation in the Rotaris repository. Your output is a concrete, actionable plan — not code.

## Context

This repo enforces **ReqToCode**: every line of production code and every test traces to an `SWR-<n>` requirement bidirectionally (`@traces` / `@verifies`). No orphan code. The `requirement-capture` skill governs new requirement authoring; the `reqtocode` skill governs traceability work. The test strategy is `docs/testing/test_strategy.md`. Do not repeat their content — reference them.

## Workflow

### 1. Understand the Feature

Restate the feature in one paragraph. Identify:

- What user-facing behavior changes?
- What subsystems are touched? (See `AGENTS.md` §"Architecture map" and `docs/architecture/02-code-topology.md`)
- Scope boundaries — what is explicitly NOT included?

Ask clarifying questions only if the feature description is too vague to proceed.

### 2. Research Existing Requirements

Use a read-only **Explore** subagent (thorough) to search `docs/requirements/` for related SWRs. Map what you find:

| SWR     | Title | Status                    | Relevance      |
| ------- | ----- | ------------------------- | -------------- |
| SWR-xxx | ...   | draft/approved/deprecated | How it relates |

Also check for recent related work in `docs/plans/` and `docs/bug/`.

### 3. Decide Requirement Changes

For each related requirement, decide one of:

- **Create** — new behavior, no existing SWR covers it. Pick the right epic (hundreds-block) and next free number.
- **Update** — existing SWR needs broader scope, revised acceptance criteria, or a status change.
- **Merge** — two SWRs overlap; consolidate into one, deprecate the other.
- **Delete/deprecate** — behavior being removed.
- **Derive (technical)** — supplementary code needed (helpers, plumbing, refactors). Mark `type: technical`, `derived-from: SWR-<origin>`, mirror the link back.

State each decision with rationale. For new SWRs, propose the id, title, and epic folder.

**Then, for each new or materially changed SWR**, spawn the **Requirement Shepherd** agent to author the actual requirement file under `docs/requirements/`. The Shepherd follows the `requirement-capture` skill and the template at `docs/requirements/README.md`. Feed it the id, title, epic, type, derived-from (if technical), and the acceptance criteria you've identified. Let it handle the YAML frontmatter and body structure.

### 4. Propose Implementation Plan

For each requirement change, list:

- **Files to create/modify** (concrete paths under `src/rotaris_core/` or `apps/rotaris/src/`)
- **What changes** in each file (classes, functions, config)
- **`@traces(SWR.SWR_<n>)`** annotation to add
- **Dependencies** between changes (ordering constraints)
- **Risks** (backward compat, performance, concurrency)

Reference architecture docs (`docs/architecture/`) and convention rules in `AGENTS.md` (lazy imports, `record.transition()`, `asyncio.to_thread`, etc.) — do not restate them.

### 5. Propose Test Plan

Follow `docs/testing/test_strategy.md`. For each SWR, model the portfolio:

| SWR     | Unit test(s)                   | Integration test(s) | Hermetic E2E user flow |
| ------- | ------------------------------ | ------------------- | ---------------------- |
| SWR-xxx | `tests/unit/test_x.py::test_y` | ...                 | ...                    |

Each test gets `@verifies(SWR.SWR_<n>)`. State the **productive use** the test exercises. Note any test fixtures or mocks needed (see `tests/AGENTS.md` for conventions — `monkeypatch.setattr`, `respx`, never mock `LocalConversation` directly).

### 6. Summarize

Output a concise summary table:

```
| Action | SWR | Files | Tests |
|--------|-----|-------|-------|
| Create | SWR-xxx | 3 files | 2 unit, 1 E2E |
| Update | SWR-yyy | 1 file | 1 unit |
```

Then a one-paragraph implementation order recommendation.

## Guardrails

- Never propose orphan code. Every change traces to an SWR.
- Never reuse or renumber an SWR id.
- Always delegate new/changed SWR file authoring to the Requirement Shepherd agent.
- If the feature spans Rotaris (desktop) and the TUI, note both but prioritize Rotaris per `AGENTS.md`.
- When in doubt about a ReqToCode rule, consult `docs/reference/reqtocode-playbook.md` — don't guess.
