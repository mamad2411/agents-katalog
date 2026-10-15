---
name: agentic-project-bootstrap
description: Create an agentic project-delivery foundation for a fresh or under-documented repository. Use when Codex needs to brainstorm project direction, research the existing codebase or competitive context, scaffold planning documents, define milestones and protocol notes, create ADRs, and generate aligned AGENTS.md and CLAUDE.md files that enforce a docs-first, test-first workflow.
---

# Agentic Project Bootstrap

Build a reusable planning and execution pipeline before feature work starts. Ground the repository in explicit product docs, milestone sequencing, protocol boundaries, parity tracking, and agent instructions that force future work through that pipeline.

Read only the references and templates that matter for the current repository. Keep the result specific to the project instead of dropping generic boilerplate unchanged.

## Workflow

### 1. Triage The Repository

- Inspect the repo layout, README, existing docs, and any existing `AGENTS.md` or `CLAUDE.md`.
- Determine whether the repository is greenfield, partially documented, or already has planning artifacts that need normalization.
- Identify the product surface area, likely users, major runtime boundaries, and any protocol or persistence concerns.
- If the user names a target product direction, use it. Otherwise, derive a minimal defensible framing from the code and existing docs.

Use [references/research-and-scoping.md](./references/research-and-scoping.md) when you need the discovery questions and evidence checklist.

### 2. Define The Planning Surface

- Ensure these artifacts exist, either by updating existing files or scaffolding them from templates:
  - `docs/prd.md`
  - `docs/milestones/`
  - `docs/parity-matrix.md`
  - `docs/protocol.md`
  - `docs/architecture-decisions/`
- Do not create all possible docs blindly. Create the minimum set needed to make future work auditable and sequenced.
- If the repo already has equivalent files with different names, preserve the local convention and adapt the templates instead of renaming everything.

Use [references/template-map.md](./references/template-map.md) to decide which template files to copy and how to adapt them.

### 3. Write The Docs In Dependency Order

Create or update documents in this order:

1. `docs/prd.md`
2. `docs/milestones/*.md`
3. `docs/parity-matrix.md`
4. `docs/protocol.md`
5. `docs/architecture-decisions/*.md` for top-level decisions
6. `AGENTS.md`
7. `CLAUDE.md`

This order matters. The agent instructions should point at real planning artifacts, not placeholders.

### 4. Keep Milestones Concrete

- Milestones must be ordered and each one must have objective, scope, acceptance criteria, and exit condition.
- Choose the smallest milestone set that explains delivery order.
- Put architecture-enabling work before UX polish.
- If parity tracking matters, record whether each milestone closes a gap, preserves a deliberate deviation, or introduces a temporary mismatch.

### 5. Make The Protocol Explicit

- In `docs/protocol.md`, document request and response shapes, event flows, persistence boundaries, approvals, permissions, and compatibility expectations.
- If the project is not networked or IPC-heavy, define protocol broadly as the contract between layers, modules, or runtime boundaries.
- Write down deliberate non-goals and compatibility assumptions so future agents do not guess.

### 6. Generate Agent Instructions Last

- `AGENTS.md` is the canonical workflow spec.
- `CLAUDE.md` should mirror the same operational rules with only wording changes needed for Claude-specific compatibility.
- Require future agents to:
  - ground non-trivial work in project docs first
  - update planning artifacts before implementation when scope changes
  - write failing tests first for new behavior
  - implement the smallest correct change
  - verify new and relevant existing tests
  - keep parity and milestone docs current

Start from [assets/templates/AGENTS.md](./assets/templates/AGENTS.md) and [assets/templates/CLAUDE.md](./assets/templates/CLAUDE.md), then rewrite them to match the repo's actual paths and terminology.

### 7. Validate The Foundation

- Check that every instruction in `AGENTS.md` points at a real file or directory.
- Check that milestone names referenced in the PRD exist.
- Check that parity rows reference real features or categories.
- Check that protocol notes match the architecture actually present in the repo.
- If the repository already has tests or CI commands, mention the concrete verification commands in the docs where appropriate.

## Adaptation Rules

- Replace template placeholders aggressively. Do not leave `your-project` style names in final docs.
- Preserve existing terminology if the repo already says `roadmap`, `spec`, or `design-doc` instead of `milestone`, `PRD`, or `ADR`.
- Avoid inventing parity tracking if the product has no external baseline. In that case, define parity as internal gap tracking against the PRD or target workflows.
- Avoid creating an ADR for every minor choice. Use ADRs only for decisions that affect top-level architecture, delivery order, or invariants future agents could violate.

## Templates

- Use [assets/templates/docs/prd.md](./assets/templates/docs/prd.md) for the product requirements baseline.
- Use [assets/templates/docs/milestones/01-foundation.md](./assets/templates/docs/milestones/01-foundation.md) as the first milestone template and clone it for later milestones.
- Use [assets/templates/docs/parity-matrix.md](./assets/templates/docs/parity-matrix.md) for gap tracking.
- Use [assets/templates/docs/protocol.md](./assets/templates/docs/protocol.md) for contracts and boundary notes.
- Use [assets/templates/docs/architecture-decisions/0001-agentic-delivery-pipeline.md](./assets/templates/docs/architecture-decisions/0001-agentic-delivery-pipeline.md) when the workflow itself is an architectural decision worth recording.
- Use [assets/templates/AGENTS.md](./assets/templates/AGENTS.md) and [assets/templates/CLAUDE.md](./assets/templates/CLAUDE.md) for the execution rules.

## Deliverable Standard

Finish with a repository state where:

- planning docs exist and are internally consistent
- milestones describe delivery order, not just a feature list
- the protocol file captures the important contracts
- agent instructions enforce docs-first and tests-first behavior
- template wording has been replaced with project-specific language
