---
name: sage-planning-make-plan
description: SAGE — phased, evidence-backed plans for multi-step work; orchestrator-friendly checkpoints.
---

# SAGE planning — Make a plan

## Purpose

**SAGE** orchestration works best with **phased plans** each agent can execute with **clear inputs, verifiers, and doc references**. This skill is for **planner** and human-in-the-loop steps.

## Rules

1. **Phase 0 — Discovery** — Read existing code, configs, and docs; list **allowed APIs** and file paths you actually saw (no invented methods).
2. **Phases 1..N** — Each phase has:
   - **Goal** (one paragraph)
   - **Tasks** (checklist, ordered)
   - **Evidence** — what to read or grep
   - **Verification** — commands or checks that prove the phase
3. **Final phase** — Integration test or end-to-end check for the whole change.

## Delegation

- Fact gathering (grep, read_file, list_dir) can be separated from synthesis; synthesis stays with the plan author.
- Every factual claim should point to a **source path** or URL.

## Anti-patterns

- Vague “implement the feature” without acceptance criteria.
- Phases that assume APIs not shown in the repo or docs.

## Cross-links

- Execution agents should follow **sage:discipline:*** and **sage:workflow:*** skills during implementation.
