---
name: project-evolution
description: Manage project evolution over time: feature lifecycle, ADR decisions, roadmap, technical debt, known issues, refactor candidates, release notes, upgrade history, and durable development process records. Use when adding features, planning upgrades, changing architecture, stabilizing a project, or keeping long-term project knowledge current.
---

# Project Evolution

## Purpose

Turn project work into durable, searchable development history.

Maintenance keeps current references accurate. Evolution records why the project changed, what risks remain, and what should happen next.

Use with `project-assistant` so evolution records are triggered automatically after meaningful implementation, not only during planning.

## Read Before Work

Read evolution docs before:
- Planning a feature or upgrade.
- Changing architecture, module boundaries, API contracts, database schema, auth, deployment, or release flow.
- Fixing recurring bugs.
- Refactoring code with known debt.
- Deciding what to implement next.

Minimum read set when present:
1. `.ai_project.md`
2. `docs/roadmap/roadmap.md`
3. `docs/changelog/development-log.md`
4. `docs/maintenance/technical-debt.md`
5. `docs/maintenance/known-issues.md`
6. `docs/maintenance/refactor-candidates.md`
7. Relevant `docs/decisions/ADR-*.md`

## Recommended Docs

```text
docs/
  roadmap/
    roadmap.md
  maintenance/
    technical-debt.md
    known-issues.md
    refactor-candidates.md
  decisions/
    ADR-0001-title.md
  changelog/
    development-log.md
```

## Feature Lifecycle

Track meaningful features with:

- `planned`: agreed direction, not started.
- `in-progress`: implementation started.
- `implemented`: code exists.
- `verified`: tested or manually verified.
- `released`: shipped or ready for distribution.
- `deprecated`: replaced or intentionally retired.

Record feature name, status, owner/module, key files, related docs, verification, open risks, and next step.

## ADR Triggers

Create or update an ADR when:
- Introducing a new framework, database, major library, runtime, or deployment path.
- Changing module boundaries or architecture style.
- Changing auth, security model, packaging, or release strategy.
- Choosing between meaningful alternatives.
- Accepting notable tradeoff or technical debt.

ADR shape:

```markdown
# ADR-0001: Title

## Status
Proposed | Accepted | Superseded

## Context
## Decision
## Consequences
## Alternatives Considered
```

## Technical Debt

Record debt when:
- A shortcut is accepted.
- A file is too large.
- Coupling is known.
- Tests are missing.
- A migration or rollout is incomplete.

Each entry should include area, debt, reason accepted, risk, suggested cleanup, and trigger for cleanup.

## Known Issues

Record recurring or unresolved issues with symptom, affected module, reproduction/evidence, current hypothesis, workaround, and next diagnostic step.

## Refactor Candidates

Record candidates when:
- A file approaches or exceeds 1000 lines.
- A module owns too many responsibilities.
- Logic is duplicated across features.
- Tests are hard to write because boundaries are unclear.
- API DTOs, UI models, and domain models are mixed.

## Development Log

Append only useful milestones:
- Date.
- Change summary.
- Files/modules touched.
- Verification.
- Docs updated.
- Next step.

Avoid noisy command logs and generic summaries.

## Project Assistant Handoff

After meaningful work, decide whether to update:
- Feature lifecycle status in `.ai_project.md` or `docs/roadmap/roadmap.md`.
- ADR for important decisions.
- Technical debt, known issues, or refactor candidates.
- Development log for durable milestones.

Do not record routine tiny edits unless they affect future planning, debugging, release, or ownership.

## Final Answer Requirements

When evolution docs changed, include:

```markdown
演进记录：
- 更新 `docs/roadmap/roadmap.md`
- 新增 `docs/decisions/ADR-0002-api-client-boundary.md`
```

If evolution docs should have changed but did not, state why.

## Output Contract

- State the selected workflow, assumptions, and concrete deliverable.
- Include verification, limitations, or next-step handoff when relevant.
- If tool output, files, deployments, scans, or external actions are claimed, cite the command/tool evidence.
