---
name: source-of-truth-docs-skills
description: Create, audit, and surgically edit repository documentation for agent-heavy projects using Harness Engineering documentation patterns and Karpathy-style restraint. Use when an agent needs to build or improve AGENTS.md, architecture docs, product specs, execution plans, generated references, design docs, reliability notes, security notes, or other source-of-truth project documentation without changing product code.
---

# Source of Truth Docs Skills

Use this skill to make a repository understandable to future agents. Focus on documentation only. Do not change product code unless the user separately asks.

## Purpose

Turn project knowledge into versioned, discoverable repository docs. Prefer a compact map over a giant manual. A future agent should be able to open one short entry point, find the right deeper source of truth, and verify claims against code.

This skill combines two ideas:

- Harness Engineering: put durable project knowledge into the repo, not only in prompts or chat history.
- Karpathy-style restraint: think first, keep changes small, avoid speculative abstractions, and verify the work.

## Recommended Documentation Map

Use this as a general pattern. Adapt names to the project. Keep entry points short and put deeper detail in focused files.

```text
AGENTS.md
ARCHITECTURE.md
docs/
|-- design-docs/
|   |-- index.md
|   |-- core-beliefs.md
|   `-- ...
|-- exec-plans/
|   |-- active/
|   |-- completed/
|   `-- tech-debt-tracker.md
|-- generated/
|   `-- db-schema.md
|-- product-specs/
|   |-- index.md
|   |-- new-user-onboarding.md
|   `-- ...
|-- references/
|   |-- design-system-reference-llms.txt
|   |-- nixpacks-llms.txt
|   |-- uv-llms.txt
|   `-- ...
|-- DESIGN.md
|-- FRONTEND.md
|-- PLANS.md
|-- PRODUCT_SENSE.md
|-- QUALITY_SCORE.md
|-- RELIABILITY.md
`-- SECURITY.md
```

## What Each File Or Folder Does

- `AGENTS.md`: Short navigation map for agents, add instruction tell future agents to edit the docs. Include repo rules, common commands, active constraints, and links to deeper source-of-truth docs. Keep it compact.
- `ARCHITECTURE.md`: Top-level system map: domains, package boundaries, layering, dependency direction, runtime entrypoints, and major invariants.
- `docs/design-docs/`: Durable design history. Store decisions, tradeoffs, core beliefs, architecture notes, and the reasoning behind non-obvious choices.
- `docs/design-docs/index.md`: Index for design docs, with status and links to the most important decisions.
- `docs/design-docs/core-beliefs.md`: Stable engineering and product principles that should guide future implementation choices.
- `docs/exec-plans/`: Versioned execution plans for complex work. Plans should include current status, decisions made, verification steps, and handoff notes.
- `docs/exec-plans/active/`: In-progress plans that another agent can resume.
- `docs/exec-plans/completed/`: Completed plans kept for historical context and debugging.
- `docs/exec-plans/tech-debt-tracker.md`: Known cleanup work, why it matters, evidence, severity, and suggested verification.
- `docs/generated/`: Generated or mechanically refreshed facts. Keep generated docs separate from human-authored guidance.
- `docs/generated/db-schema.md`: Database schema snapshot or generated schema reference, including generation command and timestamp when useful.
- `docs/product-specs/`: Product behavior docs: user flows, feature specs, acceptance criteria, states, permissions, and edge cases.
- `docs/product-specs/index.md`: Map of product areas and specs so agents can quickly find behavior sources.
- `docs/references/`: Local agent-readable copies or summaries of external/vendor documentation that the project depends on.
- `docs/references/*-llms.txt`: LLM-optimized references such as design systems, hosting docs, package manager docs, framework docs, or API behavior notes.
- `docs/DESIGN.md`: Cross-cutting visual, interaction, accessibility, and content design rules.
- `docs/FRONTEND.md`: Frontend architecture, UI state patterns, routing conventions, component rules, and test expectations.
- `docs/PLANS.md`: Index of planning conventions and links to active, completed, and recurring plans.
- `docs/PRODUCT_SENSE.md`: Product principles, audience assumptions, UX priorities, and tradeoffs to preserve.
- `docs/QUALITY_SCORE.md`: Quality rubric or scorecard by product area, including known gaps and target improvements.
- `docs/RELIABILITY.md`: Operational expectations, failure modes, retries, observability, incident patterns, and performance budgets.
- `docs/SECURITY.md`: Security model, sensitive boundaries, auth rules, secrets handling, threat notes, and review expectations.

## Workflow

1. Ground in repo truth first.
   - Inspect existing docs, `AGENTS.md`, architecture notes, manifests, schemas, tests, and likely entrypoints.
   - Use `rg` to verify claims against code before writing.
   - Treat code, tests, configs, migrations, generated schemas, and committed plans as evidence.

2. Choose the smallest useful documentation change.
   - Update existing docs before creating new ones.
   - Create a new doc only when the topic has no clear home.
   - Keep indexes and cross-links current when they are part of the repo pattern.

3. Preserve progressive disclosure.
   - Keep entry docs short and navigational.
   - Put detailed behavior in targeted docs near the relevant domain.
   - Split stable principles, active plans, generated facts, external references, and product specs into separate homes.

4. Edit surgically.
   - Touch only docs needed for the request.
   - Preserve existing tone, structure, headings, and formatting unless they block clarity.
   - Do not rewrite adjacent sections for style.
   - Do not remove stale docs unless the user asked or evidence proves they are obsolete.

5. Verify the result.
   - Check that changed docs point to real files, commands, APIs, and behavior.
   - Run existing markdown lint, link checks, generated-doc checks, or docs tests if the repo already has them.
   - If no checker exists, do targeted manual verification with `rg` and file reads.

## What To Document

Prefer documenting facts that help an agent work correctly later:

- Architecture boundaries and dependency direction.
- Product behavior and user-facing flows.
- Runtime ownership, entrypoints, and data flow.
- Schema contracts, generated docs, and source-of-truth files.
- Known decisions, tradeoffs, active plans, and completed plans.
- Design, frontend, quality, reliability, and security expectations.
- Operational commands only when they are stable and repo-specific.

Avoid documenting obvious implementation details that are easier to read in code.

## Good Documentation Test

A documentation change is good when:

- A future agent can find the right source of truth in under a minute.
- The doc says where the evidence came from.
- The doc has a clear home and does not duplicate another source.
- The change is small enough that stale parts can be found and fixed later.
- Claims can be checked by commands, links, generated files, tests, or explicit source paths.

## Karpathy Guardrails

- Think before editing: state assumptions when docs and code disagree.
- Simplicity first: write the minimum useful documentation.
- Surgical changes: every changed line must trace to the request.
- Goal-driven verification: define what the docs must make clear, then verify it.

## Output Expectations

When finished, report:

- Which docs changed.
- What source evidence was used.
- What was verified.
- Any remaining uncertainty or stale area that needs human judgment.
