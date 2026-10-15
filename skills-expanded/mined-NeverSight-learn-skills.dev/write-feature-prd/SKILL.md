---
name: write-feature-prd
description: Write implementation-aware feature PRDs by grounding requirements in the current codebase, reusable modules, and available skills/tools. Use when the user wants a PRD for an existing product, asks for a codebase-aware feature spec, or wants feature planning that explicitly accounts for current architecture and tooling.
---

# Write Feature PRD

Write PRDs for features in an existing system. Start from what already exists; do not treat the codebase as greenfield.

## Quick Start

1. Clarify the problem, users, and constraints.
2. Explore the repo to find the current flows, modules, and boundaries involved.
3. Inventory reusable code, existing skills, and deterministic tools before proposing new work.
4. Write the PRD with explicit reuse decisions, gaps, risks, and testing/rollout guidance.

## Workflow

### 1. Frame the request

Capture:
- user problem and desired outcome
- affected actors and surfaces
- constraints, deadlines, and non-goals
- whether this is net-new behavior, an extension, or a replacement

### 2. Audit the current system

Read enough code to answer:
- where this feature enters the system
- which modules already solve part of it
- what patterns, contracts, and naming conventions already exist
- what tests, plans, or docs already describe adjacent behavior

Prefer exact code lookup over guessing. Use `/find-code` and `/code-graph` if available.

### 3. Inventory available tools

Before proposing implementation, list:
- reusable modules, services, and components already in the repo
- existing skills that can help deliver the work (`/design-api`, `/write-tests`, `/prd-to-plan`, `/grill-me`, etc.)
- scripts, generators, or platform capabilities already present

The PRD must distinguish:
- **Reuse**: extend or compose as-is
- **Modify**: existing modules that need changes
- **Net-new**: capabilities that do not exist yet

### 4. Resolve decisions

Interrogate missing details until the design is coherent:
- user-visible behavior and edge cases
- data model or schema impact
- API, events, and background jobs
- auth and permissions
- migration, rollout, and failure modes
- observability and testing approach

Use `/grill-me` if the proposal is still vague or risky.

### 5. Write the PRD

Use the template in [REFERENCE.md](REFERENCE.md). Keep the document implementation-aware but durable:
- include module boundaries, contracts, dependencies, and testing strategy
- include named systems and routes when they are durable
- avoid volatile file paths or code snippets unless the user explicitly asks

### 6. Hand off cleanly

If the user wants next steps:
- use `/prd-to-plan` to break the PRD into phases
- route focused execution work to the relevant skill
- note open questions that block implementation

## Guardrails

- Never recommend building new infrastructure when a viable existing path already exists.
- Call out assumptions separately from confirmed findings.
- Treat missing code evidence as uncertainty, not permission to invent.
- If the repo is too large to inspect fully, state the sample you used and the confidence level.

## References

- [REFERENCE.md](REFERENCE.md) - PRD template, repo-audit checklist, reuse inventory format, and decision prompts.
