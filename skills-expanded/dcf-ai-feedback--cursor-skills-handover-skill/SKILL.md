---
name: handover
description: Use at the end of delivery to create a holistic handover pack for downstream teams (BAs, architects, developers, QAs, PMs). Summarizes what was built, spec deltas, design decisions, evidence, and open risks.
---

# Handover

Use this skill at the end of a delivery cycle to produce a **handover deliverable** that provides a complete, role-friendly view of what was built and how to operate/validate it.

## Hard enforcement (manual PR operations)

This skill MUST NOT create, open, update, comment on, approve, or merge pull requests. Any PR/merge action is **manual developer work**; this skill only produces the handover artifact in the repo.

## Required output

Create a handover document at:

- `<projectDir>/Docs/HANDOVER.md`

using the template in:

- `system-prompts-skills/handover/HANDOVER-TEMPLATE.md`

## Content requirements

The handover MUST include:

- Delivered outcomes (what changed for users/systems)
- Links to OpenSpec source-of-truth specs and the change folders implemented
- Links to OpenAPI contract (when applicable)
- Key design decisions and patterns considered (chosen vs rejected)
- Evidence summary (tests, CI run links, screenshots, metrics, contract validation)
- Operational notes (config, migrations, telemetry/log keys, runbook-style notes)
- QA guidance (what to validate; environments; known edge cases)
- Rollback plan and residual risks
- Deferred work / open questions / follow-ups
