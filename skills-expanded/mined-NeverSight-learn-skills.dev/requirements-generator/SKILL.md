---
name: requirements-generator
description: Generate structured requirements.md from scope descriptions, stack context, and design briefs for a product version. Use when starting a new version, the user asks for requirements, RF/features document, or before task generation when requirements.md is missing — even if they only describe the feature in chat. Follow SDD planning gates in nextstage-harness. Do NOT generate task files (use task-generator).
depends:
  - nextstage-harness
---

# Requirements Generator

Produce a structured `requirements.md` for `{product_root}/docs/versions/{version_san}/`.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md` and `../nextstage-harness/references/artifact-layout.md`. Create `{product_root}/docs/versions/{version_san}/` before writing.

## Inputs

- Scope description (possibly enriched by `clarify-requirements`)
- `{product_root}`, `{version_san}`
- Optional: `design-brief.md`, stack profile, brownfield map, web research from orchestrator

## Stack profiles

Load **one** profile from `references/stacks/` when stack is known:

| Profile | When |
|---------|------|
| `generic.md` | Default — stack-agnostic structure |
| `laravel-react.md` | Laravel + React monorepo detected or confirmed |
| `intelligent-saas.md` | Backend + frontend + agent-api |

Do not mention framework-specific tooling unless the profile or detected stack applies.

## Document structure

Generate **only** the markdown document (no conversational preamble):

```markdown
## Main objective of the version:
{executive summary}

## Technology stack:
{confirmed stack — reference applicable rules when harness has them}

## UI/UX guidelines:
{from design-brief when frontend in scope — omit if backend-only}

## Data model and APIs:
{tables, FK order, key endpoints — source of truth for tasks}

## Feature grouping:
### Feature 001 - TITLE
**Precedence:** None | Feature NNN
**Layers:** Backend | Frontend | Infrastructure | Tests
**Detailed description:** ...
#### Acceptance criteria:
- [ ] ...

## Non-functional requirements (NFRs):
...
```

## New project ordering

When the project is greenfield, infrastructure/setup features come before domain features (per stack profile): infra → database → cache/queues → backend modules → frontend → tests.

## Language

English unless the user explicitly requests another language for the deliverable.

## Rules

- Work only under confirmed `{product_root}`
- Incorporate research into NFRs or acceptance criteria when provided
- For frontend features: include UI/UX section from design brief; acceptance criteria for visual tokens when applicable
- Data model section is **critical** — explicit table creation order and endpoints

## Integration

- After generation: Gate 1 (`requirements_confirmed`) — see `../nextstage-harness/references/gates.md`
- Next: `analyze-consistency` after Gate 2

## References

| File | When |
|------|------|
| `references/stacks/generic.md` | Default |
| `references/stacks/laravel-react.md` | Laravel/React stack |
| `references/stacks/intelligent-saas.md` | Agent-augmented SaaS |
